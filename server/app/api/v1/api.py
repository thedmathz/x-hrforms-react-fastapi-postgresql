from fastapi import APIRouter
from app.api.v1.endpoints import (
    starter,
    register,
    forgot_password,
    authentication,
    my_profile,
    change_password,
    dashboard,
    my_applications,
    for_approvals,
    offices,
    positions,
    users,
    user_types,
)

api_router = APIRouter()

api_router.include_router(starter.router, prefix="/starter", tags=["Starter"])
# api_router.include_router(register.router, prefix="/register", tags=["Register"])
# api_router.include_router(forgot_password.router, prefix="/forgot-password", tags=["Forgot Password"])
api_router.include_router(authentication.router, prefix="/authentication", tags=["Authentication"])
api_router.include_router(my_profile.router, prefix="/my-profile", tags=["My Profile"])
api_router.include_router(change_password.router, prefix="/change-password", tags=["Change Password"])
# api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
# api_router.include_router(my_applications.router, prefix="/my-applications", tags=["My Applications"])
# api_router.include_router(for_approvals.router, prefix="/for-approvals", tags=["For Approvals"])
api_router.include_router(offices.router, prefix="/offices", tags=["Offices"])
api_router.include_router(positions.router, prefix="/positions", tags=["Positions"])
# api_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_router.include_router(user_types.router, prefix="/user-types", tags=["User Types"])
