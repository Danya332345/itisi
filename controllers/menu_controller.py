from models.task_manager import TaskManager
from models.task import Task, Priority, Status, UrgentTask
from views.console_view import ConsoleView

class MenuController:
    def __init__(self):
        self.manager = TaskManager()
        self.view = ConsoleView()

    def run(self):
        while True:
            choice = self.view.display_menu()
            if choice == "1":
                self._add_task()
            elif choice == "2":
                self._view_all()
            elif choice == "3":
                self._next_priority()
            elif choice == "4":
                self._edit_task()
            elif choice == "5":
                self._delete_task()
            elif choice == "6":
                self._filter_tasks()
            elif choice == "7":
                self._undo()
            elif choice == "8":
                self._save()
            elif choice == "9":
                self._load()
            elif choice == "0":
                break
            else:
                print("Неверный пункт меню.")

    def _add_task(self):
        title, desc, prio, stat = self.view.get_task_details()
        priority = Priority[prio.upper()]
        status = Status[stat.upper().replace(" ", "_")]
        task = Task(title, desc, priority, status)
        # возможность создать срочную задачу (наследование)
        urgent = input("Это срочная задача? (y/n): ").strip().lower()
        if urgent == "y":
            task = UrgentTask(title, desc, status)
            deadline = input("Дедлайн (опционально): ").strip()
            if deadline:
                task.deadline = deadline
        self.manager.add_task(task)
        self.view.show_message("Задача добавлена.")

    def _view_all(self):
        tasks = self.manager.get_all_tasks()
        self.view.display_tasks(tasks)

    def _next_priority(self):
        task = self.manager.get_next_task_by_priority()
        if task:
            print("Следующая задача по приоритету:")
            print(task.display())
        else:
            print("Очередь пуста.")

    def _edit_task(self):
        tid = self.view.get_task_id()
        if tid is None:
            print("Некорректный ID.")
            return
        task = self.manager.get_task_by_id(tid)
        if not task:
            print("Задача не найдена.")
            return
        print("Оставьте поле пустым, чтобы не изменять.")
        title = input(f"Название ({task.title}): ").strip()
        desc = input(f"Описание ({task.description}): ").strip()
        prio = input(f"Приоритет ({task.priority.value}) [Low/Medium/High]: ").strip()
        stat = input(f"Статус ({task.status.value}) [To Do/In Progress/Done]: ").strip()
        # собираем изменения
        updates = {}
        if title:
            updates["title"] = title
        if desc:
            updates["description"] = desc
        if prio:
            try:
                updates["priority"] = Priority[prio.upper()]
            except KeyError:
                print("Некорректный приоритет, оставляем как есть.")
        if stat:
            try:
                updates["status"] = Status[stat.upper().replace(" ", "_")]
            except KeyError:
                print("Некорректный статус, оставляем как есть.")
        if updates:
            self.manager.update_task(tid, **updates)
            self.view.show_message("Задача обновлена.")
        else:
            print("Изменений не внесено.")

    def _delete_task(self):
        tid = self.view.get_task_id()
        if tid is None:
            print("Некорректный ID.")
            return
        if self.manager.delete_task(tid):
            self.view.show_message("Задача удалена.")
        else:
            print("Задача не найдена.")

    def _filter_tasks(self):
        criteria = self.view.get_filter_criteria()
        if not criteria:
            print("Неверный выбор фильтра.")
            return
        ftype, value = criteria
        if ftype == "status":
            status = Status[value.upper().replace(" ", "_")]
            tasks = self.manager.filter_by_status(status)
        else:
            priority = Priority[value.upper()]
            tasks = self.manager.filter_by_priority(priority)
        self.view.display_tasks(tasks)

    def _undo(self):
        if self.manager.undo():
            self.view.show_message("Отмена выполнена.")
        else:
            print("Нет действий для отмены.")

    def _save(self):
        filename = input("Имя файла (по умолчанию tasks.json): ").strip()
        if not filename:
            filename = "tasks.json"
        if self.manager.save_to_json(filename):
            self.view.show_message(f"Сохранено в {filename}")
        else:
            print("Ошибка сохранения.")

    def _load(self):
        filename = input("Имя файла (по умолчанию tasks.json): ").strip()
        if not filename:
            filename = "tasks.json"
        if self.manager.load_from_json(filename):
            self.view.show_message(f"Загружено из {filename}")
        else:
            print("Ошибка загрузки.")
