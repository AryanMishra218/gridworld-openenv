import os
import requests
import numpy as np

API_BASE_URL = os.getenv("API_BASE_URL")

tasks = ["easy", "medium", "hard"]

print("[START]")

for task in tasks:

    # Reset env
    res = requests.post(f"{API_BASE_URL}/reset", params={"task": task})

    if res.status_code != 200:
        print("[ERROR]", res.text)
        continue

    state = res.json()["state"]

    total_steps = 0
    reached_goal = False

    for step in range(100):

        action = np.random.randint(4)

        res = requests.post(
            f"{API_BASE_URL}/step",
            params={"task": task},
            json={"action": action}
        )

        # ✅ Safety check (VERY IMPORTANT)
        if res.status_code != 200:
            print("[ERROR]", res.text)
            break

        data = res.json()

        print(f"[STEP] task={task} step={step} action={action} reward={data['reward']}")

        state = data["state"]
        total_steps += 1

        # ✅ Handle BOTH cases
        if data["terminated"] or data["truncated"]:
            if data["terminated"]:
                reached_goal = True
            break

    print(f"[STEP] task={task} completed steps={total_steps}")

print("[END]")
