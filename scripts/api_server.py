from fastapi import FastAPI
import subprocess

app = FastAPI()


@app.get("/run-demo")
def run_demo():
    result = subprocess.run(
        ["python", "run_demo_batch.py"],
        capture_output=True,
        text=True
    )

    return {
        "status": "demo pipeline executed",
        "output": result.stdout
    }


@app.get("/run-onboarding")
def run_onboarding():
    result = subprocess.run(
        ["python", "run_onboarding_batch.py"],
        capture_output=True,
        text=True
    )

    return {
        "status": "onboarding pipeline executed",
        "output": result.stdout
    }