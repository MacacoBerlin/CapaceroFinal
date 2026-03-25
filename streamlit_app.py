import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Soberanía Hogar | Auditoría", page_icon="🏠", layout="centered")
# --- SECCIÓN: ESTADO DEL NODO LOCAL (ACTUALIZADO) ---
st.divider()

# --- SECCIÓN: INFRAESTRUCTURA PARA HUMANOS ---
st.divider()

with st.container():
    st.subheader("📡 Tu Centro de Control Local")
    
    # Frase de "Traducción Humana" - El rompehielos
    st.info("""
        **¿No hablas 'tecniqués'?** Quédate con esto: He eliminado a los intermediarios. 
        Tu casa ahora te obedece a ti, no a una nube en otro país. 🛡️
    """)

    # Bloque de Badges con "Traducción"
    col_b1, col_b2 = st.columns(2)
    
    with col_b1:
        st.markdown("""
            <div style="background:#e3f2fd; padding:10px; border-radius:10px; border-left:5px solid #007bff;">
                <span style="font-weight:bold; color:#0056b3;">📶 Zigbee 3.0</span><br>
                <small><b>Privacidad:</b> Tus datos no salen de tu casa. Jamás.</small>
            </div>
        """, unsafe_allow_html=True)
        
    with col_b2:
        st.markdown("""
            <div style="background:#e8f5e9; padding:10px; border-radius:10px; border-left:5px solid #2e7d32;">
                <span style="font-weight:bold; color:#1b5e20;">⚡ Local Push</span><br>
                <small><b>Velocidad:</b> Control instantáneo, sin esperas por internet.</small>
            </div>
        """, unsafe_allow_html=True)

    st.write("") # Espaciador

    # Estado del Nodo con lenguaje sencillo
    col_node1, col_node2 = st.columns([1, 2])
    
    with col_node1:
        st.markdown("""
            <div style="background-color: #fff3e0; border: 1px solid #ffb74d; padding: 15px; border-radius: 10px; text-align: center;">
                <span style="font-size: 30px;">🏠</span><br>
                <b style="color: #e65100;">PREPARANDO TU NODO</b><br>
                <small>Fase de instalación</small>
            </div>
            """, unsafe_allow_html=True)
            
    with col_node2:
        st.markdown(f"""
            **¿Qué estamos montando aquí?**
            * **Hardware:** Una `Raspberry Pi 3` (El cerebro que no duerme).
            * **Misión:** Vigilar tus consumos y apagar lo que no usas.
            * **Seguridad:** 100% desconectado de servidores externos.
            
            _Este equipo es el que detendrá el contador de pérdida que ves abajo._
        """)

# Barra de progreso amigable
st.progress(25, text="Sincronizando el cerebro de tu casa...")


