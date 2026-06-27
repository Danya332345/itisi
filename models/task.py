from enum import Enum

class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Status(Enum):
    TO_DO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class Task:
    def __init__(self, title, description, priority=Priority.MEDIUM, status=Status.TO_DO, task_id=None):
        self._id = task_id
        self._title = title
        self._description = description
        self._priority = priority
        self._status = status

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not value.strip():
            raise ValueError("Название не может быть пустым")
        self._title = value.strip()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not value or not value.strip():
            raise ValueError("Описание не может быть пустым")
        self._description = value.strip()

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        if not isinstance(value, Priority):
            raise ValueError("Приоритет должен быть типом Priority")
        self._priority = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if not isinstance(value, Status):
            raise ValueError("Статус должен быть типом Status")
        self._status = value

    def to_dict(self):
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "priority": self._priority.value,
            "status": self._status.value,
            "type": "base"
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            title=data["title"],
            description=data["description"],
            priority=Priority(data["priority"]),
            status=Status(data["status"]),
            task_id=data.get("id")
        )
        return task

    def display(self):
        return (f"ID: {self._id}\n"
                f"Название: {self._title}\n"
                f"Описание: {self._description}\n"
                f"Приоритет: {self._priority.value}\n"
                f"Статус: {self._status.value}")

    def __str__(self):
        return f"{self._id}: {self._title} ({self._priority.value}, {self._status.value})"


class UrgentTask(Task):
    """Подкласс для срочных задач (наследование и полиморфизм)"""
    def __init__(self, title, description, status=Status.TO_DO, task_id=None):
        super().__init__(title, description, Priority.HIGH, status, task_id)
        self._deadline = None

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, value):
        self._deadline = value

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "urgent"
        data["deadline"] = self._deadline
        return data

    @classmethod
    def from_dict(cls, data):
        task = cls(
            title=data["title"],
            description=data["description"],
            status=Status(data["status"]),
            task_id=data.get("id")
        )
        task.deadline = data.get("deadline")
        return task

    def display(self):
        base = super().display()
        return base + f"\nДедлайн: {self._deadline or 'Не указан'}"
