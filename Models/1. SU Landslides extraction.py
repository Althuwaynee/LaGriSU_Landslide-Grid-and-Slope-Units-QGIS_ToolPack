"""
Model exported as python.
Name : 1. SU Landslides extraction
Group : SU (Slope Unit) analysis
With QGIS : 31400
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterExpression
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterFileDestination
from qgis.core import QgsProcessingParameterVectorDestination
from qgis.core import QgsProcessingParameterDefinition
import processing


class SuLandslidesExtraction(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        param = QgsProcessingParameterNumber('MinsizeofBasinDefault100mOrlargerthansinglepixelsize', 'Min size of Basin (Default =100 m) "Or larger than single pixel size"', type=QgsProcessingParameterNumber.Integer, defaultValue=100)
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))
        self.addParameter(QgsProcessingParameterExpression('addmaxshapeindexdefault7circle1sequare15equiteral2', 'Shape Index: Add max; default=6 (ex. small value for more uniform; 1= Circle, 2 = Equilateral)', parentLayerParameterName='', defaultValue='\"Shape_index\"  <  (6) '))
        self.addParameter(QgsProcessingParameterString('confirmallhavesameprojection', 'Confirm (add YES) using single projection ', multiLine=False, defaultValue=''))
        self.addParameter(QgsProcessingParameterRasterLayer('dem', 'Study area DEM (Raster)', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('landslidespoints', 'Landslides points/polygons', types=[QgsProcessing.TypeVector], defaultValue=None))
        self.addParameter(QgsProcessingParameterExpression('m', 'Minimum area of single SU (default=15000 m2) "Divide the scale by 1000 to get minimum dimension of visible object)', parentLayerParameterName='', defaultValue='area  <  (15000) '))
        self.addParameter(QgsProcessingParameterRasterDestination('DemFilled', 'DEM (filled)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('UnionSuOfStudyArea', 'Union (SU of study area)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('SlopeUnitsOfLandslides', 'Slope units of landslides', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('BoxPlot', 'Box Plot', fileFilter='HTML files (*.html)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('ChannelNetworkNeg', 'Channel network (neg.)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('ChannelNetworkPos', 'Channel network (pos)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('WatershedBasinNegative', 'Watershed Basin (negative)', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('WatershedBasinPosative', 'Watershed Basin (posative)', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(32, model_feedback)
        results = {}
        outputs = {}

        # Fill sinks (wang & liu)
        alg_params = {
            'ELEV': parameters['dem'],
            'MINSLOPE': 0.01,
            'FDIR': QgsProcessing.TEMPORARY_OUTPUT,
            'FILLED': QgsProcessing.TEMPORARY_OUTPUT,
            'WSHED': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FillSinksWangLiu'] = processing.run('saga:fillsinkswangliu', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Channel network and drainage basins
        alg_params = {
            'DEM': outputs['FillSinksWangLiu']['FILLED'],
            'THRESHOLD': 3,
            'BASIN': QgsProcessing.TEMPORARY_OUTPUT,
            'BASINS': QgsProcessing.TEMPORARY_OUTPUT,
            'CONNECTION': QgsProcessing.TEMPORARY_OUTPUT,
            'DIRECTION': QgsProcessing.TEMPORARY_OUTPUT,
            'NODES': QgsProcessing.TEMPORARY_OUTPUT,
            'ORDER': QgsProcessing.TEMPORARY_OUTPUT,
            'SEGMENTS': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ChannelNetworkAndDrainageBasins'] = processing.run('saga:channelnetworkanddrainagebasins', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Raster calculator
        alg_params = {
            'BAND_A': 1,
            'BAND_B': None,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '',
            'FORMULA': 'A*(-1)',
            'INPUT_A': outputs['FillSinksWangLiu']['FILLED'],
            'INPUT_B': None,
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterCalculator'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Flow accumulation (qm of esp)
        alg_params = {
            'DEM': outputs['FillSinksWangLiu']['FILLED'],
            'DZFILL': 0.1,
            'PREPROC': 0,
            'FLOW': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FlowAccumulationQmOfEsp'] = processing.run('saga:flowaccumulationqmofesp', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Flow accumulation (qm of esp)
        alg_params = {
            'DEM': outputs['RasterCalculator']['OUTPUT'],
            'DZFILL': 0.1,
            'PREPROC': 0,
            'FLOW': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FlowAccumulationQmOfEsp'] = processing.run('saga:flowaccumulationqmofesp', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Warp (reproject)
        alg_params = {
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': outputs['FillSinksWangLiu']['FILLED'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,
            'SOURCE_CRS': None,
            'TARGET_CRS': parameters['dem'],
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': parameters['DemFilled']
        }
        outputs['WarpReproject'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['DemFilled'] = outputs['WarpReproject']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Raster layer statistics
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['ChannelNetworkAndDrainageBasins']['BASIN']
        }
        outputs['RasterLayerStatistics'] = processing.run('qgis:rasterlayerstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Channel network and drainage basins
        alg_params = {
            'DEM': outputs['RasterCalculator']['OUTPUT'],
            'THRESHOLD': 3,
            'BASIN': QgsProcessing.TEMPORARY_OUTPUT,
            'BASINS': QgsProcessing.TEMPORARY_OUTPUT,
            'CONNECTION': QgsProcessing.TEMPORARY_OUTPUT,
            'DIRECTION': QgsProcessing.TEMPORARY_OUTPUT,
            'NODES': QgsProcessing.TEMPORARY_OUTPUT,
            'ORDER': QgsProcessing.TEMPORARY_OUTPUT,
            'SEGMENTS': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ChannelNetworkAndDrainageBasins'] = processing.run('saga:channelnetworkanddrainagebasins', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Raster layer statistics
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['ChannelNetworkAndDrainageBasins']['BASIN']
        }
        outputs['RasterLayerStatistics'] = processing.run('qgis:rasterlayerstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Channel network
        alg_params = {
            'DIV_CELLS': 10,
            'DIV_GRID': None,
            'ELEVATION': outputs['FillSinksWangLiu']['FILLED'],
            'INIT_GRID': outputs['FlowAccumulationQmOfEsp']['FLOW'],
            'INIT_METHOD': 2,
            'INIT_VALUE': outputs['RasterLayerStatistics']['MIN'],
            'MINLEN': 13,
            'SINKROUTE': outputs['ChannelNetworkAndDrainageBasins']['DIRECTION'],
            'TRACE_WEIGHT': None,
            'CHNLNTWRK': QgsProcessing.TEMPORARY_OUTPUT,
            'CHNLROUTE': QgsProcessing.TEMPORARY_OUTPUT,
            'SHAPES': parameters['ChannelNetworkPos']
        }
        outputs['ChannelNetwork'] = processing.run('saga:channelnetwork', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ChannelNetworkPos'] = outputs['ChannelNetwork']['SHAPES']

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Watershed basins
        alg_params = {
            'CHANNELS': outputs['ChannelNetwork']['CHNLNTWRK'],
            'ELEVATION': outputs['FillSinksWangLiu']['FILLED'],
            'MINSIZE': parameters['MinsizeofBasinDefault100mOrlargerthansinglepixelsize'],
            'SINKROUTE': None,
            'BASINS': parameters['WatershedBasinPosative']
        }
        outputs['WatershedBasins'] = processing.run('saga:watershedbasins', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['WatershedBasinPosative'] = outputs['WatershedBasins']['BASINS']

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Channel network
        alg_params = {
            'DIV_CELLS': 10,
            'DIV_GRID': None,
            'ELEVATION': outputs['RasterCalculator']['OUTPUT'],
            'INIT_GRID': outputs['FlowAccumulationQmOfEsp']['FLOW'],
            'INIT_METHOD': 2,
            'INIT_VALUE': outputs['RasterLayerStatistics']['MIN'],
            'MINLEN': 13,
            'SINKROUTE': outputs['ChannelNetworkAndDrainageBasins']['DIRECTION'],
            'TRACE_WEIGHT': None,
            'CHNLNTWRK': QgsProcessing.TEMPORARY_OUTPUT,
            'CHNLROUTE': QgsProcessing.TEMPORARY_OUTPUT,
            'SHAPES': parameters['ChannelNetworkNeg']
        }
        outputs['ChannelNetwork'] = processing.run('saga:channelnetwork', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ChannelNetworkNeg'] = outputs['ChannelNetwork']['SHAPES']

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Watershed basins
        alg_params = {
            'CHANNELS': outputs['ChannelNetwork']['CHNLNTWRK'],
            'ELEVATION': outputs['RasterCalculator']['OUTPUT'],
            'MINSIZE': parameters['MinsizeofBasinDefault100mOrlargerthansinglepixelsize'],
            'SINKROUTE': None,
            'BASINS': parameters['WatershedBasinNegative']
        }
        outputs['WatershedBasins'] = processing.run('saga:watershedbasins', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['WatershedBasinNegative'] = outputs['WatershedBasins']['BASINS']

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Polygonize (raster to vector)
        alg_params = {
            'BAND': 1,
            'EIGHT_CONNECTEDNESS': False,
            'EXTRA': '',
            'FIELD': 'DN',
            'INPUT': outputs['WatershedBasins']['BASINS'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PolygonizeRasterToVector'] = processing.run('gdal:polygonize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Fix geometries
        alg_params = {
            'INPUT': outputs['PolygonizeRasterToVector']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Polygonize (raster to vector)
        alg_params = {
            'BAND': 1,
            'EIGHT_CONNECTEDNESS': False,
            'EXTRA': '',
            'FIELD': 'DN',
            'INPUT': outputs['WatershedBasins']['BASINS'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PolygonizeRasterToVector'] = processing.run('gdal:polygonize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Fix geometries
        alg_params = {
            'INPUT': outputs['PolygonizeRasterToVector']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Union
        alg_params = {
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'OVERLAY': outputs['FixGeometries']['OUTPUT'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Union'] = processing.run('native:union', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Fix geometries
        alg_params = {
            'INPUT': outputs['Union']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Define layer projection
        alg_params = {
            'CRS': parameters['dem'],
            'INPUT': outputs['FixGeometries']['OUTPUT']
        }
        outputs['DefineLayerProjection'] = processing.run('qgis:definecurrentprojection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Multipart to singleparts
        alg_params = {
            'INPUT': outputs['DefineLayerProjection']['INPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MultipartToSingleparts'] = processing.run('native:multiparttosingleparts', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Add geometry attributes
        alg_params = {
            'CALC_METHOD': 0,
            'INPUT': outputs['MultipartToSingleparts']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddGeometryAttributes'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Select by expression
        alg_params = {
            'EXPRESSION': parameters['m'],
            'INPUT': outputs['AddGeometryAttributes']['OUTPUT'],
            'METHOD': 0
        }
        outputs['SelectByExpression'] = processing.run('qgis:selectbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Eliminate selected polygons
        alg_params = {
            'INPUT': outputs['SelectByExpression']['OUTPUT'],
            'MODE': 2,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['EliminateSelectedPolygons'] = processing.run('qgis:eliminateselectedpolygons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Extract by expression
        alg_params = {
            'EXPRESSION': parameters['m'],
            'INPUT': outputs['EliminateSelectedPolygons']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByExpression'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Symmetrical difference
        alg_params = {
            'INPUT': outputs['ExtractByExpression']['OUTPUT'],
            'OVERLAY': outputs['EliminateSelectedPolygons']['OUTPUT'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SymmetricalDifference'] = processing.run('native:symmetricaldifference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'ID',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '$id',
            'INPUT': outputs['SymmetricalDifference']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculator'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Shape_index',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': ' ( $perimeter   ^ 2) / ( $area  * 4 * \r\n3.14159265358979)',
            'INPUT': outputs['FieldCalculator']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculator'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # Box plot
        alg_params = {
            'INPUT': outputs['FieldCalculator']['OUTPUT'],
            'MSD': 0,
            'NAME_FIELD': 'DN',
            'VALUE_FIELD': 'Shape_index',
            'OUTPUT': parameters['BoxPlot']
        }
        outputs['BoxPlot'] = processing.run('qgis:boxplot', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['BoxPlot'] = outputs['BoxPlot']['OUTPUT']

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # Extract by expression
        alg_params = {
            'EXPRESSION': parameters['addmaxshapeindexdefault7circle1sequare15equiteral2'],
            'INPUT': outputs['FieldCalculator']['OUTPUT'],
            'OUTPUT': parameters['UnionSuOfStudyArea']
        }
        outputs['ExtractByExpression'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['UnionSuOfStudyArea'] = outputs['ExtractByExpression']['OUTPUT']

        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}

        # Extract by location
        alg_params = {
            'INPUT': outputs['ExtractByExpression']['OUTPUT'],
            'INTERSECT': parameters['landslidespoints'],
            'PREDICATE': [0],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByLocation'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}

        # Advanced Python field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Area',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,
            'FORMULA': 'value =  $geom.area()',
            'GLOBAL': '',
            'INPUT': outputs['ExtractByLocation']['OUTPUT'],
            'OUTPUT': parameters['SlopeUnitsOfLandslides']
        }
        outputs['AdvancedPythonFieldCalculator'] = processing.run('qgis:advancedpythonfieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SlopeUnitsOfLandslides'] = outputs['AdvancedPythonFieldCalculator']['OUTPUT']
        return results

    def name(self):
        return '1. SU Landslides extraction'

    def displayName(self):
        return '1. SU Landslides extraction'

    def group(self):
        return 'SU (Slope Unit) analysis'

    def groupId(self):
        return 'SU (Slope Unit) analysis'

    def createInstance(self):
        return SuLandslidesExtraction()
