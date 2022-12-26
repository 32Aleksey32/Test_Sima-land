
# Тестовое для компании Сима-ленд


### Как запустить:
 - запустите файл data_base (он создает базу данных и 2 таблицы: 'permissions' и 'users', затем их заполняет по умолчанию.)
 - запустите файл backend (позволяет работать с базой данных)

### Как работать с API CRUD:
Работать с API CRUD можно через консоль или по средствам других приложений(postman, paw и д.р.)

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

### Для работы с базой данных создайте файл .env со своими значениями или используйте данные по умолчанию:
  ```
  - NAME=test_db
  - USER=postgres
  - PASSWORD=postgres
  - HOST=localhost
  - PORT=5432
  ```


