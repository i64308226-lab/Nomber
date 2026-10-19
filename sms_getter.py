import requests
import time

# Данные для доступа
API_KEY = "lw_UajEkyjbkndm3Bx-d0gSg54baQ-UF77lOo1i2hxn4F0"
BASE_URL = "https://sms-activate.org/stry.php"

# 1. Запрашиваем номер для конкретного сервиса (например, 'tg' - Telegram, 'go' - Google)
# country=0 — это Россия (код страны можно менять)
rent_response = requests.get(f"{BASE_URL}?api_key={API_KEY}&action=getNumber&service=tg&country=0")
# Ответ приходит в формате: ACCESS_NUMBER:$id:$number
data = rent_response.text.split(':')

if data[0] == "ACCESS_NUMBER":
    activation_id = data[1]
    phone_number = data[2]
    print(f"Успешно получен номер: {phone_number} (ID активации: {activation_id})")
    
    # 2. Теперь запускаем цикл ожидания SMS-кода
    print("Ожидание SMS...")
    for _ in range(30):  # Ждем максимум 5 минут (30 попыток по 10 секунд)
        time.sleep(10)
        
        status_response = requests.get(f"{BASE_URL}?api_key={API_KEY}&action=getStatus&id={activation_id}")
        status_data = status_response.text.split(':')
        
        # Если статус STATUS_OK, значит SMS пришло
        if status_data[0] == "STATUS_OK":
            sms_code = status_data[1]
            print(f"Код из SMS получен: {sms_code}")
            
            # Извещаем сервис, что код успешно принят и активация завершена
            requests.get(f"{BASE_URL}?api_key={API_KEY}&action=setStatus&status=6&id={activation_id}")
            break
        elif status_data[0] == "STATUS_WAIT_RETRY":
            print("Код еще не пришел, ждем...")
        else:
            print(f"Статус: {status_response.text}")
else:
    print(f"Ошибка при заказе номера: {rent_response.text}")
