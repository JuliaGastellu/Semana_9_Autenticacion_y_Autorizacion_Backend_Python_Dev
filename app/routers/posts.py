from typing import Annotated

from fastapi import APIRouter, Query, Response, status

from app.dependencies import EditorDep, OptionalUserDep, PostServiceDep
from app.exceptions import ForbiddenError, NotFoundError
from app.schemas import PostCreate, PostPage, PostResponse, PostStatus, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=PostPage)
async def list_posts(service: PostServiceDep, user: OptionalUserDep, skip: Annotated[int, Query(ge=0)] = 0, limit: Annotated[int, Query(ge=1, le=100)] = 20, status_filter: PostStatus | None = None, category_id: int | None = None, tag: str | None = None, author_id: int | None = None):
    if user is None or user.role == "user": status_filter = PostStatus.PUBLISHED
    items, total = await service.page(skip=skip, limit=limit, status=status_filter, category_id=category_id, tag=tag, author_id=author_id)
    return PostPage(items=items, total=total, skip=skip, limit=limit)


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, service: PostServiceDep, user: OptionalUserDep):
    item = await service.get(post_id)
    if item.status != "published" and (user is None or (user.role not in {"admin", "editor"} and item.author_id != user.id)): raise NotFoundError(f"El post {post_id} no existe")
    return item


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(data: PostCreate, service: PostServiceDep, user: EditorDep): return await service.create(data, user.id)


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, data: PostUpdate, service: PostServiceDep, user: EditorDep):
    item = await service.get(post_id)
    if user.role != "admin" and item.author_id != user.id: raise ForbiddenError("Solo puedo editar mis propios posts")
    return await service.update(post_id, data)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, service: PostServiceDep, user: EditorDep):
    item = await service.get(post_id)
    if user.role != "admin" and item.author_id != user.id: raise ForbiddenError("Solo puedo borrar mis propios posts")
    await service.delete(post_id); return Response(status_code=204)
