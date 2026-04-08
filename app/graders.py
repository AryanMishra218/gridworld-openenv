def normalize_steps(steps, max_steps):
    return max(0.0, min(1.0, 1 - steps / max_steps))


def grade_easy(steps, reached_goal):
    step_score = normalize_steps(steps, 50)
    score = (0.7 if reached_goal else 0.2) + step_score * 0.3
    return max(0.0, min(1.0, score))


def grade_medium(reached_goal, steps):
    step_score = normalize_steps(steps, 70)
    score = (0.6 if reached_goal else 0.1) + step_score * 0.4
    return max(0.0, min(1.0, score))


def grade_hard(reached_goal, survival_steps):
    survival_score = min(survival_steps / 100, 1.0)
    score = (0.5 if reached_goal else 0.1) + survival_score * 0.5
    return max(0.0, min(1.0, score))