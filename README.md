
# Тестовое для компании Сима-ленд


### Описание проекта:

Файл data_base создает базу данных и 2 таблицы: 'permissions' и 'users', затем их заполнит по умолчанию. 
Работать с API CRUD можно через консоль или по средствам других приложений(postman, paw и д.р.)


### Как запустить:
 - запустите файл data_base 
 - запустите файл backend

### Доступные адреса для работы с CRUD:
- для просмотра пользователей перейдите по адресу http://localhost:8080/
- для создания пользователя http://localhost:8080/create
- для удаления пользователя http://localhost:8080/delete
- для удаления права в таблице 'permissions' http://localhost:8080/delete_permission

### Стек технологий использованный в проекте:
- Python 3.9
- SQLAlchemy
- asyncio
- aiohttp 
- PostgreSQL

### Для работы с базой данных создайте файл .env c такими данными или используйте свои значения:
  ```
  - NAME=test_db
  - USER=postgres
  - PASSWORD=postgres
  - HOST=localhost
  - PORT=5432
  ```

