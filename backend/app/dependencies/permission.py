from typing import Annotated

from fastapi import Depends

from backend.app.core.enum.permission import MemberPermission
from backend.app.core.utils.permission import check_permission_dependency

MemberPermissionDep = Annotated[MemberPermission, Depends(check_permission_dependency(MemberPermission.MEMBER))]
ModeratorPermissionDep = Annotated[MemberPermission, Depends(check_permission_dependency(MemberPermission.MODERATOR))]
AdminPermissionDep = Annotated[MemberPermission, Depends(check_permission_dependency(MemberPermission.ADMIN))]