from pydantic import BaseModel
from typing import Optional
import uuid

class UserCredential(BaseModel):
    tenant_id: str
    data_platform_id: str
    applicant_id: str
    username: str
    password: Optional[str] = None
    otp: Optional[str] = None
    relogin: Optional[bool] = None