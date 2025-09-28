# Entrada de la app - Version Netward 1.5 Modular (Transición)
import streamlit as st
import os
from datetime import date

# Función para activar modo modular
def try_activate_full_modular():
    """Intenta activar el modo modular completo"""
    try:
        # Probar importaciones modulares completas
        from core.inventory_types import InventoryType
        from ui.components.widgets import NotificationManager
        from ui.admin import AdminUIFactory
        from ui.employee import EmployeeUIFactory
        return True, "COMPLETE"
    except ImportError as e:
        # Probar importaciones básicas
        try:
            from core.inventory_types import InventoryType
            return True, "PARTIAL"
        except ImportError as e:
            return False, str(e)

# Imports modulares - usando try/except para fallback gradual
modular_success, modular_result = try_activate_full_modular()

if modular_success and modular_result == "COMPLETE":
    MODULAR_MODE = True
    print("✅ Modo modular COMPLETO activado")
    print("   📦 Funciones disponibles: Inventario por tipos, Reportes avanzados, Análisis predictivo")
elif modular_success and modular_result == "PARTIAL":
    MODULAR_MODE = "PARTIAL" 
    print("🔄 Modo modular PARCIAL activado")
    print("   📦 Funciones disponibles: Inventario por tipos (funcionalidad limitada)")
else:
    MODULAR_MODE = False
    print(f"⚠️  Modo clásico activado (falló importación modular: {modular_result})")
    print("   📦 Funciones disponibles: Inventario básico, Delivery, Historial")

# Imports clásicos como fallback
from persistencia import (
    cargar_inventario, guardar_inventario, guardar_historial,
    cargar_historial, cargar_catalogo_delivery, guardar_catalogo_delivery,
    guardar_venta_delivery, cargar_ventas_delivery
)
from auth import login, logout
from ui_empleado import empleado_inventario_ui, empleado_delivery_ui
from ui_admin import admin_inventario_ui, admin_historial_ui, admin_delivery_ui

