
import subprocess
import time
import os 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
PATHFINDER_DIR = BASE_DIR / "docker" / "pathfinder"

def deploy_pathfinder(rpc_port: int):
    env = os.environ.copy()
    env["RPC_PORT"] = str(rpc_port)

    result = subprocess.run(
        ["docker", "compose", "up", "-d"],
        #cwd="docker/pathfinder",
        cwd=PATHFINDER_DIR,
        env=env,
        capture_output=True, text=True,
        check=True
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Docker compose failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )

    return True 

def destroy_pathfinder(rpc_port: int):
    env = os.environ.copy()
    env["RPC_PORT"] = str(rpc_port)

    subprocess.run(
        ["docker", "compose", "down", "-v"],
        #cwd="docker/pathfinder",
        cwd=PATHFINDER_DIR,
        env=env,
        check=True
    )

    return True

#poll docker health from celery task instead of hitting RPC immediately
def wait_for_container(container_name: str, timeout: int = 180):
    start_time = time.time()
    #while True:
        #result = subprocess.run(
        #    ["docker", "inspect", "--format='{{.State.Health.Status}}'", container_name],
        #    capture_output=True, text=True
        #)
        #status = result.stdout.strip().strip("'")
        #if status == "healthy":
        #    return True
        #elif time.time() - start_time > timeout:
        #    raise TimeoutError(f"Container {container_name} did not become healthy in time.")
        #time.sleep(5)
    while time.time() - start_time < timeout:
        status = subprocess.check_output(
            ["docker", "inspect", "--format='{{.State.Health.Status}}'", container_name]
        ).decode().strip()
        if status == "healthy": return True
        time.sleep(5)
    raise Exception(f"Container {container_name} did not become healthy in time.")