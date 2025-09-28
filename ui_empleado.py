# UI y lógica de empleados (Inventario, delivery)
import streamlit as st
from datetime import date
try:
    from utils import df_to_csv_bytes
except ImportError:
    def df_to_csv_bytes(df):
        return df.to_csv(index=False).encode('utf-8')

def empleado_inventario_ui(inventario, usuario, opciones_valde, guardar_inventario, guardar_historial):
    st.header("Inventario")
    
    # Selector de tipo de inventario
    col1, col2 = st.columns(2)
    with col1:
        fecha_carga = st.date_input("Selecciona la fecha de carga", value=date.today(), key="fecha_inv")
    with col2:
        tipo_inventario = st.selectbox(
            "Tipo de inventario", 
            ["Diario", "Semanal", "Quincenal"], 
            key="tipo_inventario"
        )
    
    # Mostrar información sobre el tipo seleccionado
    if tipo_inventario == "Quincenal":
        st.info("📊 **Inventario Quincenal**: En la categoría 'Por Kilos' registrarás la cantidad exacta en kilos de cada balde.")

    # Inicializar sistema de inventario por tipo
    if "inventario_por_tipo" not in st.session_state:
        st.session_state.inventario_por_tipo = {
            "Diario": {},
            "Semanal": {},
            "Quincenal": {}
        }
    
    # Inicializar productos cargados en session_state si no existe
    if "productos_cargados" not in st.session_state:
        st.session_state.productos_cargados = {}
        
    # Detectar cambio de tipo de inventario y limpiar session_state
    if "tipo_actual" not in st.session_state:
        st.session_state.tipo_actual = tipo_inventario
    
    if st.session_state.tipo_actual != tipo_inventario:
        # Limpiar todas las keys de widgets cuando cambia el tipo
        keys_to_clear = [k for k in st.session_state.keys() if any(x in k for x in ["cant_", "_balde_", "num_baldes_"])]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        
        st.session_state.tipo_actual = tipo_inventario
        st.info(f"🔄 Cambiado a inventario **{tipo_inventario}**")

    tabs = st.tabs(list(inventario.keys()))
    for i, categoria in enumerate(inventario.keys()):
        with tabs[i]:
            productos = inventario[categoria]
            producto_seleccionado = st.selectbox(
                f"Producto de {categoria}",
                list(productos.keys()),
                key=f"sel_{categoria}"
            )

            # Ya no necesitamos la opción de añadir/reemplazar, siempre será modificar
            
            if categoria == "Por Kilos":
                if tipo_inventario == "Quincenal":
                    # Modo quincenal: registrar kilos exactos
                    st.markdown("### Registrar cantidad exacta en kilos por balde:")
                    num_baldes = st.number_input(
                        "Cantidad de baldes",
                        min_value=1,
                        max_value=10,
                        value=1,
                        step=1,
                        key=f"num_baldes_{producto_seleccionado}_{fecha_carga}_{usuario}"
                    )
                    st.markdown(f"### Kilos en cada balde (hasta {num_baldes} baldes):")
                    
                    kilos_baldes = []
                    total_kilos = 0.0
                    
                    for n in range(1, num_baldes + 1):
                        key_balde = f"{producto_seleccionado}_balde_{n}_{fecha_carga}_{usuario}_kilos"
                        
                        # Inicializar valor si no existe
                        if key_balde not in st.session_state:
                            # Empezar en 0.0 por defecto
                            valor_inicial = 0.0
                            if isinstance(productos[producto_seleccionado], list) and len(productos[producto_seleccionado]) >= n:
                                if isinstance(productos[producto_seleccionado][n-1], (int, float)):
                                    valor_inicial = float(productos[producto_seleccionado][n-1])
                            st.session_state[key_balde] = valor_inicial
                        
                        kilos = st.number_input(
                            f"Balde {n} (kg)",
                            min_value=0.0,
                            max_value=50.0,
                            value=st.session_state[key_balde],
                            step=0.1,
                            format="%.1f",
                            key=key_balde
                        )
                        # Usar el valor actual del input
                        kilos_actual = st.session_state[key_balde]
                        kilos_baldes.append(round(kilos_actual, 1))
                        total_kilos += kilos_actual
                    
                    st.markdown(f"**Total: {total_kilos:.1f} kg**")
                    
                    if st.button(
                        f"Actualizar {producto_seleccionado} ({categoria}) - Quincenal",
                        key=f"btn_{categoria}_{producto_seleccionado}_quincenal"
                    ):
                        productos[producto_seleccionado] = kilos_baldes.copy()
                        guardar_inventario(inventario)
                        guardar_historial(
                            fecha_carga, usuario, categoria, producto_seleccionado, 
                            {"kilos_por_balde": kilos_baldes, "total_kilos": total_kilos, "tipo": "Quincenal"}, 
                            "Modificar", tipo_inventario
                        )
                        
                        # Registrar en productos cargados
                        if categoria not in st.session_state.productos_cargados:
                            st.session_state.productos_cargados[categoria] = {}
                        st.session_state.productos_cargados[categoria][producto_seleccionado] = {
                            "kilos_por_balde": kilos_baldes.copy(),
                            "total_kilos": total_kilos,
                            "tipo": "Quincenal"
                        }
                        
                        st.success(f"Actualizado. Total: {total_kilos:.1f} kg ({', '.join([f'{k:.1f}kg' for k in kilos_baldes])})")
                
                else:
                    # Modo diario/semanal: sistema actual de estados
                    st.markdown("### Selecciona la cantidad de baldes a registrar:")
                    num_baldes = st.number_input(
                        "Cantidad de baldes",
                        min_value=1,
                        max_value=10,
                        value=1,
                        step=1,
                        key=f"num_baldes_{producto_seleccionado}_{fecha_carga}_{usuario}"
                    )
                    st.markdown(f"### Estado de hasta {num_baldes} baldes:")

                    estados_baldes = []
                    for n in range(1, num_baldes + 1):
                        key_balde = f"{producto_seleccionado}_balde_{n}_{fecha_carga}_{usuario}"
                        
                        # Inicializar valor si no existe
                        if key_balde not in st.session_state:
                            # Empezar en "Vacío" por defecto
                            valor_inicial = "Vacío"
                            if isinstance(productos[producto_seleccionado], list) and len(productos[producto_seleccionado]) >= n:
                                if isinstance(productos[producto_seleccionado][n-1], str):
                                    valor_inicial = productos[producto_seleccionado][n-1]
                            st.session_state[key_balde] = valor_inicial
                        opcion = st.selectbox(
                            f"Balde {n}",
                            list(opciones_valde.keys()),
                            index=list(opciones_valde.keys()).index(st.session_state[key_balde]) if st.session_state[key_balde] in opciones_valde else 0,
                            key=key_balde
                        )
                        # Usar el valor actual del selectbox
                        estado_actual = st.session_state[key_balde]
                        estados_baldes.append(estado_actual)

                    if st.button(
                        f"Actualizar {producto_seleccionado} ({categoria}) - {tipo_inventario}",
                        key=f"btn_{categoria}_{producto_seleccionado}_estados"
                    ):
                        productos[producto_seleccionado] = estados_baldes.copy()
                        guardar_inventario(inventario)
                        guardar_historial(
                            fecha_carga, usuario, categoria, producto_seleccionado, 
                            {"estados": estados_baldes, "tipo": tipo_inventario}, 
                            "Modificar", tipo_inventario
                        )
                        
                        # Registrar en productos cargados
                        if categoria not in st.session_state.productos_cargados:
                            st.session_state.productos_cargados[categoria] = {}
                        st.session_state.productos_cargados[categoria][producto_seleccionado] = {
                            "estados": estados_baldes.copy(),
                            "tipo": tipo_inventario
                        }
                        
                        st.success(f"Actualizado. Estado actual: {', '.join(estados_baldes)}")

            else:
                # Key específica por tipo de inventario
                key_tipo_producto = f"{tipo_inventario}_{categoria}_{producto_seleccionado}"
                
                # Obtener valor específico del tipo actual
                if key_tipo_producto in st.session_state.inventario_por_tipo[tipo_inventario]:
                    valor_inicial = st.session_state.inventario_por_tipo[tipo_inventario][key_tipo_producto]
                else:
                    valor_inicial = 0
                    st.session_state.inventario_por_tipo[tipo_inventario][key_tipo_producto] = 0
                
                cantidad = st.number_input(
                    "Cantidad (unidades)", 
                    min_value=0, 
                    value=valor_inicial,
                    step=1, 
                    key=f"cant_{tipo_inventario}_{categoria}_{producto_seleccionado}"
                )
                
                if st.button(
                    f"Actualizar {producto_seleccionado} ({categoria}) - {tipo_inventario}",
                    key=f"btn_{tipo_inventario}_{categoria}_{producto_seleccionado}"
                ):
                    # Guardar en el inventario principal (para compatibilidad)
                    productos[producto_seleccionado] = cantidad
                    guardar_inventario(inventario)
                    
                    # Guardar en el sistema por tipo
                    st.session_state.inventario_por_tipo[tipo_inventario][key_tipo_producto] = cantidad
                    
                    # Guardar en historial con tipo específico
                    guardar_historial(
                        fecha_carga, usuario, categoria, producto_seleccionado, cantidad, "Modificar", tipo_inventario
                    )
                    
                    # Registrar en productos cargados
                    if categoria not in st.session_state.productos_cargados:
                        st.session_state.productos_cargados[categoria] = {}
                    st.session_state.productos_cargados[categoria][producto_seleccionado] = {
                        "cantidad": cantidad,
                        "tipo_inventario": tipo_inventario
                    }
                    
                    st.success(f"✅ {producto_seleccionado}: {cantidad} unidades ({tipo_inventario})")

    # Mostrar resumen de todos los tipos de inventario cargados
    st.subheader("📋 Resumen de inventarios cargados:")
    
    hay_datos = False
    for tipo in ["Diario", "Semanal", "Quincenal"]:
        if tipo in st.session_state.inventario_por_tipo:
            datos_tipo = st.session_state.inventario_por_tipo[tipo]
            if datos_tipo:
                hay_datos = True
                st.markdown(f"**🔹 Inventario {tipo}:**")
                for key, cantidad in datos_tipo.items():
                    # Extraer categoria y producto del key
                    partes = key.split('_', 2)  # Formato: tipo_categoria_producto
                    if len(partes) >= 3:
                        categoria = partes[1]
                        producto = partes[2]
                        if cantidad > 0:
                            st.write(f"   • {producto} ({categoria}): **{cantidad}** unidades")
    
    # Mostrar también los productos de la sesión actual
    if st.session_state.productos_cargados:
        st.markdown(f"**🔸 Cargados en esta sesión ({tipo_inventario}):**")
        for categoria, productos_cat in st.session_state.productos_cargados.items():
            for producto, datos in productos_cat.items():
                if isinstance(datos, dict):
                    if "cantidad" in datos:
                        # Nuevo formato con tipo específico
                        cantidad = datos["cantidad"]
                        tipo_inv = datos.get("tipo_inventario", tipo_inventario)
                        st.write(f"   • {producto} ({categoria}): **{cantidad}** unidades - {tipo_inv}")
                    elif categoria == "Por Kilos":
                        # Formato de kilos
                        if datos.get("tipo") == "Quincenal":
                            total = datos.get("total_kilos", 0)
                            kilos_detalle = datos.get("kilos_por_balde", [])
                            detalle = ', '.join([f'{k:.1f}kg' for k in kilos_detalle])
                            st.write(f"   • {producto} (Quincenal): **{total:.1f} kg** ({detalle})")
                        else:
                            estados = datos.get("estados", [])
                            tipo = datos.get("tipo", "")
                            st.write(f"   • {producto} ({tipo}): {', '.join(estados)}")
                else:
                    # Formato numérico simple
                    st.write(f"   • {producto}: **{datos}** unidades")
    
    if not hay_datos and not st.session_state.productos_cargados:
        st.info("Aún no has cargado ningún producto en ningún tipo de inventario.")

