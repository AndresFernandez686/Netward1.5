# UI y lógica de empleados (Inventario, delivery)
import streamlit as st
from datetime import date
from utils import df_to_csv_bytes

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

    # Inicializar productos cargados en session_state si no existe
    if "productos_cargados" not in st.session_state:
        st.session_state.productos_cargados = {}

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
                        # Inicializar valor
                        if key_balde not in st.session_state:
                            valor_guardado = 0.0
                            if isinstance(productos[producto_seleccionado], list) and len(productos[producto_seleccionado]) >= n:
                                # Si hay datos guardados como float, usarlos
                                if isinstance(productos[producto_seleccionado][n-1], (int, float)):
                                    valor_guardado = float(productos[producto_seleccionado][n-1])
                            st.session_state[key_balde] = valor_guardado
                        
                        kilos = st.number_input(
                            f"Balde {n} (kg)",
                            min_value=0.0,
                            max_value=50.0,
                            value=st.session_state[key_balde],
                            step=0.1,
                            format="%.1f",
                            key=key_balde
                        )
                        kilos_baldes.append(round(kilos, 1))
                        total_kilos += kilos
                    
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
                            "Modificar"
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
                        # Inicializa el valor solo si no existe
                        if key_balde not in st.session_state:
                            valor_guardado = None
                            if isinstance(productos[producto_seleccionado], list) and len(productos[producto_seleccionado]) >= n:
                                # Solo usar si es string (formato anterior)
                                if isinstance(productos[producto_seleccionado][n-1], str):
                                    valor_guardado = productos[producto_seleccionado][n-1]
                            st.session_state[key_balde] = valor_guardado if valor_guardado is not None else "Vacío"
                        opcion = st.selectbox(
                            f"Balde {n}",
                            list(opciones_valde.keys()),
                            index=list(opciones_valde.keys()).index(st.session_state[key_balde]) if st.session_state[key_balde] in opciones_valde else 0,
                            key=key_balde
                        )
                        estados_baldes.append(opcion)

                    if st.button(
                        f"Actualizar {producto_seleccionado} ({categoria}) - {tipo_inventario}",
                        key=f"btn_{categoria}_{producto_seleccionado}_estados"
                    ):
                        productos[producto_seleccionado] = estados_baldes.copy()
                        guardar_inventario(inventario)
                        guardar_historial(
                            fecha_carga, usuario, categoria, producto_seleccionado, 
                            {"estados": estados_baldes, "tipo": tipo_inventario}, 
                            "Modificar"
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
                # Mostrar la cantidad actual del inventario en lugar de empezar en 0
                valor_inicial = productos[producto_seleccionado]
                cantidad = st.number_input(
                    "Cantidad (unidades)", 
                    min_value=0, 
                    value=valor_inicial,  # Usar el valor actual del inventario
                    step=1, 
                    key=f"cant_{categoria}_{producto_seleccionado}"
                )
                
                if st.button(
                    f"Actualizar {producto_seleccionado} ({categoria})",
                    key=f"btn_{categoria}_{producto_seleccionado}"
                ):
                    cantidad = max(0, int(cantidad))
                    productos[producto_seleccionado] = cantidad  # Siempre reemplazar con el nuevo valor
                    guardar_inventario(inventario)
                    guardar_historial(
                        fecha_carga, usuario, categoria, producto_seleccionado, cantidad, "Modificar"
                    )
                    
                    # Registrar en productos cargados
                    if categoria not in st.session_state.productos_cargados:
                        st.session_state.productos_cargados[categoria] = {}
                    st.session_state.productos_cargados[categoria][producto_seleccionado] = cantidad
                    
                    st.success(f"Actualizado. Nuevo stock: {cantidad}")

    # Mostrar solo los productos que ha cargado el empleado en la sesión actual
    st.subheader("Productos que has cargado:")
    if not st.session_state.productos_cargados:
        st.write("Aún no has cargado ningún producto.")
    else:
        for categoria, productos_cat in st.session_state.productos_cargados.items():
            for producto, datos in productos_cat.items():
                if categoria == "Por Kilos" and isinstance(datos, dict):
                    if datos.get("tipo") == "Quincenal":
                        # Formato quincenal con kilos
                        total = datos.get("total_kilos", 0)
                        kilos_detalle = datos.get("kilos_por_balde", [])
                        detalle = ', '.join([f'{k:.1f}kg' for k in kilos_detalle])
                        st.write(f"• {producto} (Quincenal): **{total:.1f} kg** ({detalle})")
                    else:
                        # Formato diario/semanal con estados
                        estados = datos.get("estados", [])
                        tipo = datos.get("tipo", "")
                        st.write(f"• {producto} ({tipo}): {', '.join(estados)}")
                elif isinstance(datos, list):  # Formato antiguo para compatibilidad
                    if all(isinstance(x, str) for x in datos):  # Estados de baldes
                        baldes_no_vacios = [x for x in datos if x != "Vacío"]
                        baldes_vacios = [x for x in datos if x == "Vacío"]
                        if baldes_no_vacios or baldes_vacios:
                            st.write(f"• {producto}: {', '.join(baldes_no_vacios + baldes_vacios)}")
                    else:  # Kilos (números)
                        total = sum(datos)
                        detalle = ', '.join([f'{k:.1f}kg' for k in datos])
                        st.write(f"• {producto}: **{total:.1f} kg** ({detalle})")
                else:  # Para productos con cantidad numérica simple
                    st.write(f"• {producto}: {datos if datos > 0 else 'Vacío'}")

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
