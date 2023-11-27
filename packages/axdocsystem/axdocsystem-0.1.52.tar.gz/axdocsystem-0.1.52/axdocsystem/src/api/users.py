from typing import Optional, Type
from axsqlalchemy.repository import BaseRepository
from fastapi import HTTPException, status

from pydantic import BaseModel
from axdocsystem.db.models import Department, Users
from axdocsystem.db.schemas import QuickSearchResult, UsersFullSchema, UsersSchema
from axdocsystem.src.api.base import Request, with_uow
from axdocsystem.src.api.schemas import UsersPostSchema
from axdocsystem.utils.email_system import EmailSystem
from axdocsystem.utils.message_system import MessageSystem
from axdocsystem.utils.utils.one_time_token_manager import OneTimeTokenManager
from .base_crud_api import BaseCRUDApi


class UsersApi(BaseCRUDApi):
    AUTH_EXISTS_EXCEPTION = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=[{"msg": "Данная почта уже зарегистрировано"}], 
    )

    def __init__(self, uowf, settings, token_manager: OneTimeTokenManager, router = None) -> None:
        super().__init__(uowf, settings, router)
        self.token_manager = token_manager
        self.email_system = EmailSystem(settings)
        self.message_system = MessageSystem(self.email_system, system_name='axdocsystem')

    @property
    def schema_full(self):
        return UsersFullSchema

    @property
    def schema(self) -> Type[BaseModel]:
        return UsersSchema

    @property
    def schema_create(self):
        return UsersPostSchema 

    @with_uow
    async def create(self, req: Request, data: UsersPostSchema):
        if (await req.state.uow.repo.users.get(data.email)) is not None:
            raise self.AUTH_EXISTS_EXCEPTION

        await self.find_repo(req).add(data)
        token = self.token_manager.create(data.email)
        await self.message_system.send_verification_code(data.email, token)

    def get_repo(self, req: Request) -> BaseRepository:
        return req.state.uow.repo.users

    def get_quick_search_pattern_filters(self, req: Request, pattern: str):
        return (getattr(self.find_repo(req).Model, 'fullname').ilike(f'%{pattern}%'),)

    def get_item_as_quick_search_result(self, item: UsersSchema):
        return QuickSearchResult(
            id=item.email,
            name=item.fullname,
        )

    async def all(
        self, 
        req: Request, 
        email: Optional[str] = None, 
        deparment_name: Optional[str] = None, 
        fullname: Optional[str] = None, 
        page: int = 1, 
        count: int = 10,
    ):
        req.state.filters = []

        if email:
            req.state.filters.append(Users.email.ilike(f'%{email}%'))
        if fullname:
            req.state.filters.append(Users.fullname.ilike(f'%{fullname}%'))
        if deparment_name:
            req.state.filters.append(Department.name.ilike(f'%{deparment_name}%'))

        return await super().all(req=req, page=page, count=count)

    async def delete(self, req: Request, id: str):
        await super().delete(req=req, id=id)  # type: ignore 

