@echo off
REM Script para subir Netward a GitHub (Windows)

echo 🚀 SUBIENDO NETWARD A GITHUB
echo ==========================

REM Verificar si es un repositorio git
if not exist ".git" (
    echo 📦 Inicializando repositorio Git...
    git init
    git branch -M main
)

REM Verificar configuración de Git
echo 📋 Configurando Git...
git config user.name "AndresFernandez686"
git config user.email "tu-email@example.com"

REM Agregar archivos
echo 📁 Agregando archivos al repositorio...
git add .

REM Crear commit
echo 💾 Creando commit...
git commit -m "feat: Netward v1.5 - Sistema modular completo - Arquitectura híbrida con fallback automático - Panel administrativo con reportes avanzados - Sistema de inventario por tipos - Dashboard ejecutivo y análisis predictivo"

REM Configurar remote si no existe
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo 🔗 Configurando repositorio remoto...
    git remote add origin https://github.com/AndresFernandez686/Netward1.4.git
)

REM Subir a GitHub
echo ⬆️  Subiendo a GitHub...
git push -u origin main

echo.
echo ✅ ¡SUBIDA COMPLETADA!
echo.
echo 🎯 PRÓXIMOS PASOS PARA STREAMLIT CLOUD:
echo 1. Ve a: https://share.streamlit.io
echo 2. Haz clic en 'New app'
echo 3. Selecciona: AndresFernandez686/Netward1.4
echo 4. Main file path: main.py
echo 5. ¡Haz clic en Deploy!
echo.
echo 🌐 Tu repositorio: https://github.com/AndresFernandez686/Netward1.4
echo 📱 Una vez deployado estará en: https://netward.streamlit.app

pause