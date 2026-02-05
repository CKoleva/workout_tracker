from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.authz import require_admin
from app.db.deps import get_db
from app.db.repositories.user import list_users
from app.schemas.user import UserRead

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserRead])
def get_users(
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    return list_users(db)