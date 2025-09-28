#!/bin/bash

# Script para subir Netward a GitHub y preparar deployment en Streamlit

echo "🚀 SUBIENDO NETWARD A GITHUB"
echo "=========================="

# Verificar si es un repositorio git
if [ ! -d ".git" ]; then
    echo "📦 Inicializando repositorio Git..."
    git init
    git branch -M main
fi

# Verificar configuración de Git
echo "📋 Verificando configuración Git..."
git config user.name "AndresFernandez686"
git config user.email "tu-email@example.com"  # Cambia por tu email

# Agregar archivos
echo "📁 Agregando archivos al repositorio..."
git add .

# Crear commit
echo "💾 Creando commit..."
git commit -m "feat: Netward v1.5 - Sistema modular completo

✨ Nuevas características:
- Arquitectura modular híbrida con fallback automático  
- Panel administrativo completo con reportes avanzados
- Sistema de inventario por tipos (Diario/Semanal/Quincenal)
- Dashboard ejecutivo con KPIs y métricas
- Análisis predictivo y reportes personalizables
- Interfaz responsive y robusta

🔧 Mejoras técnicas:
- Importaciones híbridas para máxima compatibilidad
- Sistema de detección automática de funcionalidades
- Configuración lista para Streamlit Cloud
- Tests automáticos con GitHub Actions

📋 Archivos incluidos:
- Aplicación principal optimizada (main.py)
- Módulos core, ui, data completamente funcionales  
- Configuración Streamlit, README y deployment scripts
- Datos de ejemplo y estructura completa

🚀 Listo para deployment en Streamlit Cloud"

# Configurar remote si no existe
if ! git remote get-url origin >/dev/null 2>&1; then
    echo "🔗 Configurando repositorio remoto..."
    git remote add origin https://github.com/AndresFernandez686/Netward1.4.git
fi

# Subir a GitHub
echo "⬆️  Subiendo a GitHub..."
git push -u origin main

echo ""
echo "✅ ¡SUBIDA COMPLETADA!"
echo ""
echo "🎯 PRÓXIMOS PASOS PARA STREAMLIT CLOUD:"
echo "1. Ve a: https://share.streamlit.io"
echo "2. Haz clic en 'New app'"
echo "3. Selecciona: AndresFernandez686/Netward1.4"
echo "4. Main file path: main.py"
echo "5. ¡Haz clic en Deploy!"
echo ""
echo "🌐 Tu repositorio: https://github.com/AndresFernandez686/Netward1.4"
echo "📱 Una vez deployado estará en: https://netward.streamlit.app"