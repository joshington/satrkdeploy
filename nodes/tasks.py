
from celery import shared_task
from .models import StarknetNode
from .services.docker import deploy_pathfinder
import time 
import requests

@shared_task(
    bind=True,autoretry_for=(Exception,), 
    retry_backoff=10, retry_kwargs={"max_retries":12}
)
def deploy_node_task(self, node_id):
    node = StarknetNode.objects.get(id=node_id)
    node.status = "deploying"
    node.save()

    #rpc_url = f"http://127.0.0.1:{node.rpc_port}"

    try:
        deploy_pathfinder(node.rpc_port)

        #wait for RPC
        for _ in range(20):
            try:
                r = requests.post(
                    f"http://localhost:{node.rpc_port}",
                    json={
                        "jsonrpc": "2.0",
                        "method": "starknet_chainId",
                        "params": [],
                        "id": 1,
                    },
                    timeout=3,
                )
                if r.status_code == 200:
                    node.status = "running"
                    node.save()
                    return
            except:
                time.sleep(5)
        raise Exception("RPC not ready")
    except Exception as e:
        node.status = "failed"
        node.save()
        raise e