from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class DevResponse(BaseModel):
    statusCode: int = Field(200, ge=200, le=599)
    result: Optional[Dict[str, Any]] = None
