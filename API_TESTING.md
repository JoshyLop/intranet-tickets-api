# 🧪 Guía para Probar la API

Esta guía te muestra cómo probar la API REST del sistema de tickets.

---

## 📋 Credenciales

**Usuario creado:**
- **Username**: `auxsistemas3`
- **Email**: `auxsistemas@refaccionariagadi.com`
- **Password**: La que configuraste al crear el superusuario

---

## 🚀 Método 1: Interfaz Web de Django REST Framework (FÁCIL)

### Paso 1: Iniciar sesión en Django Admin
1. Ve a: http://127.0.0.1:8000/admin/
2. Inicia sesión con tu usuario y contraseña
3. ¡Listo! Ya estás autenticado

### Paso 2: Navegar por la API
Ahora puedes visitar cualquier endpoint y la interfaz web te permitirá hacer peticiones:
- http://127.0.0.1:8000/api/tickets/
- http://127.0.0.1:8000/api/comments/
- http://127.0.0.1:8000/api/profiles/
- http://127.0.0.1:8000/api/users/

**En cada página verás:**
- Lista de recursos (GET)
- Formularios para crear (POST)
- Botones para editar/eliminar

---

## 🔐 Método 2: Usando JWT Tokens (Para Postman/Thunder Client/Frontend)

### Paso 1: Obtener el Token de Acceso

**Endpoint:** `POST http://127.0.0.1:8000/api/token/`

**Body (JSON):**
```json
{
  "username": "auxsistemas3",
  "password": "tu_contraseña_aquí"
}
```

**Respuesta esperada:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Paso 2: Usar el Token en las Peticiones

Para todas las demás peticiones, incluye el header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## 📝 Ejemplos de Peticiones

### 1. Listar todos los tickets
```http
GET http://127.0.0.1:8000/api/tickets/
Authorization: Bearer <tu_token>
```

### 2. Crear un nuevo ticket
```http
POST http://127.0.0.1:8000/api/tickets/
Authorization: Bearer <tu_token>
Content-Type: application/json

{
  "title": "Problema con la impresora del piso 2",
  "description": "La impresora HP del piso 2 no imprime. Dice que está fuera de línea.",
  "priority": "alta"
}
```

### 3. Ver mis tickets
```http
GET http://127.0.0.1:8000/api/tickets/my-tickets/
Authorization: Bearer <tu_token>
```

### 4. Ver detalle de un ticket
```http
GET http://127.0.0.1:8000/api/tickets/1/
Authorization: Bearer <tu_token>
```

### 5. Agregar un comentario a un ticket
```http
POST http://127.0.0.1:8000/api/comments/
Authorization: Bearer <tu_token>
Content-Type: application/json

{
  "ticket": 1,
  "content": "Ya revisé la impresora, el cable de red estaba desconectado.",
  "is_internal": false
}
```

### 6. Cerrar un ticket
```http
POST http://127.0.0.1:8000/api/tickets/1/close/
Authorization: Bearer <tu_token>
```

### 7. Ver mi perfil
```http
GET http://127.0.0.1:8000/api/profiles/me/
Authorization: Bearer <tu_token>
```

---

## 🔄 Refrescar el Token (cuando expire)

Los tokens de acceso expiran después de **1 hora**. Cuando expire, usa el refresh token:

```http
POST http://127.0.0.1:8000/api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Respuesta:**
```json
{
  "access": "nuevo_token_aquí..."
}
```

---

## 🎨 Usando Thunder Client en VS Code

Thunder Client es una extensión de VS Code similar a Postman.

### Instalación:
1. En VS Code, ve a Extensiones (Ctrl+Shift+X)
2. Busca "Thunder Client"
3. Instala la extensión

### Crear una colección:

1. **Request 1: Login**
   - Method: `POST`
   - URL: `http://127.0.0.1:8000/api/token/`
   - Body (JSON):
     ```json
     {
       "username": "auxsistemas3",
       "password": "tu_contraseña"
     }
     ```
   - Guarda el `access` token que te devuelve

2. **Request 2: Listar Tickets**
   - Method: `GET`
   - URL: `http://127.0.0.1:8000/api/tickets/`
   - Headers:
     - `Authorization`: `Bearer <pega_aquí_tu_token>`

3. **Request 3: Crear Ticket**
   - Method: `POST`
   - URL: `http://127.0.0.1:8000/api/tickets/`
   - Headers:
     - `Authorization`: `Bearer <tu_token>`
     - `Content-Type`: `application/json`
   - Body (JSON):
     ```json
     {
       "title": "Nuevo ticket de prueba",
       "description": "Este es un ticket de prueba desde Thunder Client",
       "priority": "media"
     }
     ```

---

## 📊 Filtros Disponibles

### Tickets:
- `?status=abierto` - Solo tickets abiertos
- `?status=cerrado` - Solo tickets cerrados
- `?priority=alta` - Solo alta prioridad
- `?search=impresora` - Buscar por palabra clave
- `?ordering=-created_at` - Ordenar por fecha (más recientes primero)

**Ejemplos:**
```
GET http://127.0.0.1:8000/api/tickets/?status=abierto&priority=alta
GET http://127.0.0.1:8000/api/tickets/?search=impresora
GET http://127.0.0.1:8000/api/tickets/?ordering=-created_at
```

### Comentarios:
- `?ticket=1` - Comentarios de un ticket específico
- `?is_internal=true` - Solo comentarios internos

---

## ❌ Errores Comunes

### Error 401: "Las credenciales de autenticación no se proveyeron"
**Causa:** No incluiste el token en el header
**Solución:** Agrega `Authorization: Bearer <tu_token>`

### Error 403: "No tienes permisos..."
**Causa:** Tu usuario no tiene permisos para esa acción
**Solución:** Verifica que tu usuario sea staff/admin si es necesario

### Error 400: Validación fallida
**Causa:** Los datos enviados no cumplen con las validaciones
**Solución:** Lee el mensaje de error, te dirá qué campo está mal

---

## 💡 Consejos

1. **Primero prueba en el navegador** (Método 1) - es más fácil para empezar
2. **Usa Thunder Client** para pruebas más avanzadas
3. **Guarda los tokens** - duran 1 hora antes de expirar
4. **Lee los mensajes de error** - Django REST Framework da mensajes muy claros
5. **Consulta la documentación automática** en http://127.0.0.1:8000/api/

---

## 🎯 Próximos Pasos

Una vez que te familiarices con la API, puedes:

1. Crear tickets desde Postman/Thunder Client
2. Integrarla con tu frontend (React, Vue, etc.)
3. Personalizar los permisos y validaciones
4. Agregar más funcionalidades según tus necesidades

¡Buena suerte! 🚀
