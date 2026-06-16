# 2. Создаём виртуальное окружение через py
py -m venv venv

# 3. Активируем окружение
.\venv\Scripts\Activate.ps1

# Создаём приложения
python manage.py startapp documents
python manage.py startapp approvals


=====================================================================================

## Как запустить проект локально

```powershell
# 1. Активировать окружение
.\venv\Scripts\Activate.ps1

# 2. Установить зависимости (пока только Django)
pip install django

# 3. Применить миграции
python manage.py migrate

# 4. Создать суперпользователя
python manage.py createsuperuser

# 5. Запустить сервер
python manage.py runserver