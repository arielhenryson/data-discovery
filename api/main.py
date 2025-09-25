from typing import Dict
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from auth import VerifyToken
from dotenv import load_dotenv

load_dotenv()

token_verifier = VerifyToken()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/public")
def public_endpoint():
    """
    This endpoint does not require authentication.
    """
    return {"message": "Hello from a public endpoint!"}


@app.get("/api/private")
def private_endpoint(token_payload: Dict = Depends(token_verifier.verify)):
    """
    This endpoint is protected and requires a valid Auth0 access token.
    """
    user_id = token_payload.get("sub")
    return {"message": f"Hello from a private endpoint! You are authenticated as user {user_id}."}
