from typing import Sequence

from fastapi import APIRouter, Depends

from leveluplife.controllers.task import TaskController
from leveluplife.dependencies import get_task_controller
from leveluplife.models.task import TaskCreate
from leveluplife.models.view import TaskView

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=TaskView, status_code=201)
async def create_task(
    task: TaskCreate, task_controller: TaskController = Depends(get_task_controller)
) -> TaskView:
    return TaskView.model_validate(await task_controller.create_task(task))


@router.get("/", response_model=Sequence[TaskView])
async def get_tasks(
    *, task_controller: TaskController = Depends(get_task_controller)
) -> Sequence[TaskView]:
    return [TaskView.model_validate(task) for task in await task_controller.get_tasks()]
