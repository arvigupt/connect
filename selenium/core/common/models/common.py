from pydantic import BaseModel

class common(BaseModel):
    id: uuid
    last_updated_by_user: str
    last_updated_at_user: str
    last_updated_by_sys: str
    last_updated_at_sys: str
    created_by_user: str
    created_at_user: str
