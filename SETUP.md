# 🚀 Guía de Instalación y Configuración
# Sistema de Tickets - API RESTful

Esta guía te llevará paso a paso para instalar y configurar el proyecto desde cero.

---

## ✅ Checklist de Instalación

- [ ] Crear entorno virtual
- [ ] Instalar dependencias de Python
- [ ] Configurar variables de entorno
- [ ] Instalar y configurar PostgreSQL
- [ ] Crear proyecto Django
- [ ] Ejecutar migraciones
- [ ] Crear superusuario
- [ ] Probar servidor de desarrollo

---

## 📦 Dependencias del Proyecto

### Python (Versión mínima: 3.10)

#### Framework Principal
- [ ] **Django 4.2+** - Framework web principal
- [ ] **djangorestframework 3.14+** - Para crear la API REST

#### Base de Datos
- [ ] **psycopg2-binary 2.9+** - Adaptador de PostgreSQL para Python

#### Autenticación y Seguridad
- [ ] **djangorestframework-simplejwt 5.3+** - Autenticación JWT
- [ ] **django-cors-headers 4.3+** - Manejo de CORS para el frontend

#### Utilidades
- [ ] **python-decouple 3.8+** - Gestión de variables de entorno
- [ ] **django-filter 23.5+** - Filtrado avanzado en la API
- [ ] **Pillow 10.1+** - Procesamiento de imágenes (avatares, adjuntos)

### Herramientas Externas
- [ ] **PostgreSQL 12+** - Base de datos

---

## 🔧 Pasos de Instalación

### 1. Crear Entorno Virtual

```powershell
# Navegar a la carpeta del proyecto
cd c:\Users\AuxSistemas3\Documents\GitHub\intranet-tickets-api

# Crear entorno virtual
python -m venv venv

# Si es la primera vez, habilitar scripts en PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activar entorno virtual (usa el símbolo & antes de la ruta)
& .\venv\Scripts\Activate.ps1

# Deberías ver (venv) al inicio de tu línea de comando
```

**Estado:** ⏳ Pendiente

---

### 2. Instalar Dependencias de Python

Una vez activado el entorno virtual:

```powershell
# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

**Estado:** ⏳ Pendiente

**Nota:** Después de este paso, los errores de importación en VS Code desaparecerán.

---

### 3. Instalar PostgreSQL

#### Opción A: Instalación Local
1. Descargar desde: https://www.postgresql.org/download/windows/
2. Instalar con las opciones por defecto
3. Recordar la contraseña del usuario `postgres`

#### Opción B: Usar Docker (Opcional)
```powershell
docker run --name tickets-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15
```

**Estado:** ⏳ Pendiente

---

### 4. Configurar Variables de Entorno

```powershell
# Copiar el archivo de ejemplo
copy .env.example .env

# Editar el archivo .env con tus datos
notepad .env
```

**Configuración mínima en `.env`:**
```
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
DB_NAME=tickets_db
DB_USER=postgres
DB_PASSWORD=tu_contraseña_postgres
DB_HOST=localhost
DB_PORT=5432
```

**Estado:** ⏳ Pendiente

---

### 5. Crear Base de Datos en PostgreSQL

```powershell
# Conectar a PostgreSQL (en cmd o PowerShell)
psql -U postgres

# Dentro de psql, ejecutar:
CREATE DATABASE tickets_db;
\q
```

**Estado:** ⏳ Pendiente

---

### 6. Crear Estructura de Django

```powershell
# Crear las migraciones (traduce los modelos a SQL)
python manage.py makemigrations

# Aplicar las migraciones (crea las tablas en la BD)
python manage.py migrate
```

**Estado:** ⏳ Pendiente

**Qué hace esto:**
- `makemigrations`: Lee tus modelos y crea un "plan" de la base de datos
- `migrate`: Ejecuta ese plan y crea las tablas reales en PostgreSQL

---

### 7. Crear Superusuario (Administrador)

```powershell
python manage.py createsuperuser

# Te pedirá:
# - Username: (elige uno)
# - Email: tu_email@ejemplo.com
# - Password: (elige una contraseña segura)
```

**Estado:** ⏳ Pendiente

**Nota:** Este usuario te permitirá acceder al panel de administración de Django.

---

### 8. Iniciar Servidor de Desarrollo

```powershell
python manage.py runserver

# Deberías ver:
# Starting development server at http://127.0.0.1:8000/
```

**Acceder a:**
- API: http://127.0.0.1:8000/api/
- Admin: http://127.0.0.1:8000/admin/

**Estado:** ⏳ Pendiente

---

## 🎯 Próximos Pasos (Después de la instalación)

Una vez que todo esté instalado y funcionando:

1. [ ] Crear serializadores DRF
2. [ ] Implementar vistas de la API
3. [ ] Configurar URLs de la API
4. [ ] Personalizar Django Admin
5. [ ] Probar endpoints con Postman o navegador
6. [ ] Conectar con el frontend

---

## ❓ Solución de Problemas Comunes

### Error: "Django no está instalado"
**Solución:** Asegúrate de tener activado el entorno virtual y ejecuta `pip install -r requirements.txt`

### Error: "No module named psycopg2"
**Solución:** Instala el adaptador de PostgreSQL: `pip install psycopg2-binary`

### Error: "FATAL: database does not exist"
**Solución:** Crea la base de datos en PostgreSQL: `CREATE DATABASE tickets_db;`

### Error: "ImportError: Could not import decouple"
**Solución:** Instala python-decouple: `pip install python-decouple`

### Error en migraciones
**Solución:** 
```powershell
# Eliminar migraciones anteriores
Remove-Item tickets\migrations\*.py -Exclude __init__.py
# Volver a crear
python manage.py makemigrations
python manage.py migrate
```

---

## 📝 Comandos Útiles

```powershell
# Ver versión de Django instalada
python -m django --version

# Ver todas las migraciones
python manage.py showmigrations

# Crear datos de prueba (shell interactivo)
python manage.py shell

# Recolectar archivos estáticos
python manage.py collectstatic

# Ver todas las URLs disponibles
python manage.py show_urls  # (requiere django-extensions)
```

---

## 📞 ¿Necesitas ayuda?

Si te atoras en algún paso, dime en cuál y te ayudo a resolverlo paso a paso.

**Última actualización:** 15 de Octubre, 2025
