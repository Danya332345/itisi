class ConsoleView:
    @staticmethod
    def display_menu():
        print("\n=== Менеджер задач ===")
        print("1. Добавить задачу")
        print("2. Показать все задачи")
        print("3. Взять следующую по приоритету (очередь)")
        print("4. Редактировать задачу")
        print("5. Удалить задачу")
        print("6. Фильтровать задачи")
        print("7. Отменить последнее действие")
        print("8. Сохранить в JSON")
        print("9. Загрузить из JSON")
        print("0. Выход")
        return input("Выберите пункт: ").strip()

    @staticmethod
    def get_task_details():
        title = input("Название: ").strip()
        while not title:
            print("Название не может быть пустым.")
            title = input("Название: ").strip()
        description = input("Описание: ").strip()
        while not description:
            print("Описание не может быть пустым.")
            description = input("Описание: ").strip()
        priority = input("Приоритет (Low/Medium/High): ").strip()
        while priority not in ["Low", "Medium", "High"]:
            print("Некорректный приоритет. Выберите Low, Medium или High.")
            priority = input("Приоритет (Low/Medium/High): ").strip()
        status = input("Статус (To Do/In Progress/Done): ").strip()
        while status not in ["To Do", "In Progress", "Done"]:
            print("Некорректный статус. Выберите To Do, In Progress или Done.")
            status = input("Статус (To Do/In Progress/Done): ").strip()
        return title, description, priority, status

    @staticmethod
    def display_tasks(tasks):
        if not tasks:
            print("Задачи отсутствуют.")
        else:
            for t in tasks:
                print(t.display())
                print("-" * 30)

    @staticmethod
    def get_task_id():
        try:
            return int(input("Введите ID задачи: ").strip())
        except ValueError:
            return None

    @staticmethod
    def get_filter_criteria():
        print("Фильтровать по:")
        print("1. Статус")
        print("2. Приоритет")
        choice = input("Выберите: ").strip()
        if choice == "1":
            status = input("Статус (To Do/In Progress/Done): ").strip()
            while status not in ["To Do", "In Progress", "Done"]:
                print("Некорректный статус.")
                status = input("Статус (To Do/In Progress/Done): ").strip()
            return ("status", status)
        elif choice == "2":
            priority = input("Приоритет (Low/Medium/High): ").strip()
            while priority not in ["Low", "Medium", "High"]:
                print("Некорректный приоритет.")
                priority = input("Приоритет (Low/Medium/High): ").strip()
            return ("priority", priority)
        else:
            return None

    @staticmethod
    def show_message(msg):
        print(msg)
