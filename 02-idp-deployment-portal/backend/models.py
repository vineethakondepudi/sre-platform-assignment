from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RegisterServiceRequest(BaseModel):
    service_name: str
    team_name: str
    repo_url: str

class ServiceInfo(BaseModel):
    service_name: str
    team_name: str
    repo_url: str
    last_deployment_time: Optional[str] = None
    deployment_status: str = "NEVER_DEPLOYED"
