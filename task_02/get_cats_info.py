"""
    Функція зчитує файл із даними про котів і повертає список словників.
    Кожен рядок файлу має формат: id,name,age.
    Результат роботи функції — список такого вигляду:
    [{"id": "60b90c1c13067a15887e1ae1", "name": "Tayson", "age": 3}, ...]
    Якщо файл не знайдено або якийсь рядок має некоректний формат, виводиться повідомлення про помилку.
"""

def get_cats_info(path: str) -> list[dict]:

    result = []  # список для збереження інформації про котів

    try:
        # Відкриваємо файл для читання
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()  # прибираємо пробіли та символ \n

                if line:  # пропускаємо порожні рядки
                    try:
                        # Розділяємо рядок на id, name, age
                        id, name, age = line.split(",")

                        # Формуємо словник для одного кота
                        our_cats = {
                            "id": id,           # ідентифікатор (рядок)
                            "name": name,       # ім’я кота
                            "age": int(age)     # вік (число)
                        }
                        result.append(our_cats)

                    except ValueError:
                        # Якщо рядок некоректний — повідомляємо користувача
                        print(f"Помилка у рядку: {line}")

    except FileNotFoundError:
        # Якщо файл не знайдено — повідомляємо і повертаємо 0
        print("Файл не знайдено.")
        return 0

    return result


# Приклад виклику
cats = get_cats_info("/Users/cordial/Documents/hw_4/task_02/cats.txt")
print(cats)
