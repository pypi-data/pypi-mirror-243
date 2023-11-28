from raga import *
import datetime
from raga.test_config import labelling_quality_test
run_name = f"poc-test-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", run_name= run_name, profile="dev")

dataset_name = "policy_bazaar_train_dataset"

edge_case_detection = labelling_quality_test(test_session=test_session,
                                             dataset_name = dataset_name,
                                             test_name = "pb_labelling_quality_2",
                                             trainModelColumnName = "target",
                                             fieldModelColumnName = "target",
                                             type = "labelling_consistency",
                                             output_type="embedding_data",
                                             embeddingTrainColName = "embedding",
                                             embeddingFieldColName = "embedding",
                                             rules = rules)



