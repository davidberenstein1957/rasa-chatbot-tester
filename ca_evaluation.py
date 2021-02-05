import glob
import json
import os
import random
from itertools import product

import pandas as pd


def run():
    train_model = ["vanilla", "textattack", "transformer", "coco", "quora"]
    demo_type_list = ["financial-demo", "helpdesk-assistant", "wellness-check-bot", "pokedex-demo"][::-1]
    performance_dict = {"accuracy": [], "precision": [], "recall": [], "f1-score": []}
    total_output = []
    for demo_type in demo_type_list:
        base = os.path.join(demo_type, "results")
        # go to correct dir
        for combi in product(train_model, repeat=2):
            train, test = combi
            for idx in range(5):
                file_name = os.path.join(base, f"train_{train}_test_{test}_report_{idx}.json")
                with open(file_name) as json_file:
                    data = json.load(json_file)
                weighted_dict = data["weighted avg"]
                # performance_dict["accuracy"].append(data["accuracy"])
                performance_dict["precision"].append(weighted_dict["precision"])
                performance_dict["recall"].append(weighted_dict["recall"])
                performance_dict["f1-score"].append(weighted_dict["f1-score"])

            output = [
                # (sum(performance_dict["accuracy"]) / len(performance_dict["accuracy"])),
                (sum(performance_dict["precision"]) / len(performance_dict["precision"])),
                (sum(performance_dict["recall"]) / len(performance_dict["recall"])),
                (sum(performance_dict["f1-score"]) / len(performance_dict["f1-score"])),
            ]
            output = [round(entry, 4) for entry in output]
            output = [demo_type, train, test] + output
            total_output.append(output)
            # performance_dict["accuracy"] = []
            performance_dict["precision"] = []
            performance_dict["recall"] = []
            performance_dict["f1-score"] = []

    pd.DataFrame(total_output, columns=["demo", "train", "test", "precision", "recall", "f1-score"]).to_excel(
        "test.xlsx"
    )

    exit()


if __name__ == "__main__":
    run()
