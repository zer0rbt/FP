"""Задача: Работа с большой базой данных заказов и клиентов.
Предположим, у вас есть большая база данных заказов и клиентов, представленных в виде
списков словарей. Вам нужно выполнить следующие операции:
1. Фильтрация заказов: Отфильтровать заказы только для определенного клиента с
заданным идентификатором клиента.
2. Подсчет суммы заказов: Подсчитать общую сумму всех заказов для данного
клиента.
3. Подсчет средней стоимости заказов: Найти среднюю стоимость заказов для
данного клиента."""
orders = [
    {"order_id": 1, "customer_id": 101, "amount": 150.0},
    {"order_id": 2, "customer_id": 102, "amount": 200.0},
    {"order_id": 3, "customer_id": 101, "amount": 75.0},
    {"order_id": 4, "customer_id": 103, "amount": 100.0},
    {"order_id": 5, "customer_id": 101, "amount": 50.0},
    {"order_id": 6, "customer_id": 104, "amount": 120.0},
    {"order_id": 7, "customer_id": 102, "amount": 90.0},
    {"order_id": 8, "customer_id": 105, "amount": 180.0},
    {"order_id": 9, "customer_id": 101, "amount": 95.0},
    {"order_id": 10, "customer_id": 106, "amount": 70.0},
    {"order_id": 11, "customer_id": 102, "amount": 110.0},
    {"order_id": 12, "customer_id": 107, "amount": 130.0},
    {"order_id": 13, "customer_id": 101, "amount": 45.0},
    {"order_id": 14, "customer_id": 108, "amount": 160.0},
    {"order_id": 15, "customer_id": 102, "amount": 75.0},
    {"order_id": 16, "customer_id": 109, "amount": 140.0},
    {"order_id": 17, "customer_id": 101, "amount": 55.0},
    {"order_id": 18, "customer_id": 110, "amount": 170.0},
    {"order_id": 19, "customer_id": 102, "amount": 85.0},
    {"order_id": 20, "customer_id": 111, "amount": 150.0}
]


id = 102
print(list(filter(lambda x: (x["customer_id"] == id), orders)))

print(sum(list(map(lambda x: int(x["amount"]), list(filter(lambda x: (x["customer_id"] == id), orders))))))

print(sum(list(map(lambda x: int(x["amount"]), list(filter(lambda x: (x["customer_id"] == id), orders))))) / len(
    list(map(lambda x: int(x["amount"]), list(filter(lambda x: (x["customer_id"] == id), orders))))))
