import uuid
from django.db import models

# Create your models here.

class StarknetNode(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("deploying", "Deploying"),
        ("running", "Running"),
        ("failed", "Failed"),
        ("stopped", "Stopped"),
    ]
    name = models.CharField(max_length=100)
    rpc_port = models.IntegerField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    container_id = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)


    def rpc_url(self):
        return f"http://localhost:{self.rpc_port}"