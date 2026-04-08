---
title: Gridworld Openenv
emoji: 🐠
colorFrom: green
colorTo: purple
sdk: docker
pinned: false
license: mit
short_description: RL GridWorld environment API (OpenEnv ready)
---

# 🚀 Autonomous Navigation RL Environment (OpenEnv Compatible)

A lightweight, API-driven Reinforcement Learning environment that simulates robot navigation in a 2D GridWorld with obstacles, traps, and dynamic challenges.

---

## 🧠 Overview

This project implements a GridWorld environment where an agent must navigate from a start position to a goal while avoiding hazards and penalties.

### Environment Elements

- 🟫 **Obstacles** — Block movement  
- ⚠️ **Traps** — Penalize the agent  
- 👾 **Enemy (Hard Mode)** — Introduces dynamic difficulty  

The environment is exposed via a **FastAPI interface** and is fully **Dockerized** for easy deployment.

---

## 🎯 Features

- ✅ OpenEnv-compliant API  
- ✅ Three difficulty levels: **easy, medium, hard**  
- ✅ Reward normalization (`0.0 → 1.0`)  
- ✅ Fully Dockerized setup  
- ✅ Lightweight and CPU-friendly  
- ✅ Inference script for evaluation  
- ✅ Stable API with no validation errors  

---

## 🎮 Action Space

| Action | Meaning |
|--------|--------|
| `0` | Up |
| `1` | Down |
| `2` | Left |
| `3` | Right |

---

## 🧮 Reward System

The reward function is designed to guide efficient navigation:

- ➖ Step penalty (encourages shorter paths)  
- 📏 Distance-based reward shaping  
- ⚠️ Trap penalty  
- 👾 Enemy penalty (hard mode)  
- 🏁 Goal reward  

👉 Final reward is **normalized to `[0, 1]`**

---

## 🌐 API Endpoints

### 🔹 Reset Environment

```

POST /reset?task=easy

```

**Query Params:**
- `task`: `easy | medium | hard`

---

### 🔹 Take a Step

```

POST /step

````

**Request Body:**
```json
{
  "action": 1
}
````

**Response:**

```json
{
  "state": [x, y],
  "reward": 0.85,
  "done": false
}
```

---

### 🔹 Get Current State

```
GET /state
```

---

## 🧪 Inference

Run the evaluation script:

```bash
python inference.py
```

### Output Format

```
[START]
[STEP] action=...
[STEP] action=...
[END]
```

---

## 🐳 Docker Setup

### Build Image

```bash
docker build -t env-test .
```

### Run Container

```bash
docker run -p 7860:7860 env-test
```

The API will be available at:

```
http://localhost:7860
```

---

## 📁 Project Structure

```
app/
  ├── api.py        # FastAPI routes
  ├── env.py        # Core environment logic
  ├── models.py     # Data models (request/response)
  ├── tasks.py      # Task configurations
  ├── graders.py    # Evaluation logic

inference.py        # Agent interaction script
Dockerfile          # Container configuration
requirements.txt    # Dependencies
openenv.yaml        # OpenEnv specification
LICENSE
```

---

## 📊 Tasks

| Difficulty | Description           |
| ---------- | --------------------- |
| 🟢 Easy    | Fewer obstacles       |
| 🟡 Medium  | More traps            |
| 🔴 Hard    | Enemy + dense hazards |

---

## ⚙️ State Representation

* Format: `[x, y]`
* Represents agent position in the grid
* Fully compliant with OpenEnv expectations

---

## ✅ Submission Ready

* ✔ Correct state format
* ✔ Normalized rewards
* ✔ Stable API responses
* ✔ No validation errors

🎉 This environment is **fully evaluator-ready**.

---

## 📜 License

This project is released under the MIT License.

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference