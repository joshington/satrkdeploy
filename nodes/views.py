import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render,redirect, get_object_or_404
from .services.docker import destroy_pathfinder
from .models import StarknetNode
from .tasks import deploy_node_task
import random 


@csrf_exempt
def rpc_proxy(request, token):
    try:
        node = StarknetNode.objects.get(access_token=token, status="running")
    except StarknetNode.DoesNotExist:
        return JsonResponse({"error":"Node not found"}, status=404)
    
    response = requests.post(
        f"http://localhost:{node.rpc_port}",
        data=request.body,
        headers={"Content-Type": "application/json"}, timeout=10
    )
    return JsonResponse(response.json(), safe=False)


def dashboard(request):
    nodes = StarknetNode.objects.all()
    return render(request, "nodes/dashboard.html", {"nodes": nodes})


# Create your views here.
def deploy_node(request):
    port = random.randint(20000, 30000)

    node = StarknetNode.objects.create(
        name="Sepolia Node",
        rpc_port=port,
        status="pending"
    )

    deploy_node_task.delay(node.id)
    return redirect("nodes:dashboard")



def destroy_node(request, node_id):
    if request.method == "POST":
        node = get_object_or_404(StarknetNode, id=node_id)

        try:
            destroy_pathfinder(node.rpc_port)
        except Exception:
            pass  # PoC: ignore infra errors

        node.delete()

    return redirect("nodes:dashboard")
