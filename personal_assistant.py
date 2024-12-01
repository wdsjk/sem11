import os
import json
import csv
import datetime


NOTES_FILE = 'notes.json'

def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_data(file_path, default_data):
    if not os.path.exists(file_path):
        save_data(file_path, default_data)
        return default_data
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


class Note:
    def __init__(self, id, title, content, timestamp):
        self.note_id = id
        self.title = title
        self.content = content
        self.timestamp = timestamp


class NoteManager:
    def __init__(self):
        self.notes = []
        self.load_notes()

    def load_notes(self):
        data = load_data(NOTES_FILE, [])
        self.notes = [Note(**note) for note in data]

    def save_notes(self):
        data = [note.__dict__ for note in self.notes]
        save_data(NOTES_FILE, data)

    def add_note(self, title, content):
        note_id = max([note.note_id for note in self.notes], default=0) + 1
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        new_note = Note(note_id, title, content, timestamp)
        self.notes.append(new_note)
        self.save_notes()
        print("Заметка успешно добавлена")

    def list_notes(self):
        if not self.notes:
            print("Список заметок пуст")
            return
        for note in self.notes:
            print(f"{note.note_id}. {note.title} (дата: {note.timestamp})")

    def get_note_by_id(self, note_id):
        for note in self.notes:
            if note.note_id == note_id:
                return note
        return None

    def view_note(self, note_id):
        note = self.get_note_by_id(note_id)
        if note:
            print(f"Заголовок: {note.title}")
            print(f"Содержимое: {note.content}")
            print(f"Дата создания / изменения: {note.timestamp}")
        else:
            print("Заметка не найдена")

    def edit_note(self, note_id, new_title, new_content):
        note = self.get_note_by_id(note_id)
        if note:
            note.title = new_title
            note.content = new_content
            note.timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.save_notes()
            print('Заметка успешно изменена')
        else:
            print('Заметка не найдена')

    def delete_note(self, note_id):
        note = self.get_note_by_id(note_id)
        if note:
            self.notes.remove(note)
            self.save_notes()
            print('Заметка успешно удалена')
        else:
            print('Заметка не найдена')

    def export_notes_to_csv(self):
        if not self.notes:
            print("Список заметок пуст")
            return
        file_name = "notes_export.csv"
        with open(file_name, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['id', 'Заголовок', 'Содержимое', 'Дата']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for note in self.notes:
                writer.writerow({
                    "id": note.note_id,
                    'Заголовок': note.title,
                    'Содержимое': note.content,
                    'Дата': note.timestamp
                })
            print(f"Заметки успешно экспортированы в файл {file_name}")

    def import_notes_to_csv(self):
        file_name = input('Введите имя CSV-файла: ')
        if not os.path.exists(file_name):
            print("Файл не найден")
            return
        with open(file_name, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                note_id = max([note.note_id for note in self.notes], default=0) + 1
                title = row.get('Заголовок', '')
                content = row.get('Содержимое', '')
                timestamp = row.get('Дата', datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
                new_note = Note(note_id, title, content, timestamp)
                self.notes.append(new_note)
                self.save_notes()


def notes():
    menu = """
Управление заметками:
1. Добавить новую заметку
2. Посмотреть список заметок
3. Посмотреть заметку
4. Редактировать заметку
5. Удалить заметку
6. Экспорт заметок в CSV
7. Импорт заметок из CSV
8. Назад
    """
    manager = NoteManager()

    while True:
        print(menu)

        choice = input("Выберите действие (1/2/3/4/5/6/7/8): ")
        if choice == "1":
            title = input("Введите заголовок заметки: ")
            content = input("Введите содержимое заметки: ")
            manager.add_note(title, content)
        elif choice == "2":
            manager.list_notes()
        elif choice == "3":
            try:
                note_id = int(input("Введите ID заметки: "))
                manager.view_note(note_id)
            except ValueError:
                print("Некорректный ID")
        elif choice == "4":
            try:
                note_id = int(input("Введите ID заметки: "))
                new_title = input("Введите заголовок заметки: ")
                new_content = input("Введите содержимое заметки: ")
                manager.edit_note(note_id, new_title, new_content)
            except ValueError:
                print("Некорректный ID")
        elif choice == "5":
            try:
                note_id = int(input("Введите ID заметки: "))
                manager.delete_note(note_id)
            except ValueError:
                print("Некорректный ID")
        elif choice == "6":
            manager.export_notes_to_csv()
        elif choice == "7":
            manager.import_notes_to_csv()
        elif choice == "8":
            break
        else:
            print("Такой опции нет!")


class Task:
    def __init__(self, id, description, deadline, status):
        self.task_id = id
        self.description = description
        self.deadline = deadline
        self.status = status


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        data = load_data('tasks.json', [])
        self.tasks = [Task(**task) for task in data]

    def save_tasks(self):
        data = [task.__dict__ for task in self.tasks]
        save_data('tasks.json', data)

    def add_task(self, description, deadline):
        task_id = max([task.task_id for task in self.tasks], default=0) + 1
        new_task = Task(task_id, description, deadline, "Не выполнено")
        self.tasks.append(new_task)
        self.save_tasks()
        print("Задача успешно добавлена")

    def list_tasks(self):
        if not self.tasks:
            print("Список задач пуст")
            return
        for task in self.tasks:
            print(f"{task.task_id}. {task.description} (Дедлайн: {task.deadline}, Статус: {task.status})")

    def mark_task_done(self, task_id):
        task = next((task for task in self.tasks if task.task_id == task_id), None)
        if task:
            task.status = "Выполнено"
            self.save_tasks()
            print("Задача отмечена как выполненная")
        else:
            print("Задача не найдена")

    def delete_task(self, task_id):
        task = next((task for task in self.tasks if task.task_id == task_id), None)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print("Задача удалена")
        else:
            print("Задача не найдена")


def tasks():
    menu = """
Управление задачами:
1. Добавить новую задачу
2. Просмотреть задачи
3. Отметить задачу выполненной
4. Удалить задачу
5. Назад
    """
    manager = TaskManager()

    while True:
        print(menu)

        choice = int(input("Выберите действие (1/2/3/4/5): "))
        if choice == 1:
            description = input("Введите описание задачи: ")
            deadline = input("Введите дедлайн (дд-мм-гггг): ")
            manager.add_task(description, deadline)
        elif choice == 2:
            manager.list_tasks()
        elif choice == 3:
            try:
                task_id = int(input("Введите ID задачи: "))
                manager.mark_task_done(task_id)
            except ValueError:
                print("Некорректный ID")
        elif choice == 4:
            try:
                task_id = int(input("Введите ID задачи: "))
                manager.delete_task(task_id)
            except ValueError:
                print("Некорректный ID")
        elif choice == 5:
            break
        else:
            print("Такой опции нет!")


class Contact:
    def __init__(self, id, name, phone, email):
        self.contact_id = id
        self.name = name
        self.phone = phone
        self.email = email


class ContactManager:
    def __init__(self):
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        data = load_data('contacts.json', [])
        self.contacts = [Contact(**contact) for contact in data]

    def save_contacts(self):
        data = [contact.__dict__ for contact in self.contacts]
        save_data('contacts.json', data)

    def add_contact(self, name, phone, email):
        contact_id = max([contact.contact_id for contact in self.contacts], default=0) + 1
        new_contact = Contact(contact_id, name, phone, email)
        self.contacts.append(new_contact)
        self.save_contacts()
        print("Контакт успешно добавлен")

    def list_contacts(self):
        if not self.contacts:
            print("Список контактов пуст")
            return
        for contact in self.contacts:
            print(f"{contact.contact_id}. {contact.name} (Телефон: {contact.phone}, Email: {contact.email})")

    def delete_contact(self, contact_id):
        contact = next((contact for contact in self.contacts if contact.contact_id == contact_id), None)
        if contact:
            self.contacts.remove(contact)
            self.save_contacts()
            print("Контакт удален")
        else:
            print("Контакт не найден")


def contacts():
    menu = """
Управление контактами:
1. Добавить контакт
2. Просмотреть контакты
3. Удалить контакт
4. Назад
    """
    manager = ContactManager()

    while True:
        print(menu)

        choice = input("Выберите действие (1/2/3/4): ")
        if choice == "1":
            name = input("Введите имя контакта: ")
            phone = input("Введите телефон контакта: ")
            email = input("Введите email контакта: ")
            manager.add_contact(name, phone, email)
        elif choice == "2":
            manager.list_contacts()
        elif choice == "3":
            try:
                contact_id = int(input("Введите ID контакта: "))
                manager.delete_contact(contact_id)
            except ValueError:
                print("Некорректный ID")
        elif choice == "4":
            break
        else:
            print("Такой опции нет!")


class FinanceRecord:
    def __init__(self, id, amount, category, date, description):
        self.record_id = id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description


class FinanceRecordManager:
    def __init__(self):
        self.records = []
        self.load_records()

    def load_records(self):
        data = load_data('finance.json', [])
        self.records = [FinanceRecord(**record) for record in data]

    def save_records(self):
        data = [record.__dict__ for record in self.records]
        save_data('finance.json', data)

    def add_record(self, amount, category, description):
        record_id = max([record.record_id for record in self.records], default=0) + 1
        new_record = FinanceRecord(record_id, amount, category, datetime.datetime.now(), description)
        self.records.append(new_record)
        self.save_records()
        print("Финансовая запись успешно добавлена")

    def list_records(self):
        if not self.records:
            print("Список финансовых записей пуст")
            return
        for record in self.records:
            print(f"{record.record_id}. {record.description} (Сумма: {record.amount}, Категория: {record.category}, Дата: {record.date})")

    def list_filtered_records(self, fil_cat, asc_desc):
        if not self.records:
            print("Список финансовых записей пуст")
            return

        records = self.records
        if fil_cat.lower() == 'категория':
            if asc_desc.lower() == 'возрастание':
                records.sort(key=lambda x: x.category)
            elif asc_desc.lower() == 'убывание':
                records.sort(key=lambda x: x.category, reverse=True)
            else:
                print("Ошибка! Введите 'возрастание' или 'убывание'!")
        elif fil_cat.lower() == 'дата':
            if asc_desc.lower() == 'возрастание':
                records.sort(key=lambda x: x.date)
            elif asc_desc.lower() == 'убывание':
                records.sort(key=lambda x: x.date, reverse=True)
            else:
                print("Ошибка! Введите 'возрастание' или 'убывание'!")
        else:
            print("Ошибка! Введите 'категория' или 'дата'!")

        for record in records:
            print(f"{record.record_id}. {record.description} (Сумма: {record.amount}, Категория: {record.category}, Дата: {record.date})")

    def generate_report(self, start, end):
        start = datetime.datetime.strptime(start, "%d-%m-%Y")
        end = datetime.datetime.strptime(end, "%d-%m-%Y")

        rev = 0
        exp = 0
        for record in self.records:
            if start <= record.date <= end:
                if record.amount > 0:
                    rev += record.amount
                else:
                    exp += record.amount

        file_name = f"report_{start}_{end}.csv"
        with open(file_name, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['Id', 'Начальная дата', 'Конечная дата', 'Общий доход', 'Общие расходы', 'Баланс']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for record in self.records:
                writer.writerow({
                    'Id': record.id,
                    'Начальная дата': start,
                    'Конечная дата': end,
                    'Общий доход': rev,
                    'Общие расходы': exp,
                    'Баланс': rev-exp
                })

        print(f"Финансовый отчёт за период с {start} по {end}:\n- Общий доход: {rev} руб.\n- Общие расходы: {exp} руб.\n- Баланс: {rev-exp} руб.\nПодробная информация сохранена в файле {file_name}")

    def delete_record(self, record_id):
        record = next((record for record in self.records if record.record_id == record_id), None)
        if record:
            self.records.remove(record)
            self.save_records()
            print("Финансовая запись удалена")
        else:
            print("Финансовая запись не найдена")


def finance_records():
    menu = """
Управление финансовыми записями:
1. Добавить новую запись
2. Просмотреть все записи
3. Генерация отчёта
4. Удалить запись
5. Назад
    """
    manager = FinanceRecordManager()

    while True:
        print(menu)

        choice = input("Выберите действие (1/2/3/4/5/6/7): ")
        if choice == "1":
            amount = input("Введите размер операции: ")
            category = input("Введите категорию: ")
            description = input("Введите описание: ")
            manager.add_record(amount, category, description)
        elif choice == "2":
            fil_cat = input("Фильтровать по (категория / дата). Если не требуется фильтрация, то оставьте поле пустым: ")
            if fil_cat == "":
                manager.list_records()
            else:
                asc_desc = input("Фильтровать по (возрастание / убывание): ")
                manager.list_filtered_records(fil_cat, asc_desc)
        elif choice == "3":
            start = input("Введите начальную дату (дд-мм-гггг): ")
            end = input("Введите конечную дату (дд-мм-гггг): ")
            manager.generate_report(start, end)
        elif choice == "4":
            record_id = input("Введите id финансовой записи: ")
            manager.delete_record(record_id)
        elif choice == "5":
            break
        else:
            print("Такой опции нет!")


def calculator():
    menu = """
Калькулятор:
1. Сложение
2. Вычитание
3. Умножение
4. Деление
5. Назад
    """

    while True:
        print(menu)

        choice = input("Выберите действие (1/2/3/4/5): ")
        if choice in '1234':
            try:
                a = float(input("Введите первое число: "))
                b = float(input("Введите второе число: "))
                if choice == "1":
                    print(f"Результат: {a + b}")
                elif choice == "2":
                    print(f"Результат: {a - b}")
                elif choice == "3":
                    print(f"Результат: {a * b}")
                elif choice == "4":
                    if b == 0:
                        print("Ошибка: деление на ноль")
                    else:
                        print(f"Результат: {a / b}")
            except ValueError:
                print("Произошла ошибка!")
        elif choice == "5":
            break
        else:
            print("Такой опции нет!")


def main():
    menu = """
Добро пожаловать в Персональный помощник!
Выберите действие:
1. Управление заметками
2. Управление задачами
3. Управление контактами
4. Управление финансовыми записями
5. Калькулятор
6. Выход
    """
    while True:
        print(menu)

        choice = input("Выберите действие (1/2/3/4/5/6): ")
        if choice == "1":
            notes()
        elif choice == "2":
            tasks()
        elif choice == "3":
            contacts()
        elif choice == "4":
            finance_records()
        elif choice == "5":
            calculator()
        elif choice == "6":
            print("Не благодарите за помощь)\nХорошего дня!")
            return
        else:
            print("Такой опции нет!")


if __name__ == '__main__':
    main()
