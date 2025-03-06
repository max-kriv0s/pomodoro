from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Tasks, Categories
from schema import TaskCreateSchema


class TaskRepository:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_tasks(self) -> list[Tasks]:
        async with self.db_session as session:
            tasks: list[Tasks] = (await session.execute(select(Tasks))).scalars().all()
        return tasks

    async def get_task(self, task_id: int) -> Tasks | None:
        async with self.db_session as session:
            task: Tasks = (
                await session.execute(select(Tasks).where(Tasks.id == task_id))
            ).scalar_one_or_none()
        return task

    async def get_user_task(self, user_id: int, task_id: int) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        async with self.db_session as session:
            task: Tasks = (await session.execute(query)).scalar_one_or_none()
        return task

    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        task_model = Tasks(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id,
            user_id=user_id,
        )
        async with self.db_session as session:
            await session.add(task_model)
            await session.commit()
            return task_model.id

    async def delete_task(self, task_id: int) -> None:
        query = delete(Tasks).where(Tasks.id == task_id)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()

    async def get_task_by_category_name(self, category_name: str) -> list[Tasks]:
        query = (
            select(Tasks)
            .join(Categories, Tasks.category_id == Categories.id)
            .where(Categories.name == category_name)
        )
        async with self.db_session as session:
            tasks: list[Tasks] = (await session.execute(query)).scalars().all()
        return tasks

    async def update_task_name(self, task_id: int, name: str) -> Tasks:
        query = (
            update(Tasks)
            .where(Tasks.id == task_id)
            .values(name=name)
            .returning(Tasks.id)
        )
        async with self.db_session as session:
            task_id: int = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            return await self.get_task(task_id)
