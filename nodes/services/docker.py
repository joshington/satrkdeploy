
import subprocess
import os 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
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
        raise RuntimeError(result.stderr)
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