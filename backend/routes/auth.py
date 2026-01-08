from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.database import get_db
from backend.schemas.user import UserCreate, UserResponse, Token
from backend.core.security import get_password_hash, verify_password
from backend.auth.jwt import create_access_token
from backend.auth.dependencies import get_current_user
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Register a new user in MongoDB."""
    existing_user = await db.users.find_one({"username": user_in.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    new_user_dict = {
        "username": user_in.username,
        "password_hash": get_password_hash(user_in.password),
        "created_at": datetime.utcnow()
    }
    
    result = await db.users.insert_one(new_user_dict)
    new_user_dict["_id"] = str(result.inserted_id)
    
    # Sync with Firebase Firestore (Optional)
    try:
        from backend.services.firebase_service import FirebaseService
        FirebaseService.save_document("users", f"user_{result.inserted_id}", {
            "username": new_user_dict["username"],
            "mongo_id": str(result.inserted_id),
            "created_at": new_user_dict["created_at"].isoformat()
        })
    except Exception as e:
        print(f"Warning: Failed to sync user to Firebase: {e}")
        
    return new_user_dict

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncIOMotorDatabase = Depends(get_db)):
    """Login and get an access token."""
    user = await db.users.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """Get the profile of the current authenticated user."""
    return current_user
