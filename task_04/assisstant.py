"""
    Цей скрипт реалізує асистента для роботи з контактами.
    Він дозволяє додавати, змінювати, виводити номер телефону для вказаного контакту та всі контакти.
    Програма працює в циклі, доки користувач не введе команду "close" або "exit".
    Контакти зберігаються в файлі contacts.json.
    Формат файлу:
    {
        "name": "phone",
        "name2": "phone2"
        ...
    }
    Приклад файлу:
    {
        "John": "1234567890",
        "Jane": "0987654321"
    }
"""

# ----------------------------------------------
# Імпортуємо необхідні модулі
# json - для роботи з JSON-файлами
# pathlib - для роботи з файлами і директоріями
# re - для регулярних виразів
import json
from pathlib import Path
import re

# Константа — шлях до файлу, де зберігаються контакти
CONTACTS_FILE = Path("contacts.json")

# Текст для повідомлень про помилки формату
pattern = "Please follow the pattern:"

# Текст із підказками для користувача
HELP_TEXT = """\
Commands:
  hello
      Output: How can I help you?

  add <name> <phone>
      Example: add John 1234567890
      Output: Contact has been added.

  change <name> <new_phone>
      Example: change John 0987654321
      Output: Contact has been updated. або Contact is not found.

  phone <name>
      Example: phone John
      Output: <phone> або Contact is not found.

  all
      Output: All the contacts "<name>: <phone>" або "No contacts."

  help
      Display this text.

  close | exit
      Output: Goodbye! and the end of work.
"""


# -------------------------------------------------------------------
# Завантажуємо контакти з JSON-файлу, якщо він існує.
# Якщо файл не знайдено або пошкоджений — повертаємо порожній словник.
def load_contacts(path: Path = CONTACTS_FILE) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# ------------------------------------------
# Нормалізуємо номер телефону:
#   - видаляємо всі символи, крім цифр і '+'
#   - додаємо міжнародний код, якщо потрібно
def normalize_phone(phone_number):
    pattern = r"[^\d\+]"
    clean_number = re.sub(pattern, "", phone_number)
    if clean_number.startswith("+"):
        pass
    elif clean_number.startswith("380"):
        clean_number = "+" + clean_number
    elif clean_number.startswith("80"):
        clean_number = "+3" + clean_number
    else:
        clean_number = "+38" + clean_number
    return clean_number


# ----------------------------------------
# Зберігаємо словник контактів у файл JSON
def save_contacts(contacts: dict, path: Path = CONTACTS_FILE) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)


# ------------------------------------------------------------
# Розбираємо введення користувача:
# повертаємо команду (у нижньому регістрі) і список аргументів
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# --------------------------------------------------------
# Додаємо новий контакт у словник (або оновлюємо існуючий)
def add_contact(args, contacts):
    if len(args) != 2:
        return f"{pattern} add <name> <phone>"
    name, phone = args
    contacts[name] = normalize_phone(phone)
    save_contacts(contacts)
    return "Contact has been added."


# -------------------------------------------------
# Змінюємо існуючий у файлі номер телефону контакту
def change_contact(args, contacts):
    if len(args) != 2:
        return f"{pattern} change <name> <phone>"
    name, phone = args
    if name not in contacts:
        return "Contact is not found."
    contacts[name] = normalize_phone(phone)
    save_contacts(contacts)
    return "Contact has been updated."


# ---------------------------------
# Виводимо номер телефону за іменем
def show_phone(args, contacts):
    if len(args) != 1:
        return f"{pattern} phone <name>"
    name, = args
    return contacts.get(name, "Contact is not found.")


# ---------------------------------------------------------------
# Виводимо усі збережені контакти або повідомлення, якщо їх немає
def show_all(contacts):
    if not contacts:
        return "There are no contacts."
    return "\n".join(f"{n}: {p}" for n, p in contacts.items())


# -----------------------------------------------
# Основна функція — цикл взаємодії з користувачем
def main():
    contacts = load_contacts()
    print("Welcome to the assistant bot!")
    print("Enter 'help' to see the list of the commands.")
    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            print("Invalid command. Enter 'help' for reference.")
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Goodbye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "help":
            print(HELP_TEXT)
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command. Enter 'help' for reference.")


# ---------------------------------------------------------------------------
# Виконати main() лише якщо файл запущено напряму, а не імпортовано як модуль
if __name__ == "__main__":
    main()
