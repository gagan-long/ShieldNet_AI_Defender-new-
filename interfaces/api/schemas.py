from pydantic import BaseModel

class PhishingRequest(BaseModel):
    text: str
    metadata: dict = {}

class DetectionResult(BaseModel):
    is_malicious: bool
    confidence: float
    threat_type: str
