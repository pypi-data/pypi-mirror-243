from typing import Optional, Union
from raga import TestSession, ModelABTestRules, FMARules, LQRules, EventABTestRules, Filter, OcrRules, OcrAnomalyRules
    
class TestConfig:
    def __init__(self, 
                 test_session: TestSession, 
                 dataset_name: str, 
                 test_name: str,
                 model: str, 
                 type: str,
                 output_type: str, 
                 rules: Union[ModelABTestRules, EventABTestRules, FMARules, LQRules, OcrRules, OcrAnomalyRules],
                 aggregation_level: Optional[list] = None, 
                 filter_obj: Optional[Filter] = None,
                 gt: Optional[str] = "", 
                 clustering: Optional[Union[dict, int]] = None,
                 object_detection_modelA: Optional[str] = "", 
                 object_detection_modelB: Optional[str] = "",
                 object_detection_model: Optional[str] = "", 
                 object_detection_gt: Optional[str] = "",
                 embedding_col_name: Optional[str] = "", 
                 embedding_train_col_name: Optional[str] = "",
                 embedding_field_col_name: Optional[str] = "", 
                 train_model_col_name: Optional[str] = "",
                 field_model_col_name: Optional[str] = "", 
                 mistake_score_col_name: Optional[str] = ""):

        self.test_session = self.validate_argument(test_session, "test_session", TestSession)
        self.dataset_name = self.validate_argument(dataset_name, "dataset_name", str)
        self.test_name = self.validate_argument(test_name, "test_name", str)
        self.model = self.validate_argument(model, "model", str)
        self.type = self.validate_argument(type, "type", str)
        self.output_type = self.validate_argument(output_type, "output_type", str)
        self.rules = self.validate_argument(rules, "rules", (ModelABTestRules, EventABTestRules, FMARules, LQRules, OcrRules, OcrAnomalyRules))
        
        self.aggregation_level = self.validate_argument(aggregation_level, "aggregation_level", list, default=[])
        self.filter_obj = self.validate_argument(filter_obj, "filter_obj", Filter, default=None)
        self.gt = self.validate_argument(gt, "gt", str, default="")
        self.clustering = self.validate_argument(clustering, "clustering", (dict, int), default=None)
        self.object_detection_modelA = self.validate_argument(object_detection_modelA, "object_detection_modelA", str, default="")
        self.object_detection_modelB = self.validate_argument(object_detection_modelB, "object_detection_modelB", str, default="")
        self.object_detection_model = self.validate_argument(object_detection_model, "object_detection_model", str, default="")
        self.object_detection_gt = self.validate_argument(object_detection_gt, "object_detection_gt", str, default="")
        self.embedding_col_name = self.validate_argument(embedding_col_name, "embedding_col_name", str, default="")
        self.embedding_train_col_name = self.validate_argument(embedding_train_col_name, "embedding_train_col_name", str, default="")
        self.embedding_field_col_name = self.validate_argument(embedding_field_col_name, "embedding_field_col_name", str, default="")
        self.train_model_col_name = self.validate_argument(train_model_col_name, "train_model_col_name", str, default="")
        self.field_model_col_name = self.validate_argument(field_model_col_name, "field_model_col_name", str, default="")
        self.mistake_score_col_name = self.validate_argument(mistake_score_col_name, "mistake_score_col_name", str, default="")

    @staticmethod
    def validate_argument(value, name, expected_type, default=None):
        if value is None:
            return default
        if not isinstance(value, expected_type):
            raise ValueError(f"{name} must be of type {expected_type}")
        return value

    def construct_payload(self):
        payload = {
            "datasetId": self.dataset_id,
            "experimentId": self.test_session.experiment_id,
            "name": self.test_name,
            "model": self.model,
            "type": self.type,
            "outputType": self.output_type,
            "rules": self.rules.get(),
            "aggregationLevels": self.aggregation_level,
            'filter': self.filter_obj.get() if self.filter_obj else "",
            'gt': self.gt,
            'test_type': self.get_test_type()
        }

        if self.clustering:
            if isinstance(self.clustering, int):
                payload['clusterId'] = self.clustering
            else:
                payload['clustering'] = self.clustering

        self.update_payload_specific_fields(payload)

        return payload

    def update_payload_specific_fields(self, payload):
        pass

    def get_test_type(self):
        pass

    def run_validation(self):
        self.dataset_id = self.validate_dataset()
        self.validate_specific_arguments()

    def validate_dataset(self):
        res_data = self.test_session.http_client.get(f"api/dataset?projectId={self.test_session.project_id}&name={self.dataset_name}",
                                                     headers={"Authorization": f'Bearer {self.test_session.token}'})
        if not isinstance(res_data, dict):
            raise ValueError("Invalid response")
        dataset_id = res_data.get("data", {}).get("id")
        if not dataset_id:
            raise KeyError("Invalid response data")
        return dataset_id

    def validate_specific_arguments(self):
        pass


class ModelABTestConfig(TestConfig):
    def update_payload_specific_fields(self, payload):
        pass

    def validate_specific_arguments(self):
        pass


class EventABTestConfig(TestConfig):
    def update_payload_specific_fields(self, payload):
        payload['objectDetectionModelA'] = self.object_detection_modelA
        payload['objectDetectionModelB'] = self.object_detection_modelB


    def validate_specific_arguments(self):
        pass


class FMATestConfig(TestConfig):
    def update_payload_specific_fields(self, payload):
        pass

    def validate_specific_arguments(self):
        pass


class LQTestConfig(TestConfig):
    def update_payload_specific_fields(self, payload):
        fields_to_update = [
            ("embeddingColName", self.embedding_col_name),
            ("embeddingTrainColName", self.embedding_train_col_name),
            ("embeddingFieldColName", self.embedding_field_col_name),
            ("trainModelColumnName", self.train_model_col_name),
            ("fieldModelColumnName", self.field_model_col_name),
        ]

        for field_name, field_value in fields_to_update:
            if field_value is not None and field_value != "":
                payload[field_name] = field_value
        

    def validate_specific_arguments(self):
        pass


class OCROrAnomalyTestConfig(TestConfig):
    def update_payload_specific_fields(self, payload):
        pass    

    def validate_specific_arguments(self):
        pass


def labelling_quality_test(test_session: TestSession, 
                           dataset_name: str, 
                           test_name: str, 
                           type: str,
                           output_type: str, 
                           mistake_score_col_name: str, 
                           rules: LQRules):
    
    config = LQTestConfig(test_session, 
                          dataset_name, 
                          test_name, 
                          type, 
                          output_type,
                          mistake_score_col_name, 
                          rules)
    config.run_validation()
    return config.construct_payload()