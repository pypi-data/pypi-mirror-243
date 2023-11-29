import wandb
import subprocess

def log(data, my_param, project_name, curr_date, num_steps): 
    git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")
    wandb.init(
        # Set the project where this run will be logged
        project=project_name, 
        # We pass a run name (otherwise it’ll be randomly assigned, like sunshine-lollypop-10)
        name=f"{curr_date} - experiment_{my_param}", 
        # Track hyperparameters and run metadata
        config={
        "learning_rate": 0.02,
        "architecture": "CNN",
        "dataset": "CIFAR-100",
        "epochs": 10,
        "steps" : 1000,
        "date": curr_date,
        "git_commit": git_commit,

        })

    steps = num_steps
    for step in range(steps):
        wandb.log({f"{my_param}": (data[my_param])[step]})

    wandb.finish()



