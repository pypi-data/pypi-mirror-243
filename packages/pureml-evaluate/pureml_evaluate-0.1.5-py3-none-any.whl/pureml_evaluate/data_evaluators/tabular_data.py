from pureml_evaluate.data_metrics.tabular.class_imbalance import ClassImbalance
from pureml_evaluate.data_metrics.tabular.column_info import ColumnInfoCheck
from pureml_evaluate.data_metrics.tabular.conflicting_labels import ConflictingLabels
from pureml_evaluate.data_metrics.tabular.data_duplicates import DataDuplicatesCheck
from pureml_evaluate.data_metrics.tabular.feature_feature_correlation import FeatureFeatureCorrelation
from pureml_evaluate.data_metrics.tabular.feature_label_correlation import FeatureLabelCorrelation
from pureml_evaluate.data_metrics.tabular.identifier_label_correlation import IdentifierLabelCorrelation
from pureml_evaluate.data_metrics.tabular.is_single_value import IsSingleValue
from pureml_evaluate.data_metrics.tabular.mixed_data_types import MixedDataTypes
from pureml_evaluate.data_metrics.tabular.mixed_nulls import MixedNulls
from pureml_evaluate.data_metrics.tabular.outlier_sample_detection import OutlierSampleDetection
from pureml_evaluate.data_metrics.tabular.percent_of_nulls import PercentOfNulls
from pureml_evaluate.data_metrics.tabular.special_character import SpecialCharacters
from pureml_evaluate.data_metrics.tabular.string_length_outOfBounds import StringLengthOutOfBounds
from pureml_evaluate.data_metrics.tabular.string_mismatch import StringMismatch



class Tabular:
    def __init__(self):
        self.task_type = "tabular"

        self.data = None

        self.metrics = [
            ClassImbalance(),
            ColumnInfoCheck(),
            ConflictingLabels(),
            DataDuplicatesCheck(),
            FeatureFeatureCorrelation(),
            #FeatureLabelCorrelation(),                            
            #IdentifierLabelCorrelation(),
            IsSingleValue(),
            #MixedDataTypes(),
            MixedNulls(),
            #OutlierSampleDetection(),
            PercentOfNulls(),
            SpecialCharacters(),
            StringLengthOutOfBounds(),
            StringMismatch()
          ]
        self.scores = {}

        # Need to check Featurelabelcorrelation and IdentifierLabelCorrelation and MixedDataTypes and OutlinerSampleDetection
    def compute(self):
    
        for m in self.metrics:
    
            try:
                score = m.compute(data = self.data)

                self.scores.update(score)
            except Exception as e:
                print("Unable to compute", m)
                print(f"Exception: {e}")

        return self.scores

    