# Ejemplos de Uso de la API de Tickets

## Autenticación

La API requiere autenticación. Puedes usar:
- Autenticación de sesión (Django)
- Autenticación básica (HTTP Basic Auth)

## Crear un Ticket

```bash
curl -X POST http://localhost:8000/api/tickets/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{
    "titulo": "Problema con el servidor",
    "descripcion": "El servidor web no responde desde las 10:00 AM",
    "estado": "abierto",
    "prioridad": "alta",
    "usuario": 1
  }'
```

## Listar Todos los Tickets

```bash
curl -X GET http://localhost:8000/api/tickets/ \
  -u username:password
```

## Obtener un Ticket Específico

```bash
curl -X GET http://localhost:8000/api/tickets/1/ \
  -u username:password
```

## Actualizar un Ticket

```bash
curl -X PUT http://localhost:8000/api/tickets/1/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{
    "titulo": "Problema con el servidor - RESUELTO",
    "descripcion": "El servidor web ha sido reiniciado y funciona correctamente",
    "estado": "resuelto",
    "prioridad": "alta",
    "usuario": 1
  }'
```

## Actualización Parcial (PATCH)

```bash
curl -X PATCH http://localhost:8000/api/tickets/1/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{
    "estado": "en_progreso"
  }'
```

## Eliminar un Ticket

```bash
curl -X DELETE http://localhost:8000/api/tickets/1/ \
  -u username:password
```

## Filtrar Tickets

### Por Estado

```bash
curl -X GET "http://localhost:8000/api/tickets/?estado=abierto" \
  -u username:password
```

### Por Prioridad

```bash
curl -X GET "http://localhost:8000/api/tickets/?prioridad=alta" \
  -u username:password
```

### Mis Tickets (del usuario autenticado)

```bash
curl -X GET "http://localhost:8000/api/tickets/?mis_tickets=true" \
  -u username:password
```

### Buscar en Título y Descripción

```bash
curl -X GET "http://localhost:8000/api/tickets/?search=servidor" \
  -u username:password
```

### Ordenar Resultados

```bash
# Ordenar por fecha de creación (más recientes primero)
curl -X GET "http://localhost:8000/api/tickets/?ordering=-creado_en" \
  -u username:password

# Ordenar por prioridad
curl -X GET "http://localhost:8000/api/tickets/?ordering=prioridad" \
  -u username:password
```

## Respuesta de la API

### Ejemplo de Respuesta de Ticket

```json
{
  "id": 1,
  "titulo": "Problema con el servidor",
  "descripcion": "El servidor web no responde desde las 10:00 AM",
  "estado": "abierto",
  "estado_display": "Abierto",
  "prioridad": "alta",
  "prioridad_display": "Alta",
  "usuario": 1,
  "usuario_detalle": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "User"
  },
  "creado_en": "2025-10-15T22:30:00Z",
  "actualizado_en": "2025-10-15T22:30:00Z"
}
```

## Usar con Python

```python
import requests

# Configuración
BASE_URL = "http://localhost:8000/api"
USERNAME = "admin"
PASSWORD = "admin123"

# Crear un ticket
response = requests.post(
    f"{BASE_URL}/tickets/",
    auth=(USERNAME, PASSWORD),
    json={
        "titulo": "Nuevo ticket desde Python",
        "descripcion": "Este ticket fue creado usando Python",
        "estado": "abierto",
        "prioridad": "media",
        "usuario": 1
    }
)
print(response.json())

# Listar tickets
response = requests.get(
    f"{BASE_URL}/tickets/",
    auth=(USERNAME, PASSWORD)
)
tickets = response.json()
print(f"Total de tickets: {len(tickets)}")
```

## Usar con JavaScript (Fetch API)

```javascript
const BASE_URL = 'http://localhost:8000/api';
const username = 'admin';
const password = 'admin123';

// Crear headers con autenticación básica
const headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Basic ' + btoa(username + ':' + password)
};

// Crear un ticket
fetch(`${BASE_URL}/tickets/`, {
  method: 'POST',
  headers: headers,
  body: JSON.stringify({
    titulo: 'Ticket desde JavaScript',
    descripcion: 'Creado con Fetch API',
    estado: 'abierto',
    prioridad: 'media',
    usuario: 1
  })
})
  .then(response => response.json())
  .then(data => console.log('Ticket creado:', data))
  .catch(error => console.error('Error:', error));

// Listar tickets
fetch(`${BASE_URL}/tickets/`, {
  method: 'GET',
  headers: headers
})
  .then(response => response.json())
  .then(data => console.log('Tickets:', data))
  .catch(error => console.error('Error:', error));
```

## Estados Disponibles

- `abierto`: Abierto
- `en_progreso`: En Progreso
- `resuelto`: Resuelto
- `cerrado`: Cerrado

## Prioridades Disponibles

- `baja`: Baja
- `media`: Media
- `alta`: Alta
- `critica`: Crítica
