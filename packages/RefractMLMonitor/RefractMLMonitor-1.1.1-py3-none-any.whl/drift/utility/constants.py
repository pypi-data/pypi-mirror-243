from email import parser
from typing import Final
import configparser

parser = configparser.ConfigParser()
parser.read('utility/properties.ini')

class DataType:
    TABULAR_DATA: Final = "Tabular"
    TEXT_DATA: Final = "Text"
    IMAGE_DATA: Final = "Image"
    VIDEO_DATA: Final = "Video"
    AUDIO_DATA: Final = "Audio"

class DriftType:
    FEATURE_DRIFT: Final = 'feature_drift'
    LABEL_DRIFT: Final = 'label_drift'
    MODEL_PERFORMANCE_DRIFT: Final = 'model_performance_drift'
    PREDICTION_DRIFT: Final = 'prediction_drift'
    CONCEPT_DRIFT: Final = 'concept_drift'

class ProblemType:
    BINARY_CLASSIFICATION: Final = 'Binary Classification'
    MULTICLASS_CLASSIFICATION: Final = 'Multiclass Classification'
    MULTI_LABEL_CLASSIFICATION: Final = 'Multilabel Classification'
    REGRESSION: Final = 'Regression'

class DataConnector:
    SNOWFLAKE: Final = 'snowflake'
    REFRACT_DATASETS: Final ='refract datasets'
    REFRACT_LOCAL_FILES: Final  = 'local data files'
    REFRACT_FILE: Final = 'refract'

class Constants:
    max_row_count=parser['constants']['max_row_count']

