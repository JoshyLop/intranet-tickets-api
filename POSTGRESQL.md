# 🗄️ Guía Rápida de PostgreSQL

## ✅ Checklist de Instalación

- [ ] Descargar PostgreSQL desde: https://www.postgresql.org/download/windows/
- [ ] Ejecutar el instalador
- [ ] Anotar la contraseña del usuario `postgres`
- [ ] Dejar puerto por defecto: `5432`
- [ ] Verificar que el servicio está corriendo
- [ ] Crear la base de datos `tickets_db`

---

## 📋 Configuración Post-Instalación

### Opción 1: Usar el Script Automático (Recomendado)

```powershell
# Ejecutar el script de configuración
.\setup_database.ps1
```

### Opción 2: Configuración Manual

```powershell
# 1. Abrir psql (cliente de PostgreSQL)
psql -U postgres

# 2. Dentro de psql, ejecutar:
CREATE DATABASE tickets_db;

# 3. Verificar que se creó
\l

# 4. Salir
\q
```

---

## 🔧 Comandos Útiles de PostgreSQL

### Verificar si PostgreSQL está corriendo

```powershell
# Ver servicios de PostgreSQL
Get-Service -Name postgresql*
```

### Conectar a la base de datos

```powershell
# Conectar con psql
psql -U postgres -d tickets_db
```

### Comandos dentro de psql

```sql
-- Listar todas las bases de datos
\l

-- Listar todas las tablas
\dt

-- Ver estructura de una tabla
\d nombre_tabla

-- Ejecutar consulta
SELECT * FROM tickets_ticket;

-- Salir
\q
```

---

## ❓ Solución de Problemas

### Error: "psql no se reconoce como comando"

**Solución:** Agregar PostgreSQL al PATH

```powershell
# Agregar al PATH temporalmente
$env:Path += ";C:\Program Files\PostgreSQL\16\bin"

# O permanentemente (ejecutar como administrador)
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\PostgreSQL\16\bin", "Machine")
```

### Error: "FATAL: password authentication failed"

**Solución:** Verifica que estás usando la contraseña correcta. Si la olvidaste:

1. Buscar el archivo `pg_hba.conf`
2. Cambiar `md5` por `trust` temporalmente
3. Reiniciar el servicio
4. Cambiar la contraseña
5. Volver a poner `md5`

### El servicio no inicia

```powershell
# Iniciar el servicio manualmente
Start-Service postgresql-x64-16

# O desde servicios.msc
services.msc
```

---

## 🔐 Configurar Variables de Entorno

Después de instalar PostgreSQL, verifica tu archivo `.env`:

```env
DB_NAME=tickets_db
DB_USER=postgres
DB_PASSWORD=TU_CONTRASEÑA_AQUI  ← Cambiar esto
DB_HOST=localhost
DB_PORT=5432
```

---

## ✅ Verificar Instalación Completa

```powershell
# 1. Verificar versión
psql --version

# 2. Verificar servicio
Get-Service postgresql*

# 3. Conectar y probar
psql -U postgres -d tickets_db -c "SELECT version();"
```

Si todos estos comandos funcionan, ¡estás listo! 🎉

---

## 🚀 Siguiente Paso

Una vez PostgreSQL esté instalado y configurado:

```powershell
# Aplicar las migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```
