"""
Model exported as python.
Name : 2. SU Extract Slope values for original inventory
Group : SU (Slope Unit) analysis
With QGIS : 31400
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSource
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterFileDestination
from qgis.core import QgsProcessingParameterVectorDestination
import processing


class SuExtractSlopeValuesForOriginalInventory(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('landslidespoints', 'Landslides points/polygons', types=[QgsProcessing.TypeVector], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSource('Slopeunitsoflandslides', 'Slope units of landslides', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('dem2', 'DEM (filled)', defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))
        self.addParameter(QgsProcessingParameterRasterDestination('SlopeRasterWithoutFlatAreas', 'Slope Raster (without flat areas)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('DissolvedSlopeUnitsOfLandslides', 'Dissolved slope units of landslides', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('StatisticsSummary_landslidesWithSlopeValue', 'Statistics summary_Landslides with Slope value', optional=True, fileFilter='HTML files (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('BoxPlotSlopeValuesWithinLandslidesLocations', 'Box Plot Slope values within Landslides locations', fileFilter='HTML files (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('LandslidesWithSlopeValue', 'Landslides with Slope value', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(10, model_feedback)
        results = {}
        outputs = {}

        # Slope
        alg_params = {
            'AS_PERCENT': False,
            'BAND': 1,
            'COMPUTE_EDGES': False,
            'INPUT': parameters['dem2'],
            'OPTIONS': '',
            'SCALE': 1,
            'ZEVENBERGEN': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Slope'] = processing.run('gdal:slope', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Raster calculator
        alg_params = {
            'FORMULA': 'ifelse(a >(1), 1, 0/0)',
            'GRIDS': outputs['Slope']['OUTPUT'],
            'RESAMPLING': 0,
            'TYPE': 7,
            'USE_NODATA': False,
            'XGRIDS': [],
            'RESULT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterCalculator'] = processing.run('saga:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Raster calculator
        alg_params = {
            'FNAME': False,
            'FORMULA': 'a*b',
            'GRIDS': outputs['RasterCalculator']['RESULT'],
            'NAME': 'Calculation',
            'RESAMPLING': 0,
            'TYPE': 7,
            'USE_NODATA': False,
            'XGRIDS': outputs['Slope']['OUTPUT'],
            'RESULT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterCalculator'] = processing.run('saga:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'DI',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '1',
            'INPUT': parameters['landslidespoints'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculator'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Add raster values to features
        alg_params = {
            'GRIDS': outputs['Slope']['OUTPUT'],
            'RESAMPLING': 0,
            'SHAPES': outputs['FieldCalculator']['OUTPUT'],
            'RESULT': parameters['LandslidesWithSlopeValue']
        }
        outputs['AddRasterValuesToFeatures'] = processing.run('saga:addrastervaluestofeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['LandslidesWithSlopeValue'] = outputs['AddRasterValuesToFeatures']['RESULT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Join attributes by location
        alg_params = {
            'DISCARD_NONMATCHING': True,
            'INPUT': parameters['Slopeunitsoflandslides'],
            'JOIN': outputs['AddRasterValuesToFeatures']['RESULT'],
            'JOIN_FIELDS': [''],
            'METHOD': 0,
            'PREDICATE': [0,1,2,3,4,5,6],
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByLocation'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Basic statistics for fields
        alg_params = {
            'FIELD_NAME': 'OUTPUT',
            'INPUT_LAYER': outputs['AddRasterValuesToFeatures']['RESULT'],
            'OUTPUT_HTML_FILE': parameters['StatisticsSummary_landslidesWithSlopeValue']
        }
        outputs['BasicStatisticsForFields'] = processing.run('qgis:basicstatisticsforfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['StatisticsSummary_landslidesWithSlopeValue'] = outputs['BasicStatisticsForFields']['OUTPUT_HTML_FILE']

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Warp (reproject)
        alg_params = {
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': outputs['RasterCalculator']['RESULT'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,
            'SOURCE_CRS': None,
            'TARGET_CRS': parameters['dem2'],
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': parameters['SlopeRasterWithoutFlatAreas']
        }
        outputs['WarpReproject'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SlopeRasterWithoutFlatAreas'] = outputs['WarpReproject']['OUTPUT']

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Box plot
        alg_params = {
            'INPUT': outputs['AddRasterValuesToFeatures']['RESULT'],
            'MSD': 0,
            'NAME_FIELD': 'DI',
            'VALUE_FIELD': 'OUTPUT',
            'OUTPUT': parameters['BoxPlotSlopeValuesWithinLandslidesLocations']
        }
        outputs['BoxPlot'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['BoxPlotSlopeValuesWithinLandslidesLocations'] = outputs['BoxPlot']['OUTPUT']

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Dissolve
        alg_params = {
            'FIELD': ['OUTPUT'],
            'INPUT': outputs['JoinAttributesByLocation']['OUTPUT'],
            'OUTPUT': parameters['DissolvedSlopeUnitsOfLandslides']
        }
        outputs['Dissolve'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['DissolvedSlopeUnitsOfLandslides'] = outputs['Dissolve']['OUTPUT']
        return results

    def name(self):
        return '2. SU Extract Slope values for original inventory'

    def displayName(self):
        return '2. SU Extract Slope values for original inventory'

    def group(self):
        return 'SU (Slope Unit) analysis'

    def groupId(self):
        return 'SU (Slope Unit) analysis'

    def createInstance(self):
        return SuExtractSlopeValuesForOriginalInventory()
