# Performance Metrics
from pureml_evaluate.metrics.accuracy.accuracy import Accuracy
from pureml_evaluate.metrics.precision.precision import Precision
from pureml_evaluate.metrics.recall.recall import Recall
from pureml_evaluate.metrics.f1_score.f1_score import F1
from pureml_evaluate.metrics.confusion_matrix.confusion_matrix import ConfusionMatrix
from pureml_evaluate.metrics.balanced_accuracy_score.balanced_accuracy_score import BalancedAccuracyScore
from pureml_evaluate.metrics.top_k_accuracy_score.top_k_accuracy_score import TopKAccuracyScore
from pureml_evaluate.metrics.log_loss.log_loss import LogLoss
from pureml_evaluate.metrics.roc_auc.roc_auc import ROC_AUC
from pureml_evaluate.metrics.average_precision_score.average_precision_score import AveragePrecisionScore
from pureml_evaluate.metrics.brier_score_loss.brier_score_loss import BrierScoreLoss

# Data Drift Metrics
from pureml_evaluate.metrics.kolmogorov_smirnov.kolmogorov_smirnov_statistic import KolmogorovSmirnov
from pureml_evaluate.metrics.wasserstein_distance.wasserstein_distance import WassersteinDistance
from pureml_evaluate.metrics.hellinger_distance.hellinger_distance import HellingerDistance
from pureml_evaluate.metrics.l_infinity_distance.l_infinity_distance import LInfinityDistance
from pureml_evaluate.metrics.chi_squared_statistic.chi_squared_statistic import ChiSquaredStatistic
from pureml_evaluate.metrics.cramers_v.cramers_v import CramersV
from pureml_evaluate.metrics.population_stability_index.population_stability_index import PopulationStabilityIndex

# Data Integrity Metrics
from pureml_evaluate.metrics.class_imbalance.class_imbalance import ClassImbalance
from pureml_evaluate.metrics.column_info.column_info import ColumnInfoCheck
from pureml_evaluate.metrics.conflicting_labels.conflicting_labels import ConflictingLabels
from pureml_evaluate.metrics.data_duplicates.data_duplicates import DataDuplicatesCheck
from pureml_evaluate.metrics.feature_feature_correlation.feature_feature_correlation import FeatureFeatureCorrelation
from pureml_evaluate.metrics.feature_label_correlation.feature_label_correlation import FeatureLabelCorrelation
from pureml_evaluate.metrics.identifier_label_correlation.identifier_label_correlation import IdentifierLabelCorrelation
from pureml_evaluate.metrics.is_single_value.is_single_value import IsSingleValue
from pureml_evaluate.metrics.mixed_data_types.mixed_data_types import MixedDataTypes
from pureml_evaluate.metrics.mixed_nulls.mixed_nulls import MixedNulls
from pureml_evaluate.metrics.outlier_sample_detection.outlier_sample_detection import OutlierSampleDetection
from pureml_evaluate.metrics.percent_of_nulls.percent_of_nulls import PercentOfNulls
from pureml_evaluate.metrics.special_character.special_character import SpecialCharacters
from pureml_evaluate.metrics.string_length_outOfBounds.string_length_outOfBounds import StringLengthOutOfBounds
from pureml_evaluate.metrics.string_mismatch.string_mismatch import StringMismatch


metrics_to_class_name = {
    'accuracy': Accuracy(),
    'precision': Precision(),
    'recall': Recall(),
    'f1': F1(),
    'confusionmatrix': ConfusionMatrix(),
    'balancedaccuracyScore': BalancedAccuracyScore(),
    'topkaccuracyscore': TopKAccuracyScore(),
    'logloss': LogLoss(),
    'averageprecisionscore': AveragePrecisionScore(),
    'roc_auc': ROC_AUC(),
    'brierscoreloss': BrierScoreLoss(),
    'kolmogorovsmirnov': KolmogorovSmirnov(),
    'wassersteindistance': WassersteinDistance(),
    'hellingerdistance': HellingerDistance(),
    'linfinitydistance': LInfinityDistance(),
    'chisquaredstatistic': ChiSquaredStatistic(),
    'cramersv': CramersV(),
    'populationstabilityindex': PopulationStabilityIndex()
}

data_metrics_to_class_name = {
    'classimbalance': ClassImbalance(),
    'columninfocheck': ColumnInfoCheck(),
    'conflictinglabels()': ConflictingLabels(),
    'dataduplicatescheck()': DataDuplicatesCheck(),
    'featurefeaturecorrelation()': FeatureFeatureCorrelation(),
    # 'FeatureLabelCorrelation()':FeatureLabelCorrelation(),
    # 'IdentifierLabelCorrelation()': IdentifierLabelCorrelation(),
    'issinglevalue()': IsSingleValue(),
    # 'MixedDataTypes()': MixedDataTypes(),
    'mixednulls()': MixedNulls(),
    # 'OutlierSampleDetection()': OutlierSampleDetection(),
    'percentofnulls()': PercentOfNulls(),
    'specialcharacters()': SpecialCharacters(),
    'stringlengthoutofbounds()': StringLengthOutOfBounds(),
    'stringmismatch()': StringMismatch()
}
