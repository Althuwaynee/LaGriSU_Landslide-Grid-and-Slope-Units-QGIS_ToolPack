"""
Model exported as python.
Name : 4.a. SU Extract Training and Testing samples
Group : SU (Slope Unit) analysis
With QGIS : 31400
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterRasterDestination
import processing


class ASuExtractTrainingAndTestingSamples(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))
        self.addParameter(QgsProcessingParameterVectorLayer('safeunitsclass0', 'Landslide-Free SU (Note: option 1 or 2)', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('slidesunitsclass1', 'Dissolved slope units of landslides', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('slope', 'DEM (filled)', defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('trainingpercentage', 'Training percentage (Default =70)', type=QgsProcessingParameterNumber.Double, minValue=0, maxValue=100, defaultValue=70))
        self.addParameter(QgsProcessingParameterFeatureSink('TestingZones0', 'Testing zones 0', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('TestingZones1', 'Testing zones 1', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('EmptyRaster', 'Empty Raster', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('TestingZones10Su', 'Testing zones 1 0 SU', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('TrainingZones10Su', 'Training zones 1 0 SU', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('TrainingZones1', 'Training zones 1', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('TrainingZones0', 'Training zones 0', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(16, model_feedback)
        results = {}
        outputs = {}

        # Field calculator
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
        outputs['FieldCalculator'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Field calculator slides u class1
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'IDI',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': '1',
            'INPUT': parameters['slidesunitsclass1'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorSlidesUClass1'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

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

        # Fix geometries
        alg_params = {
            'INPUT': outputs['FieldCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Random extract within subsets Training zones 0
        alg_params = {
            'FIELD': 'IDI',
            'INPUT': outputs['FieldCalculator']['OUTPUT'],
            'METHOD': 1,
            'NUMBER': parameters['trainingpercentage'],
            'OUTPUT': parameters['TrainingZones0']
        }
        outputs['RandomExtractWithinSubsetsTrainingZones0'] = processing.run('qgis:randomextractwithinsubsets', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TrainingZones0'] = outputs['RandomExtractWithinSubsetsTrainingZones0']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Random extract within subsets Training zones 1
        alg_params = {
            'FIELD': 'IDI',
            'INPUT': outputs['FieldCalculatorSlidesUClass1']['OUTPUT'],
            'METHOD': 1,
            'NUMBER': parameters['trainingpercentage'],
            'OUTPUT': parameters['TrainingZones1']
        }
        outputs['RandomExtractWithinSubsetsTrainingZones1'] = processing.run('qgis:randomextractwithinsubsets', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TrainingZones1'] = outputs['RandomExtractWithinSubsetsTrainingZones1']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Fix geometries
        alg_params = {
            'INPUT': outputs['FieldCalculatorSlidesUClass1']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Fix geometries
        alg_params = {
            'INPUT': outputs['RandomExtractWithinSubsetsTrainingZones1']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Fix geometries
        alg_params = {
            'INPUT': outputs['RandomExtractWithinSubsetsTrainingZones0']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Symmetrical difference
        alg_params = {
            'A': outputs['FixGeometries']['OUTPUT'],
            'B': outputs['FixGeometries']['OUTPUT'],
            'SPLIT': False,
            'RESULT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SymmetricalDifference'] = processing.run('saga:symmetricaldifference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Difference
        alg_params = {
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'OVERLAY': outputs['FixGeometries']['OUTPUT'],
            'OUTPUT': parameters['TestingZones0']
        }
        outputs['Difference'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TestingZones0'] = outputs['Difference']['OUTPUT']

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Difference
        alg_params = {
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'OVERLAY': outputs['FixGeometries']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Difference'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Reproject layer
        alg_params = {
            'INPUT': outputs['Difference']['OUTPUT'],
            'TARGET_CRS': 'ProjectCrs',
            'OUTPUT': parameters['TestingZones1']
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TestingZones1'] = outputs['ReprojectLayer']['OUTPUT']

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Training',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': 'CASE \r\n  WHEN  \"Area\"   = 0 THEN 1\r\n  ELSE 0\r\nEND',
            'INPUT': outputs['SymmetricalDifference']['RESULT'],
            'NEW_FIELD': True,
            'OUTPUT': parameters['TrainingZones10Su']
        }
        outputs['FieldCalculator'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TrainingZones10Su'] = outputs['FieldCalculator']['OUTPUT']

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Symmetrical difference
        alg_params = {
            'A': outputs['ReprojectLayer']['OUTPUT'],
            'B': outputs['Difference']['OUTPUT'],
            'SPLIT': False,
            'RESULT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SymmetricalDifference'] = processing.run('saga:symmetricaldifference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Testing',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': 'CASE \r\n  WHEN  \"Area\"   = 0 THEN 0\r\n  ELSE 1\r\nEND',
            'INPUT': outputs['SymmetricalDifference']['RESULT'],
            'NEW_FIELD': True,
            'OUTPUT': parameters['TestingZones10Su']
        }
        outputs['FieldCalculator'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TestingZones10Su'] = outputs['FieldCalculator']['OUTPUT']
        return results

    def name(self):
        return '4.a. SU Extract Training and Testing samples'

    def displayName(self):
        return '4.a. SU Extract Training and Testing samples'

    def group(self):
        return 'SU (Slope Unit) analysis'

    def groupId(self):
        return 'SU (Slope Unit) analysis'

    def createInstance(self):
        return ASuExtractTrainingAndTestingSamples()
