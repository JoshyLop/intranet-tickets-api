# Script para configurar PostgreSQL
# Ejecutar despues de instalar PostgreSQL

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Configuracion de PostgreSQL" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si psql esta instalado
Write-Host "1. Verificando instalacion de PostgreSQL..." -ForegroundColor Yellow
$psqlPath18 = "C:\Program Files\PostgreSQL\18\bin\psql.exe"
$psqlPath17 = "C:\Program Files\PostgreSQL\17\bin\psql.exe"
$psqlPath16 = "C:\Program Files\PostgreSQL\16\bin\psql.exe"
$psqlPath15 = "C:\Program Files\PostgreSQL\15\bin\psql.exe"

if (Test-Path $psqlPath18) {
    Write-Host "   OK PostgreSQL 18 encontrado" -ForegroundColor Green
    $psql = $psqlPath18
} elseif (Test-Path $psqlPath17) {
    Write-Host "   OK PostgreSQL 17 encontrado" -ForegroundColor Green
    $psql = $psqlPath17
} elseif (Test-Path $psqlPath16) {
    Write-Host "   OK PostgreSQL 16 encontrado" -ForegroundColor Green
    $psql = $psqlPath16
} elseif (Test-Path $psqlPath15) {
    Write-Host "   OK PostgreSQL 15 encontrado" -ForegroundColor Green
    $psql = $psqlPath15
} else {
    Write-Host "   ERROR PostgreSQL no encontrado" -ForegroundColor Red
    Write-Host "   Por favor, instala PostgreSQL primero" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "2. Creando base de datos tickets_db..." -ForegroundColor Yellow
Write-Host "   (Te pedira la contrasena de postgres)" -ForegroundColor Gray

# Crear base de datos
& $psql -U postgres -c "CREATE DATABASE tickets_db;" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "   OK Base de datos creada exitosamente" -ForegroundColor Green
} else {
    Write-Host "   INFO La base de datos puede que ya exista o hubo un error" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "3. Verificando conexion..." -ForegroundColor Yellow
& $psql -U postgres -d tickets_db -c "SELECT version();" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "   OK Conexion exitosa" -ForegroundColor Green
} else {
    Write-Host "   ERROR Error de conexion" -ForegroundColor Red
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Configuracion completada" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ahora puedes ejecutar:" -ForegroundColor Green
Write-Host "  python manage.py migrate" -ForegroundColor White
Write-Host ""
