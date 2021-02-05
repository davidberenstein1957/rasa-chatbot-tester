# rasa-chatbot-tester

rasa data split nlu --training-fraction 0.75
rasa train --data train_test_split/training_data.md
rasa test nlu --nlu train_test_split/test_data.md

