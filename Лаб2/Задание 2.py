# Получение данных
price = float(input("Цена товара: "))
quantity = int(input("Количество: "))
discount_percent = float(input("Скидка (%): "))

# Вычисления
total_price = price * quantity
discount_amount = total_price * (discount_percent / 100)
final_price = total_price - discount_amount

# Вывод результатов
print(f"Стоимость без скидки: {total_price:.0f}")
print(f"Размер скидки: {discount_amount:.0f}")
print(f"К оплате: {final_price:.0f}")
