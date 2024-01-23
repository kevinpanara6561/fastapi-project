from fastapi import APIRouter

from app.routers.admin.crud.admin_user.routes import router as admin_user
from app.routers.admin.crud.admin_users.routes import router as admin_users
from app.routers.admin.crud.authentication.routes import router as authentication
from app.routers.admin.crud.issues.routes import router as issues
from app.routers.admin.crud.module_types.routes import router as module_types
from app.routers.admin.crud.modules.routes import router as modules
from app.routers.admin.crud.operations.routes import router as operations
from app.routers.admin.crud.projects.routes import router as projects
from app.routers.admin.crud.roles.routes import router as roles
from app.routers.admin.crud.tasks.routes import router as tasks

router = APIRouter()

router.include_router(authentication)
router.include_router(admin_user)
router.include_router(admin_users)
router.include_router(issues)
router.include_router(module_types)
router.include_router(modules)
router.include_router(operations)
router.include_router(projects)
router.include_router(roles)
router.include_router(tasks)
