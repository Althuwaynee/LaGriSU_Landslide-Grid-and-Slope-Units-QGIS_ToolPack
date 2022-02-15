"""
Model exported as python.
Name : 4.b. SU Extract conditioning factors values
Group : SU (Slope Unit) analysis
With QGIS : 31400
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterLayer
import processing


class BSuExtractConditioningFactorsValues(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))
        self.addParameter(QgsProcessingParameterString('note', 'Note:', optional=True, multiLine=False, defaultValue='Later, in resultant layer, keep \"Var_majority\" for Categorial var. and \"Var_mean\" for Continous var.'))
        self.addParameter(QgsProcessingParameterVectorLayer('testingzones10', 'Testing zones 1 0 SU', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('trainingzones10', 'Training zones 1 0 SU', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('var10', 'Var1', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('var11', 'Var2 (or insert the Empty Raster)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('var12', 'Var3 (or insert the Empty Raster)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('var132', 'Var4 (or insert the Empty Raster)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('var14', 'Var5 (or insert the Empty Raster)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('var15', 'Var6 (or insert the Empty Raster)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('var16', 'Var7 (or insert the Empty Raster)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('var17', 'Var8 (or insert the Empty Raster)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('var18', 'Var9 (or insert the Empty Raster)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('var42', 'Var10 (or insert the Empty Raster)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('var5', 'Var11 (or insert the Empty Raster)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('var6', 'Var12 (or insert the Empty Raster)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('var7', 'Var13 (or insert the Empty Raster)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('var8', 'Var14 (or insert the Empty Raster)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('var9', 'Var15 (or insert the Empty Raster)', defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(30, model_feedback)
        results = {}
        outputs = {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var5_',
            'INPUT_RASTER': parameters['var14'],
            'INPUT_VECTOR': parameters['trainingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var6_',
            'INPUT_RASTER': parameters['var15'],
            'INPUT_VECTOR': parameters['testingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [0,2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var15_',
            'INPUT_RASTER': parameters['var9'],
            'INPUT_VECTOR': parameters['trainingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var11_',
            'INPUT_RASTER': parameters['var5'],
            'INPUT_VECTOR': parameters['testingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var15_',
            'INPUT_RASTER': parameters['var9'],
            'INPUT_VECTOR': parameters['testingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var7_',
            'INPUT_RASTER': parameters['var16'],
            'INPUT_VECTOR': parameters['testingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var11_',
            'INPUT_RASTER': parameters['var5'],
            'INPUT_VECTOR': parameters['trainingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var12_',
            'INPUT_RASTER': parameters['var6'],
            'INPUT_VECTOR': parameters['trainingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var3_',
            'INPUT_RASTER': parameters['var12'],
            'INPUT_VECTOR': parameters['trainingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var6_',
            'INPUT_RASTER': parameters['var15'],
            'INPUT_VECTOR': parameters['trainingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var8_',
            'INPUT_RASTER': parameters['var17'],
            'INPUT_VECTOR': parameters['trainingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var1_',
            'INPUT_RASTER': parameters['var10'],
            'INPUT_VECTOR': parameters['trainingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var13_',
            'INPUT_RASTER': parameters['var7'],
            'INPUT_VECTOR': parameters['trainingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var14_',
            'INPUT_RASTER': parameters['var8'],
            'INPUT_VECTOR': parameters['testingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var9_',
            'INPUT_RASTER': parameters['var18'],
            'INPUT_VECTOR': parameters['testingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var4_',
            'INPUT_RASTER': parameters['var132'],
            'INPUT_VECTOR': parameters['trainingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var1_',
            'INPUT_RASTER': parameters['var10'],
            'INPUT_VECTOR': parameters['testingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var10_',
            'INPUT_RASTER': parameters['var42'],
            'INPUT_VECTOR': parameters['testingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var10_',
            'INPUT_RASTER': parameters['var42'],
            'INPUT_VECTOR': parameters['trainingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var9_',
            'INPUT_RASTER': parameters['var18'],
            'INPUT_VECTOR': parameters['trainingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var2_',
            'INPUT_RASTER': parameters['var11'],
            'INPUT_VECTOR': parameters['testingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var3_',
            'INPUT_RASTER': parameters['var12'],
            'INPUT_VECTOR': parameters['testingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var4_',
            'INPUT_RASTER': parameters['var132'],
            'INPUT_VECTOR': parameters['testingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var12_',
            'INPUT_RASTER': parameters['var6'],
            'INPUT_VECTOR': parameters['testingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var13_',
            'INPUT_RASTER': parameters['var7'],
            'INPUT_VECTOR': parameters['testingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var14_',
            'INPUT_RASTER': parameters['var8'],
            'INPUT_VECTOR': parameters['trainingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var8_',
            'INPUT_RASTER': parameters['var17'],
            'INPUT_VECTOR': parameters['testingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var2_',
            'INPUT_RASTER': parameters['var11'],
            'INPUT_VECTOR': parameters['trainingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var7_',
            'INPUT_RASTER': parameters['var16'],
            'INPUT_VECTOR': parameters['trainingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': 'Var5_',
            'INPUT_RASTER': parameters['var14'],
            'INPUT_VECTOR': parameters['testingzones10'],
            'RASTER_BAND': 1,
            'STATISTICS': [2,4,9]
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return '4.b. SU Extract conditioning factors values'

    def displayName(self):
        return '4.b. SU Extract conditioning factors values'

    def group(self):
        return 'SU (Slope Unit) analysis'

    def groupId(self):
        return 'SU (Slope Unit) analysis'

    def createInstance(self):
        return BSuExtractConditioningFactorsValues()
