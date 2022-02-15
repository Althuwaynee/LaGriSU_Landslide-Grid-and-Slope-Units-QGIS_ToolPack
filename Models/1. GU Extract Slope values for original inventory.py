"""
Model exported as python.
Name : 1. GU Extract Slope values for original inventory
Group : GU (Grid Unit) analysis
With QGIS : 31400
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterFileDestination
from qgis.core import QgsProcessingParameterVectorDestination
import processing


class GuExtractSlopeValuesForOriginalInventory(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))
        self.addParameter(QgsProcessingParameterRasterLayer('dem', 'DEM (Study area)', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('landslidespoints', 'Landslides inventory (points or polygons)', types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('SlopeRaster', 'Slope Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('StatisticsSummary_landslidesWithSlopeValue', 'Statistics summary_Landslides with Slope value', optional=True, fileFilter='HTML files (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('BoxPlotSlopeValuesWithinLandslidesLocations', 'Box Plot Slope values within Landslides locations', fileFilter='HTML files (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('LandslidesWithSlopeValue', 'Landslides with Slope value', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(5, model_feedback)
        results = {}
        outputs = {}

        # Slope
        alg_params = {
            'AS_PERCENT': False,
            'BAND': 1,
            'COMPUTE_EDGES': False,
            'EXTRA': '',
            'INPUT': parameters['dem'],
            'OPTIONS': '',
            'SCALE': 1,
            'ZEVENBERGEN': False,
            'OUTPUT': parameters['SlopeRaster']
        }
        outputs['Slope'] = processing.run('gdal:slope', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SlopeRaster'] = outputs['Slope']['OUTPUT']

        feedback.setCurrentStep(1)
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

        feedback.setCurrentStep(2)
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

        feedback.setCurrentStep(3)
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

        feedback.setCurrentStep(4)
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
        return results

    def name(self):
        return '1. GU Extract Slope values for original inventory'

    def displayName(self):
        return '1. GU Extract Slope values for original inventory'

    def group(self):
        return 'GU (Grid Unit) analysis'

    def groupId(self):
        return 'GU (Grid Unit) analysis'

    def createInstance(self):
        return GuExtractSlopeValuesForOriginalInventory()
