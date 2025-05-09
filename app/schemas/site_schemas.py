from pydantic import BaseModel, HttpUrl

class SiteRequest(BaseModel):
    url: str

class SiteResponse(BaseModel):
    url: str
    status: str
    response_time: float