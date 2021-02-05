import glob
import os
import random
import re
from itertools import product


def run():
    train_model = ["vanilla", "textattack", "transformer", "coco", "quora"]
    demo_type_list = ["financial-demo", "helpdesk-assistant", "wellness-check-bot", "pokedex-demo"]
    demo_type_list = ["financial-demo"]
    dict_of_data_dicts = {}

    for model in train_model:
        dict_of_data_dicts[model] = create_data_dict(model)

    for demo_type in demo_type_list:
        # go to correct dir
        os.chdir(demo_type)
        for combi in product(train_model, repeat=2):
            for idx in range(5):
                # split original data
                os.system("rasa data split nlu --training-fraction 0.8")

                # update data for specific test set-up
                train, test = combi
                if train == "vanilla" and test != train:
                    train_dict, test_dict = dict_of_data_dicts[train], dict_of_data_dicts[test]
                    update_train_test_data(train_dict, "training")
                    update_train_test_data(test_dict, "test")

                    # strart training with specific data
                    os.system("rasa train --data train_test_split/training_data_2.md")

                    # strart testing with specific data
                    os.system("rasa test nlu --nlu train_test_split/test_data_2.md")

                    # rename outcome to idx and
                    base = os.path.join(os.getcwd(), "results")
                    old_name = os.path.join(base, "intent_report.json")
                    new_name = os.path.join(base, f"train_{train}_test_{test}_report_{idx}.json")
                    os.rename(old_name, new_name)

                    # delete previous model
                    files = glob.glob("models/*")
                    for f in files:
                        os.remove(f)

        # go back to main dir
        os.chdir("..")


def create_data_dict(model_type):
    data_dict = {}
    if model_type == "vanilla":
        return data_dict
    else:
        f = open(f"gen_{model_type}.txt")
        intent = ""
        for line in f.readlines():
            if "## intent:" in line:
                intent = line.split(":")[-1].strip()
                if intent not in data_dict:
                    data_dict[intent] = []
            else:
                if line.strip() != "":
                    if "_" not in line:
                        data_dict[intent].append(line.strip())

    return data_dict


def update_train_test_data(data_dict, tt_type="training"):
    file_path_old = os.path.join(os.getcwd(), "train_test_split", f"{tt_type}_data.md")
    file_path_new = os.path.join(os.getcwd(), "train_test_split", f"{tt_type}_data_2.md")
    with open(file_path_old, "r") as f:
        lines = list(f)
    added = None
    if tt_type == "training":
        n_samples = 3
    else:
        n_samples = 1
    with open(file_path_new, "w") as output_file:
        for line in lines:
            if "## intent" in line:
                output_file.write(line)
                added = set()
            else:
                line = line.strip().replace("- ", "")
                line = re.sub(r"\([^)]*\)", "", line).replace("[", "").replace("]", "")
                line = re.sub(r"{.*?}", "", line).replace("{", "").replace("}", "")

                if line in data_dict:
                    for i in range(n_samples):
                        option = random.choice(data_dict[line])
                        if option not in added:
                            output_file.write("- " + option + "\n")
                            added.add(option)

                    if tt_type == "training":
                        if line != "":
                            output_file.write("- " + line + "\n")
                        else:
                            output_file.write("\n")
                else:
                    if line != "":
                        output_file.write("- " + line + "\n")
                    else:
                        output_file.write("\n")


if __name__ == "__main__":
    run()
