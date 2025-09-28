# 🏪 Netward - Sistema de Gestión de Inventario

Sistema modular de gestión de inventario y delivery con interfaz web desarrollado en Streamlit.

## 🚀 Características

### 👥 Panel de Empleados
- **Inventario por tipos**: Diario, Semanal, Quincenal
- **Sistema de delivery**: Gestión de entregas y ventas
- **Interfaz intuitiva**: Fácil de usar y navegar

### 👑 Panel de Administradores
- **Gestión completa de inventario**: Vista consolidada y por tipos
- **Análisis de historial**: Tendencias, comparaciones y métricas
- **Sistema de entregas**: Dashboard, gestión y catálogo
- **Reportes avanzados**: Dashboard ejecutivo y análisis predictivo

## 🛠️ Arquitectura Modular

El sistema utiliza una arquitectura modular híbrida que permite:
- **Modo Clásico**: Funcionalidad básica garantizada
- **Modo Modular**: Funciones avanzadas cuando están disponibles
- **Fallback automático**: Sistema robusto ante errores de importación

### 📁 Estructura del Proyecto

```
Netward1.4/
├── 📁 core/              # Lógica de negocio central
│   ├── inventory_types.py
│   ├── data_models.py
│   └── inventory_manager.py
├── 📁 ui/                # Interfaces de usuario
│   ├── admin/           # Componentes administrativos
│   ├── employee/        # Componentes de empleados
│   └── components/      # Widgets reutilizables
├── 📁 data/             # Gestión de datos
│   ├── persistence.py
│   └── history.py
├── 📁 utils/            # Utilidades generales
├── 📁 config/           # Configuraciones
└── main.py              # Aplicación principal
```

## 🔧 Instalación Local

1. **Clonar el repositorio:**
```bash
git clone https://github.com/AndresFernandez686/Netward1.4.git
cd Netward1.4
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación:**
```bash
streamlit run main.py
```

## 🌐 Deployment en Streamlit Cloud

### Opción A: Deployment Directo

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Conecta tu cuenta de GitHub
3. Selecciona este repositorio: `AndresFernandez686/Netward1.4`
4. Archivo principal: `main.py`
5. ¡Despliega!

### Opción B: Usando GitHub Actions (Automático)

El repositorio incluye configuración automática para deployment.

## 📊 Sistema de Modos

La aplicación detecta automáticamente el nivel de funcionalidad:

- 🚀 **Modular Completo**: Todas las funciones avanzadas
- 🔄 **Modular Parcial**: Funciones básicas + tipos de inventario  
- 📋 **Modo Clásico**: Funcionalidad estándar garantizada

## 👨‍💻 Uso

### Credenciales de Acceso

**Empleados:**
- Usuario: `empleado1`, `empleado2`, etc.
- Contraseña: `123`

**Administradores:**
- Usuario: `admin`
- Contraseña: `admin123`

### Funcionalidades por Rol

#### 👤 Empleados
- Cargar inventario por tipos (Diario/Semanal/Quincenal)
- Gestionar entregas y delivery
- Consultar historial personal

#### 👑 Administradores  
- Panel ejecutivo con KPIs y métricas
- Gestión completa de inventario
- Análisis de tendencias e historial
- Sistema completo de reportes
- Gestión de entregas y catálogo
- Análisis predictivo y proyecciones

## 🛡️ Características Técnicas

- **Persistencia**: Archivos JSON con sistema de backup
- **Validación**: Datos validados en tiempo real
- **Responsive**: Compatible con dispositivos móviles
- **Robusto**: Sistema de fallback ante errores
- **Modular**: Arquitectura escalable y mantenible

## 📈 Roadmap

- [ ] Base de datos SQL
- [ ] API REST
- [ ] Autenticación OAuth
- [ ] Análisis ML avanzado
- [ ] Integración con sistemas ERP

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una branch para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Añadir nueva característica'`)
4. Push a la branch (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🏷️ Versión

**Netward v1.5** - Sistema modular con arquitectura híbrida

---

**Desarrollado con ❤️ usando Streamlit**