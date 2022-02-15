"""
Model exported as python.
Name : 2. GU Extract Landslides-free inventory
Group : GU (Grid Unit) analysis
With QGIS : 31400
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterFileDestination
from qgis.core import QgsExpression
import processing


class GuExtractLandslidesfreeInventory(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterString('safeslopesdegnoslides', 'Safe areas slope degree: ((default=10)) Use the html file "Original inventory within Slopes SU stat" in the results to replace the text below with prefered maximum Slope degree of landslide free areas', multiLine=False, defaultValue='ifelse(a < (10), 1, 0/0)'))
        self.addParameter(QgsProcessingParameterString('SafeareasdistancefromproneareasDefault250m', 'Safe areas distance from prone areas (Default:250 m)', multiLine=False, defaultValue='250'))
        self.addParameter(QgsProcessingParameterVectorLayer('landslideinventory', 'Landslides with Slope value (polygon or points)', types=[QgsProcessing.TypeVectorPoint,QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('slope', 'Slope Raster', defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))
        self.addParameter(QgsProcessingParameterFeatureSink('LandslidefreePolygonsOption1', 'Landslide-Free polygons (option1)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('LandslidefreePolygonsOption2', 'Landslide-Free polygons (option2)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('LandslidefreeZones_option2ByBuffer', 'Landslide-Free zones_Option2 (by buffer)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('LandslidefreeZones_option1BySafeSlope', 'Landslide-Free zones_Option1 (by safe slope)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('SummaryOfLandslidesAreaStatistics', 'Summary of Landslides area statistics', optional=True, fileFilter='HTML files (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('BoxPlotOfLandslidesAreaStatistics', 'Box plot of Landslides area statistics', fileFilter='HTML files (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('LandslidefreePointsOption1', 'Landslide-Free points (option1)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('LandslidefreePointsOption2', 'Landslide-Free points (option2)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(24, model_feedback)
        results = {}
        outputs = {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Class_area',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': ' $area ',
            'INPUT': parameters['landslideinventory'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculator'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Raster calculator
        alg_params = {
            'FORMULA': parameters['safeslopesdegnoslides'],
            'GRIDS': parameters['slope'],
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
            'CELLSIZE': 30,
            'CRS': parameters['slope'],
            'EXPRESSION': '\"Slope@1\" * 0',
            'EXTENT': parameters['slope'],
            'LAYERS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterCalculator'] = processing.run('qgis:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Polygonize (raster to vector)
        alg_params = {
            'BAND': 1,
            'EIGHT_CONNECTEDNESS': False,
            'EXTRA': '',
            'FIELD': 'DN',
            'INPUT': outputs['RasterCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PolygonizeRasterToVector'] = processing.run('gdal:polygonize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Buffer
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': parameters['SafeareasdistancefromproneareasDefault250m'],
            'END_CAP_STYLE': 0,
            'INPUT': parameters['landslideinventory'],
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Dissolve
        alg_params = {
            'FIELD': [''],
            'INPUT': outputs['PolygonizeRasterToVector']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Dissolve'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'count',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': '1',
            'INPUT': parameters['landslideinventory'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculator'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Fix geometries
        alg_params = {
            'INPUT': parameters['landslideinventory'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Basic statistics for fields
        alg_params = {
            'FIELD_NAME': 'Class_area',
            'INPUT_LAYER': outputs['FieldCalculator']['OUTPUT'],
            'OUTPUT_HTML_FILE': parameters['SummaryOfLandslidesAreaStatistics']
        }
        outputs['BasicStatisticsForFields'] = processing.run('qgis:basicstatisticsforfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SummaryOfLandslidesAreaStatistics'] = outputs['BasicStatisticsForFields']['OUTPUT_HTML_FILE']

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Box plot
        alg_params = {
            'INPUT': outputs['FieldCalculator']['OUTPUT'],
            'MSD': 0,
            'NAME_FIELD': 'DI',
            'VALUE_FIELD': 'Class_area',
            'OUTPUT': parameters['BoxPlotOfLandslidesAreaStatistics']
        }
        outputs['BoxPlot'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['BoxPlotOfLandslidesAreaStatistics'] = outputs['BoxPlot']['OUTPUT']

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Polygonize (raster to vector)
        alg_params = {
            'BAND': 1,
            'EIGHT_CONNECTEDNESS': False,
            'EXTRA': '',
            'FIELD': 'DN',
            'INPUT': outputs['RasterCalculator']['RESULT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PolygonizeRasterToVector'] = processing.run('gdal:polygonize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Fix geometries
        alg_params = {
            'INPUT': outputs['Dissolve']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Basic statistics for fields
        alg_params = {
            'FIELD_NAME': 'count',
            'INPUT_LAYER': outputs['FieldCalculator']['OUTPUT']
        }
        outputs['BasicStatisticsForFields'] = processing.run('qgis:basicstatisticsforfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Fix geometries
        alg_params = {
            'INPUT': outputs['PolygonizeRasterToVector']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Difference
        alg_params = {
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'OVERLAY': outputs['Buffer']['OUTPUT'],
            'OUTPUT': parameters['LandslidefreeZones_option2ByBuffer']
        }
        outputs['Difference'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['LandslidefreeZones_option2ByBuffer'] = outputs['Difference']['OUTPUT']

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Random points in layer bounds
        alg_params = {
            'INPUT': outputs['Difference']['OUTPUT'],
            'MIN_DISTANCE': 0,
            'POINTS_NUMBER': outputs['BasicStatisticsForFields']['COUNT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RandomPointsInLayerBounds'] = processing.run('qgis:randompointsinlayerbounds', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'ID',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '1',
            'INPUT': outputs['RandomPointsInLayerBounds']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': parameters['LandslidefreePointsOption2']
        }
        outputs['FieldCalculator'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['LandslidefreePointsOption2'] = outputs['FieldCalculator']['OUTPUT']

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Difference
        alg_params = {
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'OVERLAY': outputs['FixGeometries']['OUTPUT'],
            'OUTPUT': parameters['LandslidefreeZones_option1BySafeSlope']
        }
        outputs['Difference'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['LandslidefreeZones_option1BySafeSlope'] = outputs['Difference']['OUTPUT']

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Buffer
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': QgsExpression('( (@Basic_statistics_for_fields_MEAN)  ^ (0.5))/2').evaluate(),
            'END_CAP_STYLE': 2,
            'INPUT': outputs['FieldCalculator']['OUTPUT'],
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Random points in layer bounds
        alg_params = {
            'INPUT': outputs['Difference']['OUTPUT'],
            'MIN_DISTANCE': 100,
            'POINTS_NUMBER': outputs['BasicStatisticsForFields']['COUNT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RandomPointsInLayerBounds'] = processing.run('qgis:randompointsinlayerbounds', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Clip
        alg_params = {
            'INPUT': outputs['Buffer']['OUTPUT'],
            'OVERLAY': outputs['Difference']['OUTPUT'],
            'OUTPUT': parameters['LandslidefreePolygonsOption2']
        }
        outputs['Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['LandslidefreePolygonsOption2'] = outputs['Clip']['OUTPUT']

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'DI',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '1',
            'INPUT': outputs['RandomPointsInLayerBounds']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': parameters['LandslidefreePointsOption1']
        }
        outputs['FieldCalculator'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['LandslidefreePointsOption1'] = outputs['FieldCalculator']['OUTPUT']

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Buffer
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': QgsExpression(' (@Basic_statistics_for_fields_MEAN)  ^ (0.5)').evaluate(),
            'END_CAP_STYLE': 2,
            'INPUT': outputs['FieldCalculator']['OUTPUT'],
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Clip
        alg_params = {
            'INPUT': outputs['Buffer']['OUTPUT'],
            'OVERLAY': outputs['Difference']['OUTPUT'],
            'OUTPUT': parameters['LandslidefreePolygonsOption1']
        }
        outputs['Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['LandslidefreePolygonsOption1'] = outputs['Clip']['OUTPUT']
        return results

    def name(self):
        return '2. GU Extract Landslides-free inventory'

    def displayName(self):
        return '2. GU Extract Landslides-free inventory'

    def group(self):
        return 'GU (Grid Unit) analysis'

    def groupId(self):
        return 'GU (Grid Unit) analysis'

    def createInstance(self):
        return GuExtractLandslidesfreeInventory()
