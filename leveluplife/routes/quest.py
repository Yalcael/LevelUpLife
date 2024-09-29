from typing import Sequence

from leveluplife.auth.utils import get_current_active_user
from leveluplife.controllers.quest import QuestController
from leveluplife.dependencies import get_quest_controller
from leveluplife.models.error import QuestNotFoundError
from leveluplife.models.quest import QuestCreate, QuestUpdate
from leveluplife.models.relationship import UserQuestLinkCreate
from leveluplife.models.view import QuestView, QuestWithUser
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from uuid import UUID

router = APIRouter(
    prefix="/quests",
    tags=["quests"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=QuestView, status_code=201)
async def create_quest(
    quest: QuestCreate,
    quest_controller: QuestController = Depends(get_quest_controller),
) -> QuestView:
    return QuestView.model_validate(await quest_controller.create_quest(quest))


@router.patch("/{quest_id}", response_model=QuestView)
async def update_quest(
    *,
    quest_id: UUID,
    quest_update: QuestUpdate,
    quest_controller: QuestController = Depends(get_quest_controller),
) -> QuestView:
    return QuestView.model_validate(
        await quest_controller.update_quest(quest_id, quest_update)
    )


@router.delete("/{quest_id}", status_code=204)
async def delete_quest(
    *, quest_id: UUID, quest_controller: QuestController = Depends(get_quest_controller)
) -> None:
    await quest_controller.delete_quest(quest_id)


@router.get("/", response_model=Sequence[QuestView])
async def get_quests(
    *,
    offset: int = 0,
    quest_controller: QuestController = Depends(get_quest_controller),
) -> Sequence[QuestView]:
    return [
        QuestView.model_validate(quest)
        for quest in await quest_controller.get_quests(offset * 20, 20)
    ]


@router.get("/{quest_id}", response_model=QuestWithUser)
async def get_quest_by_id(
    *, quest_id: UUID, quest_controller: QuestController = Depends(get_quest_controller)
) -> QuestWithUser:
    return QuestWithUser.model_validate(
        await quest_controller.get_quest_by_id(quest_id)
    )


@router.patch("/{quest_id}/link_user", response_model=QuestWithUser, status_code=200)
async def assign_quest_to_user(
    *,
    quest_id: UUID,
    user_quest_link_create: UserQuestLinkCreate,
    quest_controller: QuestController = Depends(get_quest_controller),
) -> QuestWithUser:
    # Get the current datetime as the start time
    quest_start = datetime.now()

    # Retrieve the quest to access its type and calculate the end time
    quest = await quest_controller.get_quest_by_id(quest_id)

    # Ensure the quest is found
    if not quest:
        raise QuestNotFoundError(quest_id=quest_id)

    # Determine the end time based on the quest's type
    quest_duration = timedelta(
        days=quest.type.duration
    )  # Using the duration defined in the Type enum
    quest_end = quest_start + quest_duration

    # Call the controller method to assign the quest to the user
    return QuestWithUser.model_validate(
        await quest_controller.assign_quest_to_user(
            quest_id,
            user_quest_link_create,
            quest_start=quest_start,
            quest_end=quest_end,
            status=user_quest_link_create.status,
        )
    )


@router.delete("/{quest_id}/unlink_user/{user_id}", status_code=204)
async def remove_quest_from_user(
    *,
    quest_id: UUID,
    user_id: UUID,
    quest_controller: QuestController = Depends(get_quest_controller),
) -> None:
    await quest_controller.remove_quest_from_user(quest_id, user_id)
