from typing import Dict
from .models import ServiceInfo
from datetime import datetime
import uuid
import time

services: Dict[str, ServiceInfo] = {}
deployments: Dict[str, dict] = {}

def add_service(service: ServiceInfo):
    services[service.service_name] = service

def get_services():
    return list(services.values())

def get_service(name: str):
    return services.get(name)

def trigger_deployment(service_name: str):
    build_id = str(uuid.uuid4())
    deployments[build_id] = {
        "service_name": service_name,
        "status": "QUEUED",
        "start_time": time.time()
    }
    return build_id

def update_deployment(build_id: str, status: str):
    if build_id in deployments:
        deployments[build_id]["status"] = status
