import argparse
import sys
import os

# parser = argparse.ArgumentParser()
# parser.add_argument("category")
# parser.add_argument("subcommand-args")
# args = parser.parse_args()
args = sys.argv

# remove "command.py"
args = args[1:]

# print(args)
subcommand = args[0].lower()

subcommand_args = " ".join(args[1:])
if subcommand=="data":
    command = "py src/data/make_dataset.py "+subcommand_args
    # print(command)
    os.system(command)
else:
    print("subcommand not supported.")

# os.system("py src/__init__.py")
"""
download the dataset:                 data download
preprocess dataset:                   data prepare
visualize dataset:                    data show
delete raw & interim dataset dir:     data delete --cache
delete all dataset dir:               data delete --all


train model:                          model train
evaluate model:                       model evaluate
inference with model:                 model predict --image test.jpg --folder images/ -d results/



"""