import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
st.set_page_config(
   page_title="Industrial Intelligence Dashboard",
   layout="wide"
)
# ------------------------------------------------
# ESTILOS CSS
# ------------------------------------------------
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], .stApp {
   background: linear-gradient(135deg,#050816,#071028,#0b1437);
   color: white;
}
/* Quitar franja blanca superior */
header {
   visibility: hidden;
}
[data-testid="stHeader"] {
   background: transparent;
}
.block-container {
   padding-top: 1rem;
   padding-left: 3.5rem;
   padding-right: 3.5rem;
}
/* Sidebar */
section[data-testid="stSidebar"] {
   background-color: #050816;
   border-right: 1px solid rgba(0,255,255,0.18);
}
section[data-testid="stSidebar"] * {
   color: white !important;
}
/* Selectbox moderno */
div[data-baseweb="select"] > div {
   background-color: rgba(255,255,255,0.07) !important;
   border: 1px solid rgba(0,245,255,0.35) !important;
   border-radius: 14px !important;
   color: white !important;
   min-height: 54px !important;
}
div[data-baseweb="select"] * {
   color: white !important;
}
div[data-baseweb="select"]:hover > div {
   border-color: #00F5FF !important;
   box-shadow: 0 0 15px rgba(0,245,255,0.25);
}
/* Título principal */
.main-title {
   font-size: 56px;
   font-weight: 900;
   color: white;
   line-height: 1.1;
   margin-bottom: 10px;
}
.subtitle {
   color: #94a3b8;
   font-size: 20px;
   margin-bottom: 40px;
   max-width: 950px;
}
/* KPI cards */
.kpi-card {
   background: rgba(255,255,255,0.045);
   border: 1px solid rgba(0,255,255,0.18);
   padding: 25px;
   border-radius: 20px;
   box-shadow: 0 0 25px rgba(0,255,255,0.08);
}
.kpi-title {
   color: #94a3b8;
   font-size: 16px;
   margin-bottom: 10px;
}
.kpi-value {
   color: white;
   font-size: 40px;
   font-weight: 800;
}
/* Secciones */
.section-title {
   color: white;
   font-size: 34px;
   font-weight: 800;
   margin-top: 40px;
   margin-bottom: 20px;
}
/* Tabs */
.stTabs [data-baseweb="tab"] {
   font-size: 17px;
   color: white;
}
.stTabs [aria-selected="true"] {
   color: #00F5FF !important;
}
/* Dataframe */
[data-testid="stDataFrame"] {
   border-radius: 15px;
   overflow: hidden;
}
/* Caja de insight */
.insight-box {
   background: rgba(255,255,255,0.045);
   border-left: 5px solid #00F5FF;
   padding: 22px;
   border-radius: 16px;
   color: #cbd5e1;
   font-size: 17px;
   margin-top: 20px;
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
       df["defectos"] / df["unidades_producidas"]
   )
   df["productividad_minuto"] = (
       df["unidades_producidas"] / df["tiempo_operacion_min"]
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
if datos_filtrados.empty:
   st.warning("No hay datos disponibles para los filtros seleccionados.")
   st.stop()
# ------------------------------------------------
# KPIS
# ------------------------------------------------
produccion_total = datos_filtrados["unidades_producidas"].sum()
defectos_totales = datos_filtrados["defectos"].sum()
tasa_defectos = defectos_totales / produccion_total
tiempo_promedio = datos_filtrados["tiempo_operacion_min"].mean()
productividad_promedio = datos_filtrados["productividad_minuto"].mean()
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
   fig_linea.update_traces(
       line=dict(width=4),
       marker=dict(size=10)
   )
   fig_linea.update_layout(
       paper_bgcolor="rgba(0,0,0,0)",
       plot_bgcolor="rgba(0,0,0,0)",
       font_color="white",
       xaxis=dict(gridcolor="#1e293b"),
       yaxis=dict(gridcolor="#1e293b"),
       margin=dict(l=20, r=20, t=40, b=20)
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
           "defectos": "sum",
           "unidades_producidas": "sum",
           "productividad_minuto": "mean"
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
       x=alt.X(
           "linea_produccion:N",
           title="Production Line"
       ),
       y=alt.Y(
           "tasa_defectos:Q",
           title="Defect Rate"
       ),
       color=alt.Color(
           "linea_produccion:N",
           scale=alt.Scale(
               range=[
                   "#00F5FF",
                   "#7C3AED",
                   "#00FFB3"
               ]
           ),
           legend=None
       ),
       tooltip=[
           alt.Tooltip("linea_produccion:N", title="Line"),
           alt.Tooltip("tasa_defectos:Q", title="Defect Rate", format=".2%"),
           alt.Tooltip("productividad_minuto:Q", title="Efficiency / Min", format=".2f")
       ]
   ).properties(
       height=420,
       background="transparent"
   ).configure_view(
       strokeWidth=0
   ).configure_axis(
       labelColor="white",
       titleColor="white",
       gridColor="#1e293b",
       domainColor="#1e293b"
   ).configure_legend(
       labelColor="white",
       titleColor="white"
   )
   st.altair_chart(
       grafico_altair,
       width="stretch"
   )
   st.markdown(
       '<div class="section-title">Efficiency by Production Line</div>',
       unsafe_allow_html=True
   )
   fig_productividad = px.bar(
       defectos_linea,
       x="linea_produccion",
       y="productividad_minuto",
       color="linea_produccion",
       text="productividad_minuto",
       color_discrete_sequence=[
           "#00F5FF",
           "#7C3AED",
           "#00FFB3"
       ]
   )
   fig_productividad.update_traces(
       texttemplate="%{text:.2f}",
       textposition="outside"
   )
   fig_productividad.update_layout(
       paper_bgcolor="rgba(0,0,0,0)",
       plot_bgcolor="rgba(0,0,0,0)",
       font_color="white",
       showlegend=False,
       xaxis=dict(gridcolor="#1e293b"),
       yaxis=dict(gridcolor="#1e293b"),
       margin=dict(l=20, r=20, t=40, b=20)
   )
   st.plotly_chart(fig_productividad, width="stretch")
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
       width="stretch",
       hide_index=True
   )
   st.markdown(
       '<div class="section-title">Executive Insight</div>',
       unsafe_allow_html=True
   )
   defectos_linea = (
       datos_filtrados
       .groupby("linea_produccion", as_index=False)
       .agg({
           "defectos": "sum",
           "unidades_producidas": "sum",
           "productividad_minuto": "mean"
       })
   )
   defectos_linea["tasa_defectos"] = (
       defectos_linea["defectos"] /
       defectos_linea["unidades_producidas"]
   )
   linea_top = (
       defectos_linea
       .sort_values("productividad_minuto", ascending=False)
       .iloc[0]["linea_produccion"]
   )
   linea_defectos = (
       defectos_linea
       .sort_values("tasa_defectos", ascending=False)
       .iloc[0]["linea_produccion"]
   )
   st.markdown(f"""
<div class="insight-box">
       The highest operational efficiency is currently achieved by
<b>{linea_top}</b>. The line with the highest defect rate is
<b>{linea_defectos}</b>. These results support decisions related to
       process optimization, quality control and production planning.
</div>
   """, unsafe_allow_html=True)
