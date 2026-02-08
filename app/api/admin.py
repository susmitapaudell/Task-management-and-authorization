from fastapi import APIRouter, Depends
from app.core.deps import require_admin

router = APIRouter(prefix="/admin")

@router.get("/ping")
def admin_ping(
    _ = Depends(require_admin)
):
    return {"status": "admin ok"}
