"""
2.Задача: Расчет общей суммы расходов для пользователей с заданными критериями.
У вас есть список пользователей с информацией о их расходах за определенные периоды
времени. Вам нужно выполнить следующие шаги:
1. Отфильтровать пользователей по заданным критериям.
2. Для каждого пользователя рассчитать общую сумму его расходов.
3. Получить общую сумму расходов всех отфильтрованных пользователей."""
users = [
    {"name": "Alice", "expenses": [100, 50, 75, 200]},
    {"name": "Bob", "expenses": [50, 75, 80, 100]},
    {"name": "Charlie", "expenses": [200, 300, 50, 150]},
    {"name": "David", "expenses": [100, 200, 300, 400]},
    {"name": "Eva", "expenses": [75, 150, 200, 50]},
    {"name": "Frank", "expenses": [80, 90, 120, 75]},
    {"name": "Grace", "expenses": [250, 120, 180, 220]},
    {"name": "Hannah", "expenses": [60, 90, 110, 130]},
    {"name": "Isaac", "expenses": [180, 220, 250, 120]},
    {"name": "Jack", "expenses": [90, 110, 130, 60]},
    {"name": "Karen", "expenses": [300, 400, 100, 200]},
    {"name": "Liam", "expenses": [150, 200, 250, 100]},
    {"name": "Mia", "expenses": [120, 150, 75, 180]},
    {"name": "Noah", "expenses": [50, 75, 90, 120]},
    {"name": "Olivia", "expenses": [220, 250, 200, 120]},
    {"name": "Patrick", "expenses": [90, 110, 60, 130]},
    {"name": "Quinn", "expenses": [100, 200, 400, 300]},
    {"name": "Rachel", "expenses": [180, 75, 60, 220]},
    {"name": "Sam", "expenses": [150, 200, 120, 180]},
    {"name": "Tom", "expenses": [250, 100, 130, 75]}
]


from typing import Any


def criterion(elem: Any) -> bool:
    return True


users = list(filter(criterion, users))

counted_users = ((list(map(lambda x: {"name": x["name"], "total_expenses": sum(x["expenses"])}, users))))

filtered_users_sum = sum(list(map(lambda x: sum(x["expenses"]), users)))

print(users)
print(counted_users)
print(filtered_users_sum)