from uuid import UUID

from fastapi import APIRouter

router = APIRouter(
    prefix="/voting",
)

@router.post("/")
async def create_voting(
        voting_data: VotingCreateSchema,
        voting_service: VotingService
):
    pass


@router.post("/{voting_id}/close")
async def close_voting(
        voting_id: UUID,
        voting_service: VotingService,
):
    pass


@router.post("/{voting_id}/vote")
async def create_user_vote(
        voting_id: UUID,
        voting_service: VotingService
):
    pass


@router.get("/{voting_id}")
async def get_voting(
        voting_id: UUID,
        voting_service: VotingService
):
    pass

@router.delete("/{voting_id}")
async def delete_voting(
        voting_id: UUID,
        voting_service: VotingService,
):
    pass
