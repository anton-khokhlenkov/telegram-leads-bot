import requests

SHEET_URL = "https://api.sheetbest.com/sheets/131279a2-25f6-43af-bf36-272ba232dfd5"  # замени на свой URL

data = {
    "Имя": "Тест Антон",
    "Телефон": "+79215994989",
    "Услуга": "Проверка API"
}

response = requests.post(SHEET_URL, json=data)

if response.status_code == 200:
    print("✅ Успешно отправлено!")
else:
    print("❌ Ошибка:", response.status_code)
