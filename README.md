## Smart Task Scheduler
### Steps to update db:
  ```
    alembic init alembic
    alembic revision --autogenerate -m "msg"
    alembic upgrade head 
  ```