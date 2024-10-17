import logging
from fastapi import FastAPI, Request, Depends, status
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from utils.email_service import send_email, EmailSchema
from utils.security import verify_token
from utils.logging_config import configure_logging

# Inicializar FastAPI
app = FastAPI()

# Configurar el limitador de solicitudes
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Configurar el logging
configure_logging()

# Manejar excepciones de Rate Limiting
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    logging.warning(f"Rate limit exceeded for IP: {request.client.host}")
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": {"message": "Too many requests, please try again later.", "status": status.HTTP_429_TOO_MANY_REQUESTS}}
    )

# Endpoint para enviar correos
@app.post("/send/")
@limiter.limit("2/minute")
async def send_email_endpoint(request: Request, email: EmailSchema, token: str = Depends(verify_token)):
    return await send_email(email)