"""
Model exported as python.
Name : 3. SU Extract Landslides-free inventory
Group : SU (Slope Unit) analysis
With QGIS : 31400
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterFeatureSource
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterExpression
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterFileDestination
from qgis.core import QgsProcessingParameterDefinition
from qgis.core import QgsExpression
import processing


class SuExtractLandslidesfreeInventory(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterString('SafeareasdistancefromproneareasDefault250m', 'Safe areas distance from prone areas (Default:250 m)', multiLine=False, defaultValue='250'))
        self.addParameter(QgsProcessingParameterString('landslideswithinslopesstat', 'Landslide-free slopes: ((default=10)) Use the html file "Original inventory within Slopes SU stat" in the results to replace the text below with prefered maximum Slope degree of landslide free areas', multiLine=False, defaultValue='ifelse(a < (10), 1, 0/0)'))
        self.addParameter(QgsProcessingParameterFeatureSource('slidesunitclass1', 'Dissolved slope units of landslides', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSource('unionsuofstudyarea', 'Union (SU of study area)', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('slope', 'Slope Raster (without flat areas)', defaultValue=None))
        param = QgsProcessingParameterExpression('test', 'DO NOT MODIFY THIS FIELD!', parentLayerParameterName='slidesunitclass1', defaultValue=' $area> @Basic_statistics_for_fields_FIRSTQUARTILE ')
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))
        self.addParameter(QgsProcessingParameterFeatureSink('LandslidefreeZones_option2ByBuffer', 'Landslide-Free zones_Option2 (by buffer)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('LandslidefreeZones_option1BySafeSlope', 'Landslide-Free zones_Option1 (by safe slope)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('LandslidefreeSuOption2Statistics', 'Landslide-Free SU  (option2) Statistics', optional=True, fileFilter='HTML files (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('LandslidefreeSuOption1', 'Landslide-Free SU (option1)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('LandslidefreeSuOption2', 'Landslide-Free SU (option2)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(27, model_feedback)
        results = {}
        outputs = {}

        # Raster calculator
        alg_params = {
            'FORMULA': parameters['landslideswithinslopesstat'],
            'GRIDS': parameters['slope'],
            'RESAMPLING': 0,
            'TYPE': 7,
            'USE_NODATA': True,
            'XGRIDS': None,
            'RESULT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterCalculator'] = processing.run('saga:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Raster calculator
        alg_params = {
            'CELLSIZE': 30,
            'CRS': parameters['slope'],
            'EXPRESSION': '\"Slope (without flat areas)@1\" * 0',
            'EXTENT': parameters['slope'],
            'LAYERS': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterCalculator'] = processing.run('qgis:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Promote to multipart
        alg_params = {
            'INPUT': parameters['unionsuofstudyarea'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PromoteToMultipart'] = processing.run('native:promotetomulti', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Basic statistics for fields
        alg_params = {
            'FIELD_NAME': 'Area',
            'INPUT_LAYER': parameters['slidesunitclass1']
        }
        outputs['BasicStatisticsForFields'] = processing.run('qgis:basicstatisticsforfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Buffer
        alg_params = {
            'DISSOLVE': True,
            'DISTANCE': parameters['SafeareasdistancefromproneareasDefault250m'],
            'END_CAP_STYLE': 0,
            'INPUT': parameters['slidesunitclass1'],
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
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

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Fix geometries
        alg_params = {
            'INPUT': outputs['Buffer']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

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
            'TARGET_CRS': parameters['slope'],
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['WarpReproject'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Difference
        alg_params = {
            'INPUT': outputs['PromoteToMultipart']['OUTPUT'],
            'OVERLAY': parameters['slidesunitclass1'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Difference'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Polygonize (raster to vector)
        alg_params = {
            'BAND': 1,
            'EIGHT_CONNECTEDNESS': False,
            'EXTRA': '',
            'FIELD': 'DN',
            'INPUT': outputs['WarpReproject']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PolygonizeRasterToVector'] = processing.run('gdal:polygonize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Extract by expression
        alg_params = {
            'EXPRESSION': parameters['test'],
            'INPUT': outputs['Difference']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByExpression'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Reproject layer
        alg_params = {
            'INPUT': outputs['PolygonizeRasterToVector']['OUTPUT'],
            'OPERATION': '',
            'TARGET_CRS': parameters['slope'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Dissolve
        alg_params = {
            'FIELD': [''],
            'INPUT': outputs['PolygonizeRasterToVector']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Dissolve'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Fix geometries
        alg_params = {
            'INPUT': outputs['Dissolve']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Difference
        alg_params = {
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'OVERLAY': outputs['FixGeometries']['OUTPUT'],
            'OUTPUT': parameters['LandslidefreeZones_option2ByBuffer']
        }
        outputs['Difference'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['LandslidefreeZones_option2ByBuffer'] = outputs['Difference']['OUTPUT']

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Extract by location
        alg_params = {
            'INPUT': outputs['ExtractByExpression']['OUTPUT'],
            'INTERSECT': outputs['Difference']['OUTPUT'],
            'PREDICATE': [6],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByLocation'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Reproject layer
        alg_params = {
            'INPUT': outputs['ExtractByLocation']['OUTPUT'],
            'OPERATION': '',
            'TARGET_CRS': parameters['slidesunitclass1'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Extract by location
        alg_params = {
            'INPUT': outputs['ExtractByExpression']['OUTPUT'],
            'INTERSECT': outputs['Difference']['OUTPUT'],
            'PREDICATE': [6],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByLocation'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Extract by location
        alg_params = {
            'INPUT': outputs['ExtractByLocation']['OUTPUT'],
            'INTERSECT': outputs['ReprojectLayer']['OUTPUT'],
            'PREDICATE': [0],
            'OUTPUT': parameters['LandslidefreeZones_option1BySafeSlope']
        }
        outputs['ExtractByLocation'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['LandslidefreeZones_option1BySafeSlope'] = outputs['ExtractByLocation']['OUTPUT']

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Random extract
        alg_params = {
            'INPUT': outputs['ReprojectLayer']['OUTPUT'],
            'METHOD': 0,
            'NUMBER': QgsExpression('( @Basic_statistics_for_fields_COUNT )*(1)').evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RandomExtract'] = processing.run('native:randomextract', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Reproject layer
        alg_params = {
            'INPUT': outputs['ExtractByLocation']['OUTPUT'],
            'OPERATION': '',
            'TARGET_CRS': parameters['slidesunitclass1'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Multipart to singleparts
        alg_params = {
            'INPUT': outputs['RandomExtract']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MultipartToSingleparts'] = processing.run('native:multiparttosingleparts', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Random extract
        alg_params = {
            'INPUT': outputs['ReprojectLayer']['OUTPUT'],
            'METHOD': 0,
            'NUMBER': QgsExpression('( @Basic_statistics_for_fields_COUNT )*(1)').evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RandomExtract'] = processing.run('native:randomextract', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Multipart to singleparts
        alg_params = {
            'INPUT': outputs['RandomExtract']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MultipartToSingleparts'] = processing.run('native:multiparttosingleparts', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Add geometry attributes
        alg_params = {
            'CALC_METHOD': 0,
            'INPUT': outputs['MultipartToSingleparts']['OUTPUT'],
            'OUTPUT': parameters['LandslidefreeSuOption2']
        }
        outputs['AddGeometryAttributes'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['LandslidefreeSuOption2'] = outputs['AddGeometryAttributes']['OUTPUT']

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Add geometry attributes
        alg_params = {
            'CALC_METHOD': 0,
            'INPUT': outputs['MultipartToSingleparts']['OUTPUT'],
            'OUTPUT': parameters['LandslidefreeSuOption1']
        }
        outputs['AddGeometryAttributes'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['LandslidefreeSuOption1'] = outputs['AddGeometryAttributes']['OUTPUT']

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Basic statistics for fields
        alg_params = {
            'FIELD_NAME': 'area_3',
            'INPUT_LAYER': outputs['AddGeometryAttributes']['OUTPUT'],
            'OUTPUT_HTML_FILE': parameters['LandslidefreeSuOption2Statistics']
        }
        outputs['BasicStatisticsForFields'] = processing.run('qgis:basicstatisticsforfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['LandslidefreeSuOption2Statistics'] = outputs['BasicStatisticsForFields']['OUTPUT_HTML_FILE']
        return results

    def name(self):
        return '3. SU Extract Landslides-free inventory'

    def displayName(self):
        return '3. SU Extract Landslides-free inventory'

    def group(self):
        return 'SU (Slope Unit) analysis'

    def groupId(self):
        return 'SU (Slope Unit) analysis'

    def createInstance(self):
        return SuExtractLandslidesfreeInventory()
