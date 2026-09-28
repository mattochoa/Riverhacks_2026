from prefect import flow, task
from datetime import datetime

@task
def hello():
    print(f"Prefect worker executed this at {datetime.now().isoformat()}")
    return "success"

@flow(log_prints=True)
def prefect_smoke_test():
    result = hello()
    print(f"Result: {result}")

if __name__ == "__main__":
    prefect_smoke_test()
