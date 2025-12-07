from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from database import get_db
from app.schemas import UserCreate,UserResponse,Token
from app import crud
from app.auth import create_access_token,authenticate_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


#====User Registration

@router.post("/register",response_model=UserResponse)
def register_user(user:UserCreate,db:Session=Depends(get_db)):
    existing_user  = crud.get_user_by_email(db,user.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email already used"
        )
    
    new_user = crud.create_user(db,user)
    return new_user


@router.post("/login",response_model=Token)
def login_user(user:UserCreate,db:Session=Depends(get_db)):

    auth_user=authenticate_user(db,user.email,user.password)

    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect email or password"
        )
    

    token = create_access_token({"user_id":auth_user.id})

    return {
        "access_token":token,
        "token_type":"bearer"
    }