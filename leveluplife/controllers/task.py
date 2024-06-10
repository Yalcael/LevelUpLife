from typing import Sequence

from sqlmodel import Session, select
from loguru import logger
from sqlalchemy.exc import IntegrityError

from leveluplife.models.error import TaskAlreadyExistsError
from leveluplife.models.task import TaskCreate, Task


class TaskController:
    def __init__(self, session: Session) -> None:
        self.session = session

    async def create_task(self, task_create: TaskCreate) -> Task:
        try:
            new_task = Task(**task_create.dict())
            self.session.add(new_task)
            self.session.commit()
            self.session.refresh(new_task)
            logger.info(f"New task created: {new_task.title}")
            return new_task
        except IntegrityError:
            raise TaskAlreadyExistsError(title=task_create.title)

    async def get_tasks(self) -> Sequence[Task]:
        logger.info("Getting tasks")
        return self.session.exec(select(Task)).all()
