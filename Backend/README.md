# Comandos para levantar el contenedor para desarrollo

- docker-compose build
- docker-compose up
- docker-compose run web python manage.py migrate

# Crear super usuario

- docker-compose run web python manage.py migrate

# Actualmente se cuenta con hot reloading pero ojo

- .El autoreload de Django no siempre detecta cambios si agregas nuevos archivos o cambias configuraciones muy internas → en esos casos hay que reiniciar el contenedor.

. En modo producción no se usa runserver, se usa gunicorn o uvicorn → y ahí normalmente no hay hot reload.

# Proceso para realizar las migraciones

- docker exec -it stockify-django python manage.py migrate
- docker exec -it stockify-django python manage.py makemigrations
