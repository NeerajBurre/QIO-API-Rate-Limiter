# Demo update: Verified QIO rate limiter logic for Jenkins CI/CD pipeline
# Rate limiter presentation update
# # CI/CD Demo Check: Verifying automated changelog generation
#DEVOPS
from fastapi import FastAPI, Request, HTTPException
import redis
import time
import numpy as np
import random

app = FastAPI()

# Redis connection
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# -----------------------------
# QIO CONFIG
# -----------------------------
LIMIT_RANGE = (50, 500)   # possible rate limits
POP_SIZE = 10             # number of candidate solutions

# Initialize probability population
q_population = np.random.uniform(LIMIT_RANGE[0], LIMIT_RANGE[1], POP_SIZE)

current_limit = 100  # initial default


# -----------------------------
# TRAFFIC METRICS
# -----------------------------
def get_metrics():
    total = int(r.get("total_requests") or 0)
    rejected = int(r.get("rejected_requests") or 0)

    if total == 0:
        return 1.0, 0.0

    success_rate = (total - rejected) / total
    drop_rate = rejected / total

    return success_rate, drop_rate


# -----------------------------
# FITNESS FUNCTION
# -----------------------------
def fitness(limit):
    success_rate, drop_rate = get_metrics()

    # Balanced objective
    return success_rate - drop_rate - (limit / 1000)


# -----------------------------
# QIO OPTIMIZER
# -----------------------------
def optimize_limit():
    global q_population, current_limit

    scores = []

    for candidate in q_population:
        score = fitness(candidate)
        scores.append(score)

    # Select best candidate
    best_idx = np.argmax(scores)
    best_limit = q_population[best_idx]

    # Quantum-inspired update (probabilistic shift)
    q_population = [
        candidate + random.uniform(-10, 10)
        for candidate in q_population
    ]

    # Keep within bounds
    q_population = np.clip(q_population, *LIMIT_RANGE)

    current_limit = int(best_limit)


# -----------------------------
# RATE LIMIT CHECK
# -----------------------------
def is_allowed(ip):
    key = f"rate:{ip}"

    count = r.get(key)

    if count is None:
        r.set(key, 1, ex=1)  # 1-second window
        return True

    if int(count) >= current_limit:
        r.incr("rejected_requests")
        return False

    r.incr(key)
    return True


# -----------------------------
# API ENDPOINT
# -----------------------------
@app.get("/api")
async def protected_api(request: Request):
    ip = request.client.host

    r.incr("total_requests")

    if not is_allowed(ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    return {"message": "Request successful", "limit": current_limit}


# -----------------------------
# BACKGROUND OPTIMIZER LOOP
# -----------------------------
@app.on_event("startup")
async def start_optimizer():
    import asyncio

    async def loop():
        while True:
            optimize_limit()
            await asyncio.sleep(1)  # real-time adjustment

    asyncio.create_task(loop())
