
import subprocess
import os 


def deploy_pathfinder(rpc_port: int):
    env = os.environ.copy()
    env["RPC_PORT"] = str(rpc_port)

    result = subprocess.run(
        ["docker-compose", "up", "-d"],
        cwd="docker/pathfinder",
        env=env,
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return True 

def destroy_pathfinder(rpc_port: int):
    env = os.environ.copy()
    env["RPC_PORT"] = str(rpc_port)

    subprocess.run(
        ["docker-compose", "down", "-v"],
        cwd="docker/pathfinder",
        env=env,
    )