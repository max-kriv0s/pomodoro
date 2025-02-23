from dataclasses import dataclass
from exception import TaskNotFoundExeption
from repository import TaskRepository, TaskCache
from schema import TaskCreateSchema, TaskSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    def get_tasks(self) -> list[TaskSchema]:
        if tasks := self.task_cache.get_tasks():
            return tasks
        else:
            tasks = self.task_repository.get_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)
            return tasks_schema

    def create_task(self, task: TaskCreateSchema, user_id: int) -> TaskSchema:
        task_id = self.task_repository.create_task(task, user_id)
        task = self.task_repository.get_task(task_id)
        return TaskSchema.model_validate(task)

    def update_task_name(self, task_id: int, name: str, user_id: int) -> TaskSchema:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFoundExeption
        task = self.task_repository.update_task_name(task_id=task_id, name=name)
        return TaskSchema.model_validate(task)

    def delete_task(self, task_id: int, user_id: int) -> None:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFoundExeption
        self.task_repository.delete_task(task_id)
