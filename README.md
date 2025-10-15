# intranet-tickets-api

API REST para el sistema de gestión de tickets de la intranet. Construida con Django y Django REST Framework.

## Características

- **Gestión completa de tickets**: Crear, leer, actualizar y eliminar tickets
- **Autenticación requerida**: API protegida con autenticación de Django
- **Panel de administración**: Django Admin configurado para gestión de tickets
- **Filtros y búsqueda**: Filtrar por estado, prioridad, usuario y buscar por título/descripción

## Tecnologías

- Python 3.12+
- Django 4.2
- Django REST Framework 3.14+
- PostgreSQL (configurado para producción)
- SQLite (por defecto para desarrollo)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/JoshyLop/intranet-tickets-api.git
cd intranet-tickets-api
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar migraciones:
```bash
python manage.py migrate
```

4. Crear superusuario:
```bash
python manage.py createsuperuser
```

5. Ejecutar servidor de desarrollo:
```bash
python manage.py runserver
```

## Modelo Ticket

El modelo `Ticket` incluye los siguientes campos:

- **titulo**: Título breve del ticket (CharField, max 200 caracteres)
- **descripcion**: Descripción detallada del problema o solicitud (TextField)
- **estado**: Estado actual del ticket (choices: abierto, en_progreso, resuelto, cerrado)
- **prioridad**: Prioridad del ticket (choices: baja, media, alta, critica)
- **usuario**: Relación ForeignKey con el usuario de Django que creó el ticket
- **creado_en**: Fecha y hora de creación (auto_now_add)
- **actualizado_en**: Fecha y hora de última actualización (auto_now)

## Endpoints API

### Base URL: `/api/`

#### Tickets

- `GET /api/tickets/` - Listar todos los tickets
- `POST /api/tickets/` - Crear nuevo ticket
- `GET /api/tickets/{id}/` - Obtener ticket específico
- `PUT /api/tickets/{id}/` - Actualizar ticket completo
- `PATCH /api/tickets/{id}/` - Actualizar ticket parcialmente
- `DELETE /api/tickets/{id}/` - Eliminar ticket

#### Parámetros de filtrado

- `?estado=abierto` - Filtrar por estado
- `?prioridad=alta` - Filtrar por prioridad
- `?usuario=1` - Filtrar por ID de usuario
- `?mis_tickets=true` - Mostrar solo tickets del usuario actual
- `?search=problema` - Buscar en título y descripción
- `?ordering=-creado_en` - Ordenar resultados

## Panel de Administración

Acceder al panel de administración en `/admin/` con las credenciales de superusuario.

Características del admin:
- Listado con filtros por estado, prioridad y fechas
- Búsqueda por título, descripción, usuario
- Campos organizados en fieldsets
- Campos de solo lectura para fechas

## Pruebas

Ejecutar las pruebas:
```bash
python manage.py test tickets
```

## Configuración para Producción

Para usar PostgreSQL en producción, actualizar `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'intranet_tickets_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
