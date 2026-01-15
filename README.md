# PlayZone (Django 5 + PostgreSQL 16)

Projeto PlayZone com:
- Django >= 5 (MTV)
- PostgreSQL >= 16 via Docker Compose
- Bootstrap 5 + customização via SASS
- Autenticação (login/registo/reset)
- Regras de negócio + Admin custom pages

## Requisitos
- Docker + Docker Compose

## Setup rápido

1) Criar ficheiros .env
cp .env.example .env
cp .env.db.example .env.db

2) Subir o projeto
docker compose up -d --build

3)Ver logs
docker compose logs -f web

#Comandos úteis
-Down
docker compose down

-Migrações
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

-Criar superuser
docker compose exec web python manage.py createsuperuser
