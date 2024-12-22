Домашная работа по сборке проекта в контейнеры Docker


1) Клонируете данный проект к себе на рабочую станцию
2) Настройте переменные окружения по шаблону ".env.sample"
3) Произведите запуск сборки контейнеров с помощью команду `docker compose up -d --build`
4) После удачной сборки контейнера используйте данную команду загрузки фикстур`docker compose exec app python3 manage.py loaddata ./fixtures/fixture3.json && docker compose exec app python3 manage.py loaddata ./fixtures/fixture2.json && 
docker compose exec app python3 manage.py loaddata ./fixtures/fixture1.json && 
docker compose exec app python3 manage.py loaddata ./fixtures/fixture4.json`
%% Порядок команд не изменять во избежание сбоя!!! %%