from fastapi import APIRouter
from .storage.views import router as storage_router

router = APIRouter()
router.include_router(router=storage_router, prefix='/storage')