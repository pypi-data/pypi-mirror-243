from report_generation import generate_report
import sys
import os
import warnings
import wandb
import argparse


print(os.environ)
wandb_key =  os.environ.get("wandbKey")
# print(wandb_key)
if not wandb_key:
    # API key is missing or empty
    warnings.warn("Warning: W&B API key is not set.")
else:
    # API key is present, so log in
    wandb.login(key=wandb_key)


parser = argparse.ArgumentParser(description='Take in inputs')
parser.add_argument('my_param', metavar='param', type=str, nargs=1,
                    help='The parameter you wish to log')
parser.add_argument('project_name', metavar='project name', type=str, nargs=1,
                    help='The name of the project')
parser.add_argument('entity_name', metavar='entity name', type=str, nargs=1,
                    help='The name of the entity who owns the project')

args = parser.parse_args()

# # Outdated
# # if len(sys.argv) != 4:
# #     print("Usage: python myscript.py parameter_name project_name entity_name")
# #     sys.exit(1)

# # # Get the parameter passed as a command-line argument
# # my_param = sys.argv[1]
# # project_name = sys.argv[2]
# # entity_name = sys.argv[3]

code = generate_report(args.my_param[0], args.project_name[0], args.entity_name[0])

if code == 0:
    print("Report generated!")
elif code == -1:
    print("Enter a valid parameter.")
    sys.exit(1)

