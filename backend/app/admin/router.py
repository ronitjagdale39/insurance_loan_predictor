from packaging import tags
from fastapi import FastAPI,HTTPException,Depends,APIRouter
from app.auth.dependencies import get_current_user,role_required
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User
router=APIRouter(prefix='/admin',tags=['admin'])

@router.get('/dashboard')
def dashboard(current_user=Depends(role_required(['admin']))):
    return {
        "user":f'welcome admin {current_user.name}'
        
    }
@router.get('/get_users')
def get_users(Users=Depends(role_required(['admin'])),db:Session=Depends(get_db)):
    all_users=db.query(User).count()
    return {
        "all users":all_users
    }
@router.get('/pending_users')
def pending_users(Users=Depends(role_required(['admin'])),db:Session=Depends(get_db)):
    pending_users=db.query(User).filter(User.is_verified==False).count()
    return {
        "pending users":pending_users
    }
    