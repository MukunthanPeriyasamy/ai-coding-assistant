from fastapi import FastAPI , HTTPException , status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from backend.services.tutor import ai_tutor, ai_beginner_tutor
from backend.database.db_config import init_db
from backend.models.user import UserCreate, UserLogin, Token
from backend.services.auth_service import register_user, authenticate_user
from backend.utils.auth_utils import create_access_token
from pydantic import BaseModel
import logging

# Initialize database
init_db()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Prompt(BaseModel):
    level: str = "advanced"
    prompt: str 
    session_id: str = "default"  # Session ID for conversation memory

@app.get("/")
def root():
    return {"message": "Welcome Esec AI Assistant"}

@app.post("/register")
def register(user: UserCreate):
    new_user = register_user(user)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    return new_user

@app.post("/login", response_model=Token)
def login(user_login: UserLogin):
    user = authenticate_user(user_login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/ai_tutor")
def ai_assitant(prompt:Prompt):
    if prompt.prompt is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Prompt is required")
    
    if prompt.level == "beginner":
        return StreamingResponse(ai_beginner_tutor(prompt.prompt, session_id=prompt.session_id), media_type="text/plain")
    elif prompt.level == "advanced":
        return StreamingResponse(ai_tutor(prompt.prompt, session_id=prompt.session_id), media_type="text/plain")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid level")
