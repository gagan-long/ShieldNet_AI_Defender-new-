from fastapi import FastAPI, Request, Depends
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from config import ConfigLoader

# Import schemas and core logic
from ..core.phishing_detection import analyze_text
from .schemas import PhishingRequest, DetectionResult

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error handler for rate limiting
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests - 5 requests per minute allowed"}
    )

@app.post("/analyze", response_model=DetectionResult)
@limiter.limit("5/minute")
async def analyze_phishing(request: Request, data: PhishingRequest):
    result = analyze_text(data.text)
    return {
        "is_malicious": result["malicious"],
        "confidence": result["confidence"],
        "threat_type": result["threat_type"]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Attach limiter to app instance
app.state.limiter = limiter

api_config = ConfigLoader().load_api_config()

app = FastAPI()
app.state.rate_limit = api_config['security']['rate_limits']['api']


@app.get("/config/health")
async def config_health():
    try:
        validate_config(ConfigLoader().load_api_config())
        return {"status": "valid"}
    except Exception as e:
        raise HTTPException(500, str(e))
