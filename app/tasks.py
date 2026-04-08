from app.env import GridWorldEnv

def make_env(task: str):
    if task == "easy":
        return GridWorldEnv(task="easy")
    elif task == "medium":
        return GridWorldEnv(task="medium")
    elif task == "hard":
        return GridWorldEnv(task="hard")
    else:
        raise ValueError("Invalid task")