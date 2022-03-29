import pytest
from app import models
from app.config import settings
from httpx import AsyncClient
from sqlalchemy.orm import Session


class TestApi:
    """Test Api class"""

    @pytest.mark.asyncio
    async def test_api_root(self, async_client: AsyncClient) -> None:
        response = await async_client.get(f'{settings.API_V1_STR}/')
        assert response.status_code == 200
        assert 'response' in response.json()

    @pytest.mark.asyncio
    async def test_create_task(
        self,
        db_session: Session,
        async_client: AsyncClient,
        new_task: dict
    ) -> None:

        response = await async_client.post(
            f'{settings.API_V1_STR}/tasks', json=new_task)

        # created_task = await models.Task.get(
        #     db_session, last_name=new_task['last_name'], raise_404=False)

        assert response.status_code == 201
        # assert response.status_code == response
        # assert created_task
        # assert new_task.items() <= created_task.items()
