import json
from models.task import Task, Priority, Status, UrgentTask

class TaskManager:
    def __init__(self):
        self._tasks = []          # все задачи
        self._next_id = 1
        self._undo_stack = []     # стек для отмены: (action, data)

    # ---------- основные операции ----------
    def add_task(self, task):
        task.id = self._next_id
        self._next_id += 1
        self._tasks.append(task)
        self._undo_stack.append(("add", task))   # сохраняем объект для отмены

    def get_all_tasks(self):
        return self._tasks.copy()

    def get_task_by_id(self, task_id):
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id, **kwargs):
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        # сохраняем старые данные для отмены
        old_dict = task.to_dict()
        if "title" in kwargs:
            task.title = kwargs["title"]
        if "description" in kwargs:
            task.description = kwargs["description"]
        if "priority" in kwargs:
            task.priority = kwargs["priority"]
        if "status" in kwargs:
            task.status = kwargs["status"]
        self._undo_stack.append(("update", (task_id, old_dict)))
        return True

    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        self._tasks.remove(task)
        self._undo_stack.append(("delete", task))
        return True

    # ---------- очередь по приоритету ----------
    def get_next_task_by_priority(self):
        """Извлекает задачу с наивысшим приоритетом (High > Medium > Low)"""
        if not self._tasks:
            return None
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        best = min(self._tasks, key=lambda t: priority_order[t.priority])
        self._tasks.remove(best)
        return best

    # ---------- фильтрация ----------
    def filter_by_status(self, status):
        return [t for t in self._tasks if t.status == status]

    def filter_by_priority(self, priority):
        return [t for t in self._tasks if t.priority == priority]

    # ---------- отмена последнего действия ----------
    def undo(self):
        if not self._undo_stack:
            return False
        action, data = self._undo_stack.pop()
        if action == "add":
            # удалить добавленную задачу
            task = data
            self._tasks.remove(task)
        elif action == "delete":
            # восстановить удалённую задачу
            task = data
            self._tasks.append(task)
        elif action == "update":
            task_id, old_dict = data
            task = self.get_task_by_id(task_id)
            if task:
                # восстановить старые значения
                task.title = old_dict["title"]
                task.description = old_dict["description"]
                task.priority = Priority(old_dict["priority"])
                task.status = Status(old_dict["status"])
        return True

    # ---------- JSON сериализация ----------
    def save_to_json(self, filename):
        try:
            data = [task.to_dict() for task in self._tasks]
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    def load_from_json(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._tasks.clear()
            self._next_id = 1
            for item in data:
                if item.get("type") == "urgent":
                    task = UrgentTask.from_dict(item)
                else:
                    task = Task.from_dict(item)
                if task.id and task.id >= self._next_id:
                    self._next_id = task.id + 1
                self._tasks.append(task)
            return True
        except Exception:
            return False
