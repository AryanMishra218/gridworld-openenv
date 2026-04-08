from fastapi import FastAPI
from app.tasks import make_env
from app.models import StepRequest, StepResponse, ResetResponse



app = FastAPI()

env = {}

@app.get("/")
def root():
    return {"message": "Env is running"}


@app.post("/reset", response_model=ResetResponse)
def reset(task: str = "easy"):
    global env
    env = make_env(task)
    state = env.reset()
    return {
        "state": state,
        "info": {}
    }



@app.post("/step")
def step(req: StepRequest, task: str = "easy"):
    global env

    # If env not initialized → create it
    if env is None:
        env = make_env(task)
        state = env.reset()
        return {
            "state": state,
            "reward": 0.0,
            "terminated": False,
            "truncated": False,
            "info": {"warning": "Auto-reset applied"}
        }

    state, reward, done, truncated, _ = env.step(req.action)

    truncated = env.steps >= 100

    return {
        "state": state,
        "reward": reward,
        "terminated": done,
        "truncated": truncated,
        "info": {}
    }



@app.get("/state")
def get_state(task: str):
    env = envs.get(task)
    if env is None:
        return {
            "state": {},
            "reward": 0.0,
            "terminated": True,
            "truncated": True,
            "info": {"error": "Call /reset first"}
        }


    return {
        "state": env._get_state(),
        "info": {}
    }