# Aplicar CSS personalizado
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), '.streamlit', 'style.css')
    if os.path.exists(css_path):
        with open(css_path, encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        # CSS básico por defecto
        default_css = """
        <style>
        .main-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        .stAlert > div {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }
        </style>
        """
        st.markdown(default_css, unsafe_allow_html=True)

# Cargar HTML personalizado
def load_html(html_file):
    html_path = os.path.join(os.path.dirname(__file__), '.streamlit', html_file)
    if os.path.exists(html_path):
        with open(html_path, encoding='utf-8') as f:
            return f.read()
    else:
        return ""

# Datos base (corregidos y actualizados)
productos_por_categoria = {
    "Impulsivo": {
        "Caja almendrado": 0,
        "Unidad Almendrado": 0,
        "Caja Bombon Crocante": 0,
        "Unidad Bombon Crocante": 0,
        "Caja Bombon Escoces": 0,
        "Unidad Bombon Escoces": 0,
        "Caja de bombon Suizo": 0,
        "Unidad bombon Suizo": 0,
        "Caja Bombon Cookies and Crema": 0,
        "Unidad Bombon Cookies and Crema": 0,
        "Caja Bombon Vainilla": 0,
        "Unidad Bombon Vainilla": 0,
        "Caja Casatta": 0,
        "Unidad Casatta": 0,
        "Crocantino": 0,
        "Delicia": 0,
        "Pizza": 0,
        "Familiar 1": 0,
        "Familiar 2": 0,
        "Familiar 3": 0,
        "Familiar 4": 0,
        "Caja palito Bombon": 0,
        "Unidad Palito Bombon": 0,
        "Caja Palito Crema Americana": 0,
        "Unidad Palito Crema Americana": 0,
        "Caja Palito Crema Frutilla": 0,
        "Unidad Palito Crema Frutilla": 0,
        "Caja Palito Frutal Frutilla": 0,
        "Unidad Palito Frutal Frutilla": 0,
        "Caja Palito Frutal Limon": 0,
        "Unidad Palito Frutal Limon": 0,
        "Caja Palito Frutal Naranja": 0,
        "Unidad Palito Frutal Naranja": 0,
        "Tentacion Chocolate": 0,
        "Tentacion Chocolate con Almendra": 0,
        "Tentacion Cookies": 0,
        "Tentacion Crema Americana": 0,
        "Tentacion Dulce de Leche Granizado": 0,
        "Tentacion Dulce de Leche": 0,
        "Tentacion Frutilla": 0,
        "Tentacion Granizado": 0,
        "Tentacion Menta Granizada": 0,
        "Tentacion Mascarpone": 0,
        "Tentacion Vainilla": 0,
        "Tentacion Limon": 0,
        "Tentacion Toddy": 0,
        "Yogurt Helado Frutilla sin Tacc": 0,
        "Yogurt Helado Mango Maracuya": 0,
        "Yogurt Helado Frutos del Bosque sin Tacc": 0,
        "Helado sin Azucar Frutilla a la Crema": 0,
        "Helado sin Azucar Durazno a la Crema": 0,
        "Helado sin Azucar chocolate sin Tacc": 0,
        "Torta con Oreo": 0,
        "Torta Grido Rellena": 0,
        "Torta Milka": 0
    },
    "Por Kilos": {
        "Vainilla": 0.0,
        "Chocolate": 0.0,
        "Fresa": 0.0,
        "Anana a la crema": 0.0,
        "Banana con Dulce de leche": 0.0,
        "Capuccino Granizado": 0.0,
        "Cereza": 0.0,
        "Chocolate Blanco": 0.0,
        "Chocolate con Almendra": 0.0,
        "Chocolate Dark": 0.0,
        "Chocolate Mani Crunch": 0.0,
        "Chocolate Suizo": 0.0,
        "Crema Americana": 0.0,
        "Crema Cookie": 0.0,
        "Crema Rusa": 0.0,
        "Dulce de Leche": 0.0,
        "Dulce de Leche con Brownie": 0.0,
        "Dulce de Leche con Nuez": 0.0,
        "Dulce de Leche Especial": 0.0,
        "Dulce de Leche Granizado": 0.0,
        "Durazno a la Crema": 0.0,
        "Flan": 0.0,
        "Frutos Rojos al Agua": 0.0,
        "Granizado": 0.0,
        "Kinotos al Whisky": 0.0,
        "Limon al Agua": 0.0,
        "Maracuya": 0.0,
        "Marroc Grido": 0.0,
        "Mascarpone con Frutos del Bosque": 0.0,
        "Menta Granizada": 0.0,
        "Naranja Helado al Agua": 0.0,
        "Pistacho": 0.0,
        "Super Gridito": 0.0,
        "Tiramisu": 0.0,
        "Tramontana": 0.0,
        "Candy": 0.0
    },
    "Extras": {
        "Cinta Grido": 0,
        "Cobertura Chocolate": 0,
        "Bolsa 40x50": 0,
        "Cobertura Frutilla": 0,
        "Cobertura Dulce de Leche": 0,
        "Leche": 0,
        "Cuchara Sunday": 0,
        "Cucharita Grido": 0,
        "Cucurucho Biscoito Dulce x300": 0,
        "Cucurucho Cascao x120": 0,
        "Cucurucho Nacional x54": 0,
        "Garrafita de Gas": 0,
        "Isopor 1 kilo": 0,
        "Isopor 1/2 kilo": 0,
        "Isopor 1/4": 0,
        "Mani tostado": 0,
        "Pajita con Funda": 0,
        "Servilleta Grido": 0,
        "Tapa Burbuja Capuccino": 0,
        "Tapa Burbuja Batido": 0,
        "Vaso capuccino": 0,
        "Vaso Batido": 0,
        "Vasito de una Bocha": 0,
        "Vaso Termico 240gr": 0,
        "Vaso Sundae": 0,
        "Rollo Termico": 0
    }
}

# Opciones de valde como texto literal
opciones_valde = {
    "Vacío": "Vacío",
    "Casi lleno": "Casi lleno",
    "Medio lleno": "Medio lleno",
    "Valde lleno": "Valde lleno"
}

def render_modular_notification():
    """Muestra notificación sobre el modo actual"""
    if MODULAR_MODE:
        st.info("🆕 **Netward 1.5 Modular** - Sistema con diferenciación de tipos de inventario")
        if 'InventoryType' in globals():
            types = ", ".join([t.value for t in InventoryType])
            st.success(f"✅ Tipos disponibles: {types}")
    else:
        st.warning("⚡ Ejecutando en modo clásico - Algunas funciones avanzadas no disponibles")

def main():
    st.set_page_config(
        page_title="Netward - Heladería Inventario & Delivery", 
        page_icon="🍦", 
        layout="wide"
    )
    
    # Cargar CSS personalizado
    load_css()
    
    # Mostrar header con información del sistema
    st.markdown("""
        <div class="main-header">
            <h1>🍦 Netward - Sistema de Gestión</h1>
            <p>Inventario y Delivery para Heladería - V1.5</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Inicializar el estado de la sesión
    if "usuario" not in st.session_state:
        st.session_state.usuario = None
        st.session_state.rol = None
    
    # Información del sistema en sidebar
    with st.sidebar:
        st.markdown("### 🔧 Estado del Sistema")
        render_modular_notification()
        
        # Botón de cierre de sesión
        if st.session_state.usuario:
            st.success(f"👤 {st.session_state.usuario}")
            st.info(f"🔑 {st.session_state.rol}")
            
            if st.button("🚪 Cerrar Sesión"):
                logout()
                st.session_state.usuario = None
                st.session_state.rol = None
                st.rerun()
    
    # Si no hay usuario en la sesión, mostrar login
    if not st.session_state.usuario:
        st.markdown("## 🔐 Inicio de Sesión")
        usuario, rol = login()
        if usuario and rol:
            st.session_state.usuario = usuario
            st.session_state.rol = rol
            st.success(f"¡Bienvenido {usuario}!")
            st.rerun()
        return

    # Cargar inventario
    inventario = cargar_inventario(productos_por_categoria)

    # Interfaz según rol
    if st.session_state.rol == 'empleado':
        st.markdown("## 👨‍💼 Panel de Empleado")
        tab_inv, tab_deliv = st.tabs(["🧊 Inventario", "🚚 Delivery"])
        
        with tab_inv:
            try:
                empleado_inventario_ui(
                    inventario, st.session_state.usuario, opciones_valde,
                    guardar_inventario, guardar_historial
                )
            except Exception as e:
                st.error(f"Error en inventario: {str(e)}")
                st.info("💡 Reinicia la aplicación si el problema persiste")
        
        with tab_deliv:
            try:
                empleado_delivery_ui(
                    st.session_state.usuario, cargar_catalogo_delivery, 
                    guardar_venta_delivery, cargar_ventas_delivery
                )
            except Exception as e:
                st.error(f"Error en delivery: {str(e)}")
                st.info("💡 Reinicia la aplicación si el problema persiste")

    elif st.session_state.rol == 'administrador':
        st.markdown("## 👑 Panel de Administrador")
        
        # Mostrar estado del sistema
        if MODULAR_MODE == True:
            st.success("🚀 **Sistema Modular Completo** - Todas las funciones avanzadas disponibles")
        elif MODULAR_MODE == "PARTIAL":
            st.warning("🔄 **Sistema Modular Parcial** - Funciones básicas disponibles")
        else:
            st.info("📋 **Sistema Clásico** - Funciones estándar disponibles")
        
        tab_inv, tab_hist, tab_deliv, tab_reports = st.tabs([
            "📦 Inventario", "📅 Historial", "🛠️ Delivery", "📋 Reportes"
        ])
        
        with tab_inv:
            try:
                # Intentar usar sistema modular primero
                try:
                    from ui.admin import AdminUIFactory
                    admin_inventory = AdminUIFactory.create("inventory_admin")
                    admin_inventory.render(st.session_state.usuario)
                except (ImportError, Exception):
                    # Fallback al sistema clásico
                    admin_inventario_ui(inventario)
            except Exception as e:
                st.error(f"Error en inventario admin: {str(e)}")
        
        with tab_hist:
            try:
                # Intentar usar sistema modular primero
                try:
                    from ui.admin import AdminUIFactory
                    admin_history = AdminUIFactory.create("history_admin")
                    admin_history.render(st.session_state.usuario)
                except (ImportError, Exception):
                    # Fallback al sistema clásico
                    admin_historial_ui(cargar_historial())
            except Exception as e:
                st.error(f"Error en historial: {str(e)}")
        
        with tab_deliv:
            try:
                # Intentar usar sistema modular primero
                try:
                    from ui.admin import AdminUIFactory
                    admin_delivery = AdminUIFactory.create("delivery_admin")
                    admin_delivery.render(st.session_state.usuario)
                except (ImportError, Exception):
                    # Fallback al sistema clásico
                    admin_delivery_ui(
                        cargar_catalogo_delivery, guardar_catalogo_delivery, 
                        cargar_ventas_delivery
                    )
            except Exception as e:
                st.error(f"Error en delivery admin: {str(e)}")
        
        with tab_reports:
            if MODULAR_MODE == True:
                try:
                    from ui.admin import AdminUIFactory
                    admin_reports = AdminUIFactory.create("reports_admin")
                    admin_reports.render(st.session_state.usuario)
                except Exception as e:
                    st.error("📋 Error al cargar sistema de reportes")
                    st.code(f"Error técnico: {str(e)}")
                    st.info("💡 Contacta al administrador del sistema")
            else:
                st.markdown("### 📋 Sistema de Reportes")
                if MODULAR_MODE == "PARTIAL":
                    st.warning("⚠️ **Sistema Modular Parcial Detectado**")
                    st.markdown("""
                    El sistema de reportes requiere el **modo modular completo** para funcionar.
                    
                    **Estado actual**: Importaciones modulares parciales
                    
                    **Para activar reportes completos**:
                    1. Verifica que todos los módulos estén correctamente instalados
                    2. Reinicia la aplicación 
                    3. Contacta al administrador si el problema persiste
                    """)
                else:
                    st.info("ℹ️ **Sistema Clásico Activo**")
                    st.markdown("""
                    El sistema de reportes avanzados no está disponible en modo clásico.
                    
                    **Funciones disponibles en modo clásico**:
                    - ✅ Gestión de inventario básico
                    - ✅ Historial de operaciones  
                    - ✅ Sistema de delivery
                    
                    **Para activar reportes**:
                    - Se requiere migrar al sistema modular completo
                    """)
                
                # Botón para reintentar activación modular  
                if st.button("🔄 Reintentar Activación Modular", type="primary"):
                    # Intentar forzar activación modular
                    try:
                        import importlib
                        import sys
                        
                        # Limpiar cache de módulos
                        modules_to_reload = [
                            'ui.admin', 'ui.components.widgets', 
                            'core.inventory_types', 'data.persistence'
                        ]
                        for module in modules_to_reload:
                            if module in sys.modules:
                                del sys.modules[module]
                        
                        # Reintentar importación completa
                        from core.inventory_types import InventoryType
                        from ui.components.widgets import NotificationManager
                        from ui.admin import AdminUIFactory
                        from ui.employee import EmployeeUIFactory
                        
                        st.success("✅ **Modo Modular Completo Activado!**")
                        st.info("🔄 Recargando aplicación...")
                        st.rerun()
                        
                    except Exception as retry_error:
                        st.error(f"❌ No se pudo activar modo completo: {str(retry_error)}")
                        st.info("💡 La aplicación seguirá funcionando con las funciones disponibles")
                
                # Mostrar reportes básicos disponibles
                st.markdown("---")
                st.markdown("### 📊 Reportes Básicos Disponibles")
                
                try:
                    historial = cargar_historial()
                    
                    if historial:
                        st.markdown("#### 📈 Resumen General")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            total_registros = len(historial)
                            st.metric("📋 Total de Registros", total_registros)
                        
                        with col2:
                            # Usuarios únicos
                            usuarios = set(r.get('usuario', 'N/A') for r in historial)
                            st.metric("👥 Usuarios Activos", len(usuarios))
                        
                        with col3:
                            # Registros del último mes
                            from datetime import datetime, timedelta
                            mes_pasado = datetime.now() - timedelta(days=30)
                            recientes = [r for r in historial 
                                       if r.get('fecha', '2020-01-01') >= mes_pasado.strftime('%Y-%m-%d')]
                            st.metric("📅 Actividad (30 días)", len(recientes))
                        
                        # Mostrar últimos registros
                        st.markdown("#### 📋 Últimos Registros")
                        if len(historial) > 0:
                            import pandas as pd
                            
                            # Mostrar últimos 5 registros
                            ultimos = historial[-5:]
                            df_data = []
                            
                            for registro in ultimos:
                                df_data.append({
                                    'Fecha': registro.get('fecha', 'N/A'),
                                    'Usuario': registro.get('usuario', 'N/A'),
                                    'Tipo': registro.get('tipo_inventario', 'N/A'),
                                    'Productos': len(registro.get('productos_modificados', []))
                                })
                            
                            df = pd.DataFrame(df_data)
                            st.dataframe(df, use_container_width=True)
                        
                        st.success("🚀 **¡Activa el modo completo para análisis detallados, gráficos interactivos y predicciones!**")
                    
                    else:
                        st.info("📊 No hay datos suficientes para generar reportes")
                        st.markdown("Realiza algunas operaciones de inventario primero.")
                
                except Exception as basic_error:
                    st.warning(f"⚠️ Error al cargar reportes básicos: {str(basic_error)}")
                
                # Agregar demo de reportes
                st.markdown("---")
                st.markdown("### 🎮 Demo: ¿Qué hacen los Reportes?")
                
                if st.button("👀 Ver Demo de Reportes", type="secondary"):
                    st.markdown("#### 📊 **Ejemplo de lo que pueden hacer los Reportes:**")
                    
                    # Simulación rápida de datos
                    st.markdown("##### 🏆 Productos Más Vendidos (Simulación)")
                    
                    productos_ejemplo = [
                        {"producto": "Cerveza Corona", "ventas": 45, "ingresos": "$22,500"},
                        {"producto": "Marlboro Box", "ventas": 38, "ingresos": "$19,000"}, 
                        {"producto": "Coca Cola 600ml", "ventas": 32, "ingresos": "$9,600"},
                        {"producto": "Fernet Branca", "ventas": 28, "ingresos": "$16,800"},
                        {"producto": "Red Bull", "ventas": 25, "ingresos": "$12,500"}
                    ]
                    
                    for i, item in enumerate(productos_ejemplo, 1):
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.write(f"{i}. **{item['producto']}**")
                        with col2:
                            st.write(f"🛒 {item['ventas']} unidades")
                        with col3:
                            st.write(f"💰 {item['ingresos']}")
                    
                    st.markdown("##### 📅 Análisis por Días")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("🎯 Mejor día", "Sábado", "+25% vs promedio")
                    with col2:
                        st.metric("📈 Crecimiento", "+15%", "vs mes pasado")
                    with col3:
                        st.metric("⏰ Hora pico", "18:00-20:00", "35% de ventas")
                    
                    st.markdown("##### ⚠️ Alertas Inteligentes")
                    st.warning("🚨 **Stock bajo**: Marlboro Box (quedan 3 cajas)")
                    st.success("🎉 **Producto estrella**: Cerveza Corona (+30% este mes)")
                    st.info("💡 **Recomendación**: Aumentar stock de cervezas para el fin de semana")
                    
                    st.markdown("##### 🔮 Predicciones")
                    st.markdown("**Próxima semana estimada:**")
                    st.write("- 🛒 Ventas esperadas: **180 productos**")
                    st.write("- 💰 Ingresos estimados: **$54,000**")
                    st.write("- 📈 Producto + demandado: **Cerveza Corona** (50 unidades)")
                    
                    st.markdown("---")
                    st.success("""
                    ### 🚀 **¡Esto es lo que hacen los Reportes Completos!**
                    
                    **Te ayudan a:**
                    - 📊 **Entender** qué se vende más y cuándo
                    - 🎯 **Decidir** qué productos comprar y en qué cantidad  
                    - ⚠️ **Prevenir** quedarte sin stock de productos populares
                    - 💰 **Maximizar** tus ganancias con datos reales
                    - 🔮 **Planificar** el futuro de tu negocio
                    
                    **Activa el modo modular completo para tener todas estas funciones con TUS datos reales!**
                    """)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Se ha producido un error: {str(e)}")
        if st.button("Reintentar"):
            st.rerun()