# --- ESTILOS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .roi-badge {
        background-color: #2e7d32; color: white; padding: 15px;
        border-radius: 10px; text-align: center; font-weight: bold;
        margin: 15px 0; border: 2px solid #1b5e20; font-size: 1.1rem;
    }
    .item-box {
        background-color: #ffffff; padding: 12px; border-radius: 8px;
        border-left: 5px solid #2196f3; margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .glossary-card {
        background-color: #f1f3f5; padding: 12px; border-radius: 8px;
        margin-bottom: 8px; border: 1px solid #e0e0e0;
    }
    .termino { color: #2e7d32; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Auditoría Soberanía Hogar")

# --- 1. CONFIGURACIÓN ---
with st.expander("📊 CONFIGURA TU ESCENARIO", expanded=True):
    factura_base = st.number_input("Factura mensual actual (€)", value=120)
    habitaciones = st.number_input("Número de estancias (habitaciones, salón...)", 1, 10, 3)
    
    # Esta variable ahora actúa como un "freno" directo a la fuga
    nivel = st.select_slider(
        "Nivel de Automatización (Freno de gasto)",
        options=["Básico", "Intermedio", "Soberanía Total"],
        value="Intermedio"
    )
    
    inflacion_pct = st.slider("Inflación energética anual (%)", 0, 20, 9)
    inflacion = inflacion_pct / 100

    protocolo = st.radio(
        "Protocolo de comunicación:",
        ["Wi-Fi Estándar (Cloud)", "Zigbee / Thread (Local)"],
        index=1
    )

    # Lógica de EFICIENCIA: A más nivel, mayor ahorro sobre la fuga
    # Si no haces nada, pierdes el 100% del potencial. Si automatizas, "frenas" la pérdida.
    eficiencia_map = {"Básico": 0.20, "Intermedio": 0.45, "Soberanía Total": 0.75}
    freno_automatizacion = eficiencia_map[nivel]
    
    # Penalización por protocolo ineficiente (Wi-Fi gasta más y ahorra menos)
    penalizacion = 0.10 if "Wi-Fi" in protocolo else 0.0
    pct_ahorro_final = freno_automatizacion - penalizacion

# --- 2. CÁLCULO DE LA FUGA (CONTADOR) ---
# La fuga es lo que pagas "de más" por no tener el sistema optimizado.
# Al subir el nivel, la factura residual baja y el contador SE RALENTIZA.
factura_inflada = factura_base * (1 + inflacion)
# Cuanto mayor es el pct_ahorro_final, menor es el remanente de fuga
fuga_mensual_real = factura_inflada * (1 - pct_ahorro_final)
fuga_por_segundo = fuga_mensual_real / (30 * 24 * 3600)

st.subheader("⏳ Fuga de capital por inacción:")
st.write(f"Estado: Automatización **{nivel}** aplicando un freno del **{int(pct_ahorro_final*100)}%** sobre la inflación.")

components.html(f"""
    <div style="background: #121212; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #ff4b4b;">
        <code style="color: #ff4b4b; font-size: 32px; text-shadow: 0 0 15px #ff4b4b; font-family: monospace;">
            € <span id="ticker">0.000000</span>
        </code>
    </div>
    <script>
        let acumulado = 0;
        const tasa = {fuga_por_segundo:.10f};
        function update() {{
            acumulado += tasa / 60;
            document.getElementById('ticker').innerText = acumulado.toFixed(6);
            requestAnimationFrame(update);
        }}
        update();
    </script>
""", height=100)

# --- 3. RECOMENDACIONES DE HARDWARE ---
st.subheader("🛠️ Tu Inventario Necesario")
st.write(f"Equipamiento para blindar {habitaciones} estancias:")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="item-box">💡 <b>{habitaciones * 2}</b> Luces Inteligentes</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="item-box">🔌 <b>{habitaciones + 1}</b> Enchufes con Medidor</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="item-box">🌡️ <b>{habitaciones}</b> Sensores de Clima</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="item-box">🧠 <b>1</b> Servidor Local (HA)</div>', unsafe_allow_html=True)

# --- 4. GRÁFICA Y PUNTO DE EQUILIBRIO ---
st.divider()
st.subheader("📈 Proyección: Inacción vs. Inversión")

inversion_inicial = 250 + (habitaciones * 50) # Inversión escalable según tamaño
años = list(range(11))
gasto_pasivo, gasto_soberano = [], []
acum_pasivo, acum_soberano = 0, inversion_inicial
mes_cruce = 0
cruce_encontrado = False

for m in range(121):
    año_actual = m // 12
    coste_mensual_inflado = factura_base * ((1 + inflacion) ** año_actual)
    
    acum_pasivo += coste_mensual_inflado
    # El sistema soberano gasta mucho menos cada mes
    acum_soberano += coste_mensual_inflado * (1 - pct_ahorro_final)
    
    if not cruce_encontrado and acum_soberano < acum_pasivo:
        mes_cruce = m
        cruce_encontrado = True
    
    if m % 12 == 0:
        gasto_pasivo.append(round(acum_pasivo, 2))
        gasto_soberano.append(round(acum_soberano, 2))

if cruce_encontrado:
    st.markdown(f'<div class="roi-badge">✅ PUNTO DE CRUCE: ¡Mes {mes_cruce}! Tu inversión se ha pagado sola</div>', unsafe_allow_html=True)

st.area_chart(pd.DataFrame({"Seguir igual": gasto_pasivo, "Inversión Soberana": gasto_soberano}, index=años), color=["#ff4b4b", "#2e7d32"])

# --- 5. TERMINOLOGÍA ---
with st.expander("📚 DICCIONARIO TÉCNICO"):
    glosario = {
        "🧠 Home Assistant": "El servidor que gestiona tu casa. Sin él, no hay automatización real.",
        "📡 Zigbee": "Protocolo inalámbrico eficiente. Al contrario que el Wi-Fi, no gasta energía extra del router.",
        "🧛 Consumo Vampiro": "El gasto invisible que tu nivel de automatización actual está frenando.",
        "🔒 Soberanía Digital": "La capacidad de que tu casa funcione sin depender de internet o nubes externas."
    }
    for t, d in glosario.items():
        st.markdown(f'<div class="glossary-card"><span class="termino">{t}:</span> {d}</div>', unsafe_allow_html=True)

# --- BOTÓN FINAL ---
st.divider()
if st.button("📡 COMPILAR MI HOJA DE RUTA", use_container_width=True, type="primary"):
    with st.status("Verificando topología...") as s:
        time.sleep(1)
        s.update(label=f"✅ Plan de rescate generado para {habitaciones} estancias", state="complete")
    st.link_button("📥 DESCARGAR PDF", "https://globaldomotica.substack.com/embed", use_container_width=True)