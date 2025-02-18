from typing import Annotated

from fastapi import APIRouter, status, Depends

from dependency import get_task_service
from schema.task import TaskSchema
from service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/all", response_model=list[TaskSchema])
async def get_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)]
):
    return task_service.get_tasks()


@router.post("/", response_model=TaskSchema)
async def create_task(task: TaskSchema, task_service: Annotated[TaskService, Depends(get_task_service)]):
    return task_service.create_task(task)


@router.patch("/{task_id}", response_model=TaskSchema)
async def update_task(
    task_id: int, 
    name: str, 
    task_service: Annotated[TaskService, Depends(get_task_service)]
    ):
    return task_service.update_task_name(task_id, name)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)]
    ):
    return task_service.delete_task(task_id)

