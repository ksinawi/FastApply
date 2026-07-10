from pydantic import BaseModel

class DownloadRequest(BaseModel):
    tailoredContent: str