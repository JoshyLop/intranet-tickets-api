# 🎨 Frontend - Sistema de Tickets

Este es el frontend del sistema de tickets, creado con **HTML, CSS y JavaScript puro** (sin frameworks).

---

## 📁 Estructura de Archivos

```
frontend/
├── index.html          # Página de login
├── dashboard.html      # Lista de tickets del usuario
├── create-ticket.html  # Formulario para crear tickets
├── ticket-detail.html  # Ver detalle de un ticket y comentarios
├── css/
│   └── styles.css      # Estilos globales
└── js/
    └── api.js          # Funciones para comunicarse con la API
```

---

## 🚀 Cómo Usar

### **Paso 1: Iniciar el Backend**

Primero, asegúrate de que tu API de Django esté corriendo:

```powershell
# Activar el entorno virtual
& .\venv\Scripts\Activate.ps1

# Iniciar el servidor
python manage.py runserver
```

Tu API estará disponible en: http://127.0.0.1:8000

---

### **Paso 2: Abrir el Frontend**

#### **Opción A: Abrir directamente en el navegador**

1. Ve a la carpeta `frontend`
2. Haz doble clic en `index.html`
3. Se abrirá en tu navegador predeterminado

#### **Opción B: Usar Live Server (Recomendado)**

Si tienes Visual Studio Code:

1. Instala la extensión "Live Server"
2. Haz clic derecho en `index.html`
3. Selecciona "Open with Live Server"
4. Se abrirá en http://127.0.0.1:5500

---

## 🔐 Credenciales de Prueba

Usa las credenciales del superusuario que creaste:

- **Usuario**: `auxsistemas3` (o el que hayas creado)
- **Contraseña**: La que configuraste

---

## 📄 Páginas Disponibles

### **1. Login (index.html)**
- Página de inicio de sesión
- Obtiene el token JWT de la API
- Redirige al dashboard después del login exitoso

### **2. Dashboard (dashboard.html)**
- Muestra todos los tickets del usuario actual
- Permite filtrar por estado, prioridad y buscar
- Click en cualquier ticket para ver detalles

### **3. Crear Ticket (create-ticket.html)**
- Formulario para crear nuevos tickets
- Campos: título, descripción, prioridad, asignar a
- Validaciones del lado del cliente
- Redirige al detalle después de crear

### **4. Detalle de Ticket (ticket-detail.html)**
- Muestra toda la información del ticket
- Lista de comentarios
- Formulario para agregar comentarios
- Botón para cerrar ticket

---

## 🎨 Características

### **Autenticación**
- ✅ Login con JWT tokens
- ✅ Token guardado en localStorage
- ✅ Redirección automática si no está autenticado
- ✅ Botón de logout en todas las páginas

### **Gestión de Tickets**
- ✅ Ver todos mis tickets
- ✅ Crear nuevos tickets
- ✅ Ver detalles completos
- ✅ Cerrar tickets
- ✅ Filtrar por estado y prioridad
- ✅ Buscar por palabra clave

### **Comentarios**
- ✅ Ver todos los comentarios de un ticket
- ✅ Agregar nuevos comentarios
- ✅ Marca de tiempo y autor

### **UI/UX**
- ✅ Diseño responsive (funciona en móviles)
- ✅ Badges de colores para estados y prioridades
- ✅ Mensajes de error y éxito
- ✅ Loading spinners
- ✅ Validaciones en formularios

---

## 🔧 Personalización

### **Cambiar la URL de la API**

Edita `js/api.js` y cambia la constante:

```javascript
const API_BASE_URL = 'http://127.0.0.1:8000/api';
```

Por ejemplo, si subes tu API a producción:

```javascript
const API_BASE_URL = 'https://tu-dominio.com/api';
```

### **Cambiar Colores**

Edita `css/styles.css` y modifica las variables CSS:

```css
:root {
    --primary-color: #4F46E5;      /* Color principal */
    --secondary-color: #10B981;    /* Color secundario */
    --danger-color: #EF4444;       /* Color de peligro */
    --warning-color: #F59E0B;      /* Color de advertencia */
}
```

---

## 🐛 Solución de Problemas

### **Error: "No se pueden cargar los tickets"**
- ✅ Verifica que el backend esté corriendo
- ✅ Revisa la consola del navegador (F12) para ver el error exacto
- ✅ Asegúrate de que CORS esté configurado en Django

### **Error: "Las credenciales de autenticación no se proveyeron"**
- ✅ Asegúrate de haber iniciado sesión
- ✅ Revisa que el token esté guardado en localStorage (F12 > Application > Local Storage)

### **Los estilos no se cargan**
- ✅ Verifica que la ruta de `css/styles.css` sea correcta
- ✅ Usa Live Server en lugar de abrir directamente el archivo

### **Error CORS**
Tu backend debe tener configurado CORS. En `config/settings.py` debe estar:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5500",      # Live Server
    "http://127.0.0.1:5500",
    "http://localhost:3000",      # Si usas React
]
```

---

## 📚 Próximos Pasos

### **Funcionalidades que puedes agregar:**

1. **Editar tickets** - Agregar página para editar tickets existentes
2. **Eliminar tickets** - Permitir eliminar tickets (solo admin)
3. **Perfil de usuario** - Página para ver/editar perfil
4. **Notificaciones** - Mostrar alertas cuando hay nuevos comentarios
5. **Adjuntar archivos** - Permitir subir imágenes/archivos
6. **Dashboard de estadísticas** - Gráficas con tickets por estado
7. **Búsqueda avanzada** - Filtros más específicos
8. **Paginación** - Cuando hay muchos tickets

---

## 💡 Consejos

1. **Usa la consola del navegador (F12)** para ver errores de JavaScript
2. **Revisa la pestaña Network** para ver las peticiones a la API
3. **localStorage** guarda el token - puedes verlo en F12 > Application
4. **Inspecciona elementos** para ver cómo está estructurado el HTML

---

## 🎓 Para Aprender Más

Este proyecto usa:
- **HTML5** - Estructura de las páginas
- **CSS3** - Estilos y diseño
- **JavaScript ES6+** - Lógica y comunicación con la API
- **Fetch API** - Para hacer peticiones HTTP
- **LocalStorage** - Para guardar el token
- **Async/Await** - Para manejar promesas

---

¡Feliz desarrollo! 🚀
