"""
Model exported as python.
Name : 3.a. GU Extract Training and Testing samples
Group : GU (Grid Unit) analysis
With QGIS : 31400
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterRasterDestination
import processing


class AGuExtractTrainingAndTestingSamples(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterNumber('trainingpercentage', 'Training percentage (ex. if 70:30 enter 70)', type=QgsProcessingParameterNumber.Double, minValue=0, maxValue=100, defaultValue=70))
        self.addParameter(QgsProcessingParameterNumber('gridsize', 'Grid unit width (in meter) "use DEM pixel width"', type=QgsProcessingParameterNumber.Double, minValue=0, maxValue=100000, defaultValue=10))
        self.addParameter(QgsProcessingParameterVectorLayer('safeunitsclass0', 'Landslide-Free points/polygons (Note: see if point or polygon invneotry)', types=[QgsProcessing.TypeVectorPoint,QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('landslideswithinslopes', 'Landslides with Slope value', types=[QgsProcessing.TypeVectorPoint,QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('slope', 'Slope Raster', defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))
        self.addParameter(QgsProcessingParameterFeatureSink('TestingGu1', 'Testing GU 1', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('TrainingGu1', 'Training GU 1', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('TestingGu0', 'Testing GU 0', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('TrainingGu0', 'Training GU 0', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('EmptyRaster', 'Empty Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('TestingGu10', 'Testing GU 1 0', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('TrainingGu10', 'Training GU 1 0', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(21, model_feedback)
        results = {}
        outputs = {}

        # Field calculator Safe zonesG class 0
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'IDI',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '1',
            'INPUT': parameters['safeunitsclass0'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorSafeZonesgClass0'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Random extract within subsets 0 T New
        alg_params = {
            'FIELD': 'DI',
            'INPUT': outputs['FieldCalculatorSafeZonesgClass0']['OUTPUT'],
            'METHOD': 1,
            'NUMBER': parameters['trainingpercentage'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RandomExtractWithinSubsets0TNew'] = processing.run('qgis:randomextractwithinsubsets', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Create constant raster layer
        alg_params = {
            'EXTENT': parameters['slope'],
            'NUMBER': 0,
            'OUTPUT_TYPE': 5,
            'PIXEL_SIZE': 100,
            'TARGET_CRS': parameters['slope'],
            'OUTPUT': parameters['EmptyRaster']
        }
        outputs['CreateConstantRasterLayer'] = processing.run('native:createconstantrasterlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['EmptyRaster'] = outputs['CreateConstantRasterLayer']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Vector grid
        alg_params = {
            'CRS': 'ProjectCrs',
            'EXTENT': parameters['slope'],
            'HOVERLAY': 0,
            'HSPACING': parameters['gridsize'],
            'TYPE': 2,
            'VOVERLAY': 0,
            'VSPACING': parameters['gridsize'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['VectorGrid'] = processing.run('qgis:creategrid', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Field calculator Slides zoneG class 1
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'IDI',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '1',
            'INPUT': parameters['landslideswithinslopes'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorSlidesZonegClass1'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Difference 000
        alg_params = {
            'INPUT': outputs['FieldCalculatorSafeZonesgClass0']['OUTPUT'],
            'OVERLAY': outputs['RandomExtractWithinSubsets0TNew']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Difference000'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Extract location Safe zonesG class 0
        alg_params = {
            'INPUT': outputs['VectorGrid']['OUTPUT'],
            'INTERSECT': outputs['RandomExtractWithinSubsets0TNew']['OUTPUT'],
            'PREDICATE': [0],
            'OUTPUT': parameters['TrainingGu0']
        }
        outputs['ExtractLocationSafeZonesgClass0'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TrainingGu0'] = outputs['ExtractLocationSafeZonesgClass0']['OUTPUT']

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Random extract within subsets NEW
        alg_params = {
            'FIELD': 'IDI',
            'INPUT': outputs['FieldCalculatorSlidesZonegClass1']['OUTPUT'],
            'METHOD': 1,
            'NUMBER': parameters['trainingpercentage'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RandomExtractWithinSubsetsNew'] = processing.run('qgis:randomextractwithinsubsets', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Extract by location 111
        alg_params = {
            'INPUT': outputs['VectorGrid']['OUTPUT'],
            'INTERSECT': outputs['RandomExtractWithinSubsetsNew']['OUTPUT'],
            'PREDICATE': [0],
            'OUTPUT': parameters['TrainingGu1']
        }
        outputs['ExtractByLocation111'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TrainingGu1'] = outputs['ExtractByLocation111']['OUTPUT']

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Extract by expression test 0
        alg_params = {
            'EXPRESSION': '$geometry is not null',
            'INPUT': outputs['Difference000']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByExpressionTest0'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Fix geometries
        alg_params = {
            'INPUT': outputs['RandomExtractWithinSubsetsNew']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Difference Testing zonesG 111
        alg_params = {
            'INPUT': outputs['FieldCalculatorSlidesZonegClass1']['OUTPUT'],
            'OVERLAY': outputs['FixGeometries']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DifferenceTestingZonesg111'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Union Training zonesG 1 0
        alg_params = {
            'INPUT': outputs['ExtractByLocation111']['OUTPUT'],
            'OVERLAY': outputs['ExtractLocationSafeZonesgClass0']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnionTrainingZonesg10'] = processing.run('native:union', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Extract by location NEW 0
        alg_params = {
            'INPUT': outputs['VectorGrid']['OUTPUT'],
            'INTERSECT': outputs['ExtractByExpressionTest0']['OUTPUT'],
            'PREDICATE': [0],
            'OUTPUT': parameters['TestingGu0']
        }
        outputs['ExtractByLocationNew0'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TestingGu0'] = outputs['ExtractByLocationNew0']['OUTPUT']

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Extract by expression Testing zonesG 1
        alg_params = {
            'EXPRESSION': '$geometry is not null',
            'INPUT': outputs['DifferenceTestingZonesg111']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByExpressionTestingZonesg1'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Extract by location NEW 1
        alg_params = {
            'INPUT': outputs['VectorGrid']['OUTPUT'],
            'INTERSECT': outputs['ExtractByExpressionTestingZonesg1']['OUTPUT'],
            'PREDICATE': [0],
            'OUTPUT': parameters['TestingGu1']
        }
        outputs['ExtractByLocationNew1'] = processing.run('native:extractbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TestingGu1'] = outputs['ExtractByLocationNew1']['OUTPUT']

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Extract by expression
        alg_params = {
            'EXPRESSION': '$geometry is not null',
            'INPUT': outputs['UnionTrainingZonesg10']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByExpression'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Union Testing zonesG 0 1
        alg_params = {
            'INPUT': outputs['ExtractByLocationNew1']['OUTPUT'],
            'OVERLAY': outputs['ExtractByLocationNew0']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnionTestingZonesg01'] = processing.run('native:union', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Training',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': 'CASE \r\n  WHEN  \"id\"   > 0 THEN 1\r\n  ELSE 0\r\nEND',
            'INPUT': outputs['ExtractByExpression']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': parameters['TrainingGu10']
        }
        outputs['FieldCalculator'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TrainingGu10'] = outputs['FieldCalculator']['OUTPUT']

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Extract by expression
        alg_params = {
            'EXPRESSION': '$geometry is not null',
            'INPUT': outputs['UnionTestingZonesg01']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByExpression'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Testing',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': 'CASE \r\n  WHEN  \"id\"   > 0 THEN 1\r\n  ELSE 0\r\nEND',
            'INPUT': outputs['ExtractByExpression']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': parameters['TestingGu10']
        }
        outputs['FieldCalculator'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TestingGu10'] = outputs['FieldCalculator']['OUTPUT']
        return results

    def name(self):
        return '3.a. GU Extract Training and Testing samples'

    def displayName(self):
        return '3.a. GU Extract Training and Testing samples'

    def group(self):
        return 'GU (Grid Unit) analysis'

    def groupId(self):
        return 'GU (Grid Unit) analysis'

    def createInstance(self):
        return AGuExtractTrainingAndTestingSamples()