def empleado_delivery_ui(usuario, cargar_catalogo_delivery, guardar_venta_delivery, cargar_ventas_delivery):
    st.header("Delivery")
    catalogo = cargar_catalogo_delivery()
    activos = [item for item in catalogo if item.get("activo", True)]

    if not activos:
        st.info("No hay productos de delivery activos. Pide al administrador que agregue opciones.")
        return

    fecha_venta = st.date_input("Fecha de la venta", value=date.today(), key="fecha_deliv")
    opciones = [f"{it['nombre']} {'(PROMO)' if it.get('es_promocion', False) else ''}" for it in activos]
    seleccion = st.selectbox("Producto de delivery", opciones)
    idx = opciones.index(seleccion)
    item_sel = activos[idx]
    cantidad = st.number_input("Cantidad vendida", min_value=1, step=1)

    if st.button("Registrar venta de delivery"):
        guardar_venta_delivery(
            fecha_venta,
            usuario,
            item_sel["nombre"],
            cantidad,
            item_sel.get("es_promocion", False)
        )
        st.success("Venta registrada con éxito ✅")

    ventas = cargar_ventas_delivery()
    if not ventas.empty:
        ventas_hoy = ventas[(ventas["Usuario"] == usuario) & (ventas["Fecha"].dt.date == date.today())]
        if not ventas_hoy.empty:
            st.subheader("Tus ventas de delivery hoy")
            st.dataframe(ventas_hoy)
