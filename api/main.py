from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt, JWTError
from pydantic import BaseModel
import requests
from functools import lru_cache
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Auth0 Configuration ---
# These values are loaded from your .env file.
# Make sure they match the settings in your Auth0 Dashboard.
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("API_AUDIENCE")
# Auth0 uses the RS256 algorithm for signing tokens.
ALGORITHM = ["RS256"]
ISSUER = f"https://{AUTH0_DOMAIN}/"

# --- Pydantic Models ---


class User(BaseModel):
    """Represents the user information extracted from the JWT."""
    id: str  # This corresponds to the 'sub' (subject) claim in the token
    permissions: list[str] = []

# --- Authentication & Authorization ---


# This dependency extracts the token from the "Authorization: Bearer <token>" header.
# auto_error=False means it will return None if the header is missing,
# allowing us to handle it gracefully in the dependency.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


@lru_cache(maxsize=1)
def get_jwks():
    """
    Fetches the JSON Web Key Set (JWKS) from Auth0.

    The lru_cache decorator caches the result, so we don't need to make a network
    request for the signing keys every time a token needs to be validated.
    This significantly improves performance.
    """
    if not AUTH0_DOMAIN:
        raise HTTPException(
            status_code=500, detail="AUTH0_DOMAIN is not configured in environment variables.")

    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    try:
        response = requests.get(jwks_url, timeout=10)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while fetching JWKS: {http_err}")
        # This error is often due to an incorrect AUTH0_DOMAIN.
        raise HTTPException(
            status_code=503, detail="Could not fetch signing keys from authentication provider.")
    except requests.exceptions.RequestException as req_err:
        print(f"Request exception occurred while fetching JWKS: {req_err}")
        # This could be a network, DNS, or timeout issue.
        raise HTTPException(
            status_code=503, detail="Network error connecting to authentication provider.")
    except ValueError:  # Catches JSON decoding errors
        print("Failed to decode JWKS JSON from Auth0.")
        raise HTTPException(
            status_code=500, detail="Invalid key format from authentication provider.")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency to validate the Auth0 JWT and return the user's info.
    This function performs the following steps:
    1. Checks for the presence of an Authorization header.
    2. Fetches the correct public signing key from Auth0's JWKS endpoint.
    3. Decodes and validates the JWT's signature and claims (like audience and issuer).
    4. Extracts user information and returns it as a Pydantic model.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token is None:
        # This happens if the Authorization header is missing.
        raise credentials_exception

    try:
        # Step 1: Get the signing keys from Auth0
        jwks = get_jwks()

        # Step 2: Get the unverified header to find the correct key ID ('kid')
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}

        if "kid" not in unverified_header:
            raise HTTPException(
                status_code=401, detail="Token is missing 'kid' in header.")

        for key in jws["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                break

        if not rsa_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to find the appropriate signing key.",
            )

        # Step 3: Decode and validate the token
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHM,
            audience=API_AUDIENCE,
            issuer=ISSUER,
        )

        # Step 4: Extract user info and return
        user_id = payload.get("sub")
        permissions = payload.get("permissions", [])
        if user_id is None:
            raise credentials_exception

        return User(id=user_id, permissions=permissions)

    except JWTError as e:
        # This is the key change: we now return the specific JWT error message.
        # This will tell you if the token is expired, has an invalid audience, etc.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation error: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException as e:
        # Re-raise HTTPExceptions from get_jwks or this function
        raise e
    except Exception as e:
        # Log any other unexpected errors for debugging
        print(f"An unexpected error occurred during token validation: {e}")
        raise credentials_exception

# --- FastAPI App Initialization ---
app = FastAPI(
    title="FastAPI Auth0 Example",
    description="An example of integrating Auth0 for authentication in a FastAPI application."
)

# --- CORS Middleware ---
# In production, you should restrict this to your frontend's actual origin.
# For example: origins = ["https://your-frontend-app.com"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---


@app.get("/")
def read_root():
    """A public endpoint that does not require authentication."""
    return {"message": "This is a public endpoint. Anyone can access it."}


@app.get("/test", response_model=User)
async def read_protected_test_route(current_user: User = Depends(get_current_user)):
    """
    A protected endpoint that requires a valid Auth0 JWT.

    The client must provide a token from Auth0 in the Authorization header.
    Format: 'Authorization: Bearer <your_auth0_token>'

    If the token is valid, this returns the user's ID and permissions.
    """
    return current_user
