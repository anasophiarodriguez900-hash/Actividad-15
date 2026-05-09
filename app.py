import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# ------------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------------

st.set_page_config(
    page_title="Industrial Intelligence Dashboard",
    layout="wide"
)

# ------------------------------------------------
# ESTILOS CSS
# ------------------------------------------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#050816,#071028,#0b1437);
    color:white;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background-color:#050816;
    border-right:1px solid rgba(0,255,255,0.15);
}

/* Título principal */
.main-title{
    font-size:60px;
    font-weight:900;
    color:white;
    line-height:1.1;
    margin-bottom:10px;
}

.subtitle{
    color:#94a3b8;
    font-size:20px;
    margin-bottom:40px;
}

/* KPI cards */
.kpi-card{
    background: rgba(255,255,255,0.04);
    border:1px solid rgba(0,255,255,0.15);
    padding:25px;
    border-radius:20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 0 25px rgba(0,255,255,0.08);
}

.kpi-title{
    color:#94a3b8;
    font-size:16px;
}

.kpi-value{
    color:white;
    font-size:42px;
    font-weight:800;
}

/* Secciones */
.section-title{
    color:white;
    font-size:36px;
    font-weight:800;
    margin-top:40px;
    margin-bottom:20px;
}

/* Tabs */
.stTabs [data-baseweb="tab"]{
    font-size:18px;
    color:white;
}

/* Dataframe */
[data-testid="stDataFrame"]{
    border-radius:15px;
    overflow:hidden;
}

/* Selectbox */
.stSelectbox label{
    color:white !important;
    font-size:18px;
}

/* Sidebar text */
section[data-testid="stSidebar"] *{
    color:white !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# CARGA DE DATOS
# ------------------------------------------------

@st.cache_data
def cargar_datos():
    df = pd.read_csv("produccion_industrial.csv")

    df["fecha"] = pd.to_datetime(df["fecha"])

    df["tasa_defectos"] = (
        df["defectos"] /
        df["unidades_producidas"]
    )

    df["productividad_minuto"] = (
        df["unidades_producidas"] /
        df["tiempo_operacion_min"]
    )

    return df

datos = cargar_datos()

# ------------------------------------------------
# VALIDACIÓN
# ------------------------------------------------

columnas_requeridas = [
    "fecha",
    "linea_produccion",
    "turno",
    "unidades_producidas",
    "defectos",
    "tiempo_operacion_min"
]

faltantes = [
    col for col in columnas_requeridas
    if col not in datos.columns
]

if faltantes:
    st.error(f"Faltan columnas: {faltantes}")
    st.stop()

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.markdown("# Industrial Filters")

lineas = ["Todas"] + sorted(datos["linea_produccion"].unique())
turnos = ["Todos"] + sorted(datos["turno"].unique())

linea = st.sidebar.selectbox(
    "Production Line",
    lineas
)

turno = st.sidebar.selectbox(
    "Shift",
    turnos
)

# ------------------------------------------------
# FILTROS
# ------------------------------------------------

datos_filtrados = datos.copy()

if linea != "Todas":
    datos_filtrados = datos_filtrados[
        datos_filtrados["linea_produccion"] == linea
    ]

if turno != "Todos":
    datos_filtrados = datos_filtrados[
        datos_filtrados["turno"] == turno
    ]

# ------------------------------------------------
# KPIS
# ------------------------------------------------

produccion_total = datos_filtrados["unidades_producidas"].sum()

defectos_totales = datos_filtrados["defectos"].sum()

tasa_defectos = defectos_totales / produccion_total

tiempo_promedio = (
    datos_filtrados["tiempo_operacion_min"].mean()
)

productividad_promedio = (
    datos_filtrados["productividad_minuto"].mean()
)

# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.markdown("""
<div class="main-title">
Industrial Intelligence Dashboard
</div>

<div class="subtitle">
Real-time operational analysis for production efficiency,
quality control and industrial performance.
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------
# KPI CARDS
# ------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Production Volume</div>
        <div class="kpi-value">{produccion_total:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Defect Rate</div>
        <div class="kpi-value">{tasa_defectos:.2%}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Average Time</div>
        <div class="kpi-value">{tiempo_promedio:.1f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Efficiency / Min</div>
        <div class="kpi-value">{productividad_promedio:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------
# TABS
# ------------------------------------------------

tab1, tab2, tab3 = st.tabs([
    "Performance Trend",
    "Operational Comparison",
    "Detailed Analysis"
])

# ------------------------------------------------
# TAB 1
# ------------------------------------------------

with tab1:

    st.markdown(
        '<div class="section-title">Production Trend</div>',
        unsafe_allow_html=True
    )

    produccion_fecha = (
        datos_filtrados
        .groupby("fecha", as_index=False)["unidades_producidas"]
        .sum()
    )

    fig_linea = px.line(
        produccion_fecha,
        x="fecha",
        y="unidades_producidas",
        markers=True,
        color_discrete_sequence=["#00F5FF"]
    )

    fig_linea.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(fig_linea, width="stretch")

# ------------------------------------------------
# TAB 2
# ------------------------------------------------

with tab2:

    st.markdown(
        '<div class="section-title">Operational Comparison</div>',
        unsafe_allow_html=True
    )

    defectos_linea = (
        datos_filtrados
        .groupby("linea_produccion", as_index=False)
        .agg({
            "defectos":"sum",
            "unidades_producidas":"sum",
            "productividad_minuto":"mean"
        })
    )

    defectos_linea["tasa_defectos"] = (
        defectos_linea["defectos"] /
        defectos_linea["unidades_producidas"]
    )

    grafico_altair = alt.Chart(defectos_linea).mark_bar(
        cornerRadiusTopLeft=8,
        cornerRadiusTopRight=8
    ).encode(
        x="linea_produccion",
        y="tasa_defectos",
        color=alt.Color(
            "linea_produccion",
            scale=alt.Scale(
                range=[
                    "#00F5FF",
                    "#7C3AED",
                    "#00FFB3"
                ]
            )
        ),
        tooltip=[
            "linea_produccion",
            alt.Tooltip(
                "tasa_defectos:Q",
                format=".2%"
            )
        ]
    ).properties(
        width=700,
        height=400
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        labelColor="white",
        titleColor="white",
        gridColor="#1e293b"
    ).configure(
        background="transparent"
    )

    st.altair_chart(
        grafico_altair,
        width="stretch"
    )

# ------------------------------------------------
# TAB 3
# ------------------------------------------------

with tab3:

    st.markdown(
        '<div class="section-title">Detailed Operational Data</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        datos_filtrados,
        width="stretch"
    )

    st.markdown(
        '<div class="section-title">Executive Insight</div>',
        unsafe_allow_html=True
    )

    linea_top = (
        defectos_linea
        .sort_values(
            "productividad_minuto",
            ascending=False
        )
        .iloc[0]["linea_produccion"]
    )

    st.info(
        f"""
        The highest operational efficiency is currently achieved by
        {linea_top}, showing superior production performance
        relative to operational time.
        """
    )