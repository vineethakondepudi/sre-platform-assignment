from fastapi import FastAPI, HTTPException, BackgroundTasks
from datetime import datetime
import time

from .models import RegisterServiceRequest, ServiceInfo
from .store import add_service, get_services, get_service, trigger_deployment, update_deployment

app = FastAPI(title="IDP Deployment Portal")

@app.post("/register-service")
def register_service(req: RegisterServiceRequest):
    service = ServiceInfo(
        service_name=req.service_name,
        team_name=req.team_name,
        repo_url=req.repo_url
    )
    add_service(service)
    return {"message": "Service registered", "service": service}

def run_fake_pipeline(build_id: str):
    # Simulate CI job
    time.sleep(2)
    update_deployment(build_id, "RUNNING")
    time.sleep(3)
    update_deployment(build_id, "SUCCESS")

@app.post("/deploy/{service_name}")
def deploy_service(service_name: str, background_tasks: BackgroundTasks):
    service = get_service(service_name)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    build_id = trigger_deployment(service_name)
    background_tasks.add_task(run_fake_pipeline, build_id)

    service.last_deployment_time = datetime.utcnow().isoformat()
    service.deployment_status = "QUEUED"

    return {
        "build_id": build_id,
        "status": "QUEUED"
    }

@app.get("/health")
def health_dashboard():
    result = []
    for svc in get_services():
        result.append({
            "service_name": svc.service_name,
            "last_deployment_time": svc.last_deployment_time,
            "deployment_status": svc.deployment_status,
            "pod_count": 2,          # mocked
            "cpu": "120m",           # mocked
            "memory": "256Mi"        # mocked
        })
    return result
