"""
╔══════════════════════════════════════════════════════════════════╗
║     PORTAFOLIO JOVEN CONSERVADOR — App Streamlit                 ║
║     Deploy: Render.com                                           ║
╚══════════════════════════════════════════════════════════════════╝

CORRECCIONES APLICADAS:
  1. applymap() → map() (deprecated en pandas ≥ 2.1)
  2. Manejo robusto de columnas MultiIndex que yfinance genera
  3. Validación de activos_sel antes de operar sobre DataFrames vacíos
  4. rend_sel puede ser vacío si no hay activos seleccionados
  5. Cálculo de rend_total_port con prod() (más robusto que cumprod().iloc[-1])
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA
# ════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Portafolio Conservador · Actuaría",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS personalizado ─────────────────────────────────────────────────────────
st.markdown(
    """
<style>
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #f8f9fc; }

    .hero {
        background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #3949ab 100%);
        padding: 2rem 2.5rem;
        border-radius: 14px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .hero h1 { font-size: 2rem; font-weight: 700; margin: 0 0 0.3rem 0; }
    .hero p  { font-size: 1rem; opacity: 0.85; margin: 0; }

    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #3949ab;
        text-align: center;
    }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #1a237e; }
    .metric-label { font-size: 0.82rem; color: #666; margin-top: 2px; }

    .info-box {
        background: #e8eaf6;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border-left: 4px solid #3949ab;
        margin: 0.8rem 0;
        font-size: 0.92rem;
        color: #333;
    }

    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 6px 18px;
    }
    .stTabs [aria-selected="true"] {
        background: #1a237e !important;
        color: white !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ════════════════════════════════════════════════════════════
# CONSTANTES DEL PORTAFOLIO
# ════════════════════════════════════════════════════════════
PORTAFOLIO = {
    "SPY":  {"peso": 0.40, "nombre": "S&P 500 ETF",      "color": "#2196F3", "clase": "Renta Variable EE.UU."},
    "QQQ":  {"peso": 0.20, "nombre": "NASDAQ 100 ETF",    "color": "#FF5722", "clase": "Renta Variable Tech"},
    "URTH": {"peso": 0.15, "nombre": "MSCI World ETF",    "color": "#4CAF50", "clase": "Renta Variable Global"},
    "AGG":  {"peso": 0.15, "nombre": "US Bonds ETF",      "color": "#9C27B0", "clase": "Renta Fija"},
    "GLD":  {"peso": 0.10, "nombre": "Gold ETF (Oro)",    "color": "#FFC107", "clase": "Materia Prima"},
}

TICKERS = list(PORTAFOLIO.keys())
PESOS   = np.array([PORTAFOLIO[t]["peso"] for t in TICKERS])
TASA_RF = 0.045
DIAS    = 252

PERIODOS_MAP = {
    "1 Semana": 7,    "1 Mes": 30,      "3 Meses": 90,
    "6 Meses": 180,   "1 Año": 365,     "3 Años": 1095,
    "5 Años": 1825,   "10 Años": 3650,  "20 Años (máx)": 7300,
}

# ════════════════════════════════════════════════════════════
# CACHÉ DE DATOS
# ════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600, show_spinner=False)
def cargar_datos():
    """Descarga y procesa los datos históricos (cachea 1 hora)."""
    fecha_fin    = datetime.today()
    fecha_inicio = fecha_fin - timedelta(days=365 * 20)

    raw = yf.download(
        tickers     = TICKERS,
        start       = fecha_inicio.strftime("%Y-%m-%d"),
        end         = fecha_fin.strftime("%Y-%m-%d"),
        auto_adjust = True,
        progress    = False,
    )

    # FIX: yfinance puede devolver columnas MultiIndex (Close, SPY), (Close, QQQ)...
    # Aplanamos el MultiIndex si existe
    if isinstance(raw.columns, pd.MultiIndex):
        precios = raw["Close"][TICKERS].ffill().dropna()
    else:
        precios = raw[TICKERS].ffill().dropna()

    rendimientos = np.log(precios / precios.shift(1)).dropna()
    rend_port    = (rendimientos * PESOS).sum(axis=1)

    return precios, rendimientos, rend_port


# ════════════════════════════════════════════════════════════
# FUNCIONES AUXILIARES
# ════════════════════════════════════════════════════════════
def calcular_metricas(rendimientos_df: pd.DataFrame, precios_df: pd.DataFrame) -> pd.DataFrame:
    m = pd.DataFrame(index=rendimientos_df.columns)
    m["Nombre"]           = [PORTAFOLIO[t]["nombre"] for t in m.index]
    m["Peso (%)"]         = [int(PORTAFOLIO[t]["peso"] * 100) for t in m.index]
    m["Rend. Anual (%)"]  = (rendimientos_df.mean() * DIAS * 100).round(2)
    m["Volatilidad (%)"]  = (rendimientos_df.std()  * np.sqrt(DIAS) * 100).round(2)
    m["Sharpe"]           = (
        (m["Rend. Anual (%)"] / 100 - TASA_RF) / (m["Volatilidad (%)"] / 100)
    ).round(3)
    m["Rend. Total (%)"]  = ((precios_df.iloc[-1] / precios_df.iloc[0] - 1) * 100).round(2)
    return m


def calc_drawdown(precios_serie: pd.Series) -> pd.Series:
    maximo = precios_serie.cummax()
    return (precios_serie - maximo) / maximo * 100


def color_hex_a_rgba(hex_color: str, alpha: float = 0.12) -> str:
    h = hex_color.lstrip("#")
    r, g, b = tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"


# ════════════════════════════════════════════════════════════
# CARGA DE DATOS
# ════════════════════════════════════════════════════════════
with st.spinner("⏳ Cargando datos desde Yahoo Finance..."):
    try:
        PRECIOS, RENDIMIENTOS, REND_PORT = cargar_datos()
        datos_ok = True
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {e}")
        datos_ok = False
        st.stop()

# ════════════════════════════════════════════════════════════
# SIDEBAR — CONTROLES
# ════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚙️ Controles")

    st.markdown("### 📦 Activos")
    activos_sel = []
    for t in TICKERS:
        p = PORTAFOLIO[t]
        checked = st.checkbox(
            f"**{t}** — {p['nombre']} `{int(p['peso']*100)}%`",
            value=True,
            key=f"cb_{t}",
        )
        if checked:
            activos_sel.append(t)

    mostrar_port = st.checkbox("📊 Portafolio ponderado", value=True)

    st.divider()

    st.markdown("### 📅 Temporalidad")
    periodo_sel = st.select_slider(
        "Selecciona el período:",
        options=list(PERIODOS_MAP.keys()),
        value="5 Años",
    )

    st.divider()

    st.markdown("### 📉 Tipo de gráfica")
    tipo_graf = st.radio(
        "Visualización:",
        options=["norm", "rend", "vol", "dd"],
        format_func=lambda x: {
            "norm": "📈 Rendimiento acumulado (Base 100)",
            "rend": "📊 Rendimientos diarios (%)",
            "vol":  "〰️ Volatilidad móvil 30 días",
            "dd":   "📉 Drawdown desde máximo",
        }[x],
        index=0,
    )

    st.divider()
    st.caption(f"🕐 Datos al: **{PRECIOS.index[-1].strftime('%d %b %Y')}**")
    st.caption("📡 Fuente: Yahoo Finance · `yfinance`")
    st.caption("⚠️ Solo con fines educativos.")

# ════════════════════════════════════════════════════════════
# FILTRAR PERÍODO SELECCIONADO
# ════════════════════════════════════════════════════════════
dias_max    = PERIODOS_MAP[periodo_sel]
fecha_corte = PRECIOS.index[-1] - timedelta(days=dias_max)
precios_f   = PRECIOS.loc[PRECIOS.index >= fecha_corte]
rend_f      = RENDIMIENTOS.loc[RENDIMIENTOS.index >= fecha_corte]
rend_port_f = REND_PORT.loc[REND_PORT.index >= fecha_corte]

# Métricas del portafolio para el período seleccionado
rend_port_anual = rend_port_f.mean() * DIAS * 100
vol_port_anual  = rend_port_f.std()  * np.sqrt(DIAS) * 100
sharpe_port     = (rend_port_anual / 100 - TASA_RF) / (vol_port_anual / 100)
rend_total_port = ((1 + rend_port_f).prod() - 1) * 100   # FIX: prod() más robusto
vport_hist      = (1 + rend_port_f).cumprod() * 100
dd_max_port     = calc_drawdown(vport_hist).min()

# ════════════════════════════════════════════════════════════
# HEADER PRINCIPAL
# ════════════════════════════════════════════════════════════
st.markdown(
    """
<div class="hero">
  <h1>📊 Portafolio del Inversor Joven Conservador</h1>
  <p>Análisis cuantitativo de largo plazo · ETFs diversificados · Estrategia Buy &amp; Hold</p>
</div>
""",
    unsafe_allow_html=True,
)

# ════════════════════════════════════════════════════════════
# MÉTRICAS EN CARDS
# ════════════════════════════════════════════════════════════
col1, col2, col3, col4, col5 = st.columns(5)
metricas_cards = [
    (col1, f"{rend_port_anual:.1f}%",  "Rend. Anual",                  rend_port_anual >= 0),
    (col2, f"{vol_port_anual:.1f}%",   "Volatilidad",                  None),
    (col3, f"{sharpe_port:.2f}",       "Sharpe Ratio",                 sharpe_port >= 1),
    (col4, f"{rend_total_port:.1f}%",  f"Rend. Total ({periodo_sel})", rend_total_port >= 0),
    (col5, f"{dd_max_port:.1f}%",      "Drawdown Máx.",                False),
]
for col, valor, label, positivo in metricas_cards:
    with col:
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-value">{valor}</div>
            <div class="metric-label">{label}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# GRÁFICA PRINCIPAL
# ════════════════════════════════════════════════════════════
if not activos_sel and not mostrar_port:
    st.warning("⚠️ Selecciona al menos un activo en el panel lateral.")
else:
    # FIX: verificamos que activos_sel no esté vacío antes de indexar
    precios_sel = precios_f[activos_sel] if activos_sel else pd.DataFrame()
    rend_sel    = rend_f[activos_sel]    if activos_sel else pd.DataFrame()

    fig = go.Figure()
    titulo, ylabel = "", ""

    if tipo_graf == "norm":
        titulo, ylabel = "Rendimiento Acumulado (Base 100)", "Valor indexado"
        if not precios_sel.empty:
            norm = (precios_sel / precios_sel.iloc[0]) * 100
            for t in activos_sel:
                fig.add_trace(
                    go.Scatter(
                        x=norm.index, y=norm[t].round(2),
                        name=f"{t} — {PORTAFOLIO[t]['nombre']}",
                        line=dict(color=PORTAFOLIO[t]["color"], width=2.5),
                        hovertemplate=f"<b>{t}</b><br>%{{x|%d %b %Y}}<br>Valor: %{{y:.1f}}<extra></extra>",
                    )
                )
        if mostrar_port:
            vp = (1 + rend_port_f).cumprod() * 100
            fig.add_trace(
                go.Scatter(
                    x=vp.index, y=vp.round(2), name="📊 Portafolio",
                    line=dict(color="#212121", width=3.5, dash="dot"),
                    hovertemplate="<b>Portafolio</b><br>%{x|%d %b %Y}<br>Valor: %{y:.1f}<extra></extra>",
                )
            )
        fig.add_hline(y=100, line_dash="dash", line_color="gray", opacity=0.5)

    elif tipo_graf == "rend":
        titulo, ylabel = "Rendimientos Diarios (%)", "Rendimiento (%)"
        for t in activos_sel:
            fig.add_trace(
                go.Bar(
                    x=rend_sel.index, y=(rend_sel[t] * 100).round(3),
                    name=t, marker_color=PORTAFOLIO[t]["color"], opacity=0.75,
                )
            )
        if mostrar_port:
            fig.add_trace(
                go.Scatter(
                    x=rend_port_f.index, y=(rend_port_f * 100).round(3),
                    name="Portafolio", line=dict(color="black", width=2), mode="lines",
                )
            )

    elif tipo_graf == "vol":
        titulo, ylabel = "Volatilidad Anualizada Móvil 30 días (%)", "Volatilidad (%)"
        for t in activos_sel:
            vm = rend_sel[t].rolling(30).std() * np.sqrt(252) * 100
            fig.add_trace(
                go.Scatter(
                    x=vm.index, y=vm.round(2), name=t,
                    line=dict(color=PORTAFOLIO[t]["color"], width=2),
                    fill="tozeroy",
                    fillcolor=color_hex_a_rgba(PORTAFOLIO[t]["color"]),
                )
            )
        if mostrar_port:
            vp_vol = rend_port_f.rolling(30).std() * np.sqrt(252) * 100
            fig.add_trace(
                go.Scatter(
                    x=vp_vol.index, y=vp_vol.round(2), name="Portafolio",
                    line=dict(color="black", width=3, dash="dot"),
                )
            )

    elif tipo_graf == "dd":
        titulo, ylabel = "Drawdown desde Máximo (%)", "Drawdown (%)"
        for t in activos_sel:
            dd = calc_drawdown(precios_sel[t])
            fig.add_trace(
                go.Scatter(
                    x=dd.index, y=dd.round(2), name=t,
                    line=dict(color=PORTAFOLIO[t]["color"], width=1.8),
                    fill="tozeroy",
                    fillcolor=color_hex_a_rgba(PORTAFOLIO[t]["color"], 0.15),
                    hovertemplate=f"<b>{t}</b><br>%{{x|%d %b %Y}}<br>Caída: %{{y:.1f}}%<extra></extra>",
                )
            )
        if mostrar_port:
            vp = (1 + rend_port_f).cumprod()
            dp = calc_drawdown(vp)
            fig.add_trace(
                go.Scatter(
                    x=dp.index, y=dp.round(2), name="Portafolio",
                    line=dict(color="black", width=3, dash="dot"),
                )
            )

    fig.update_layout(
        title=dict(
            text=f"<b>{titulo}</b> · {periodo_sel}",
            font=dict(size=16, color="#1a237e"), x=0.01,
        ),
        xaxis=dict(title="Fecha", showgrid=True, gridcolor="#f0f0f0",
                   rangeslider=dict(visible=True, thickness=0.04)),
        yaxis=dict(title=ylabel, showgrid=True, gridcolor="#f0f0f0"),
        legend=dict(orientation="v", x=1.01, y=1, bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="#ddd", borderwidth=1),
        hovermode="x unified",
        height=520,
        margin=dict(l=60, r=20, t=60, b=50),
        plot_bgcolor="white",
        paper_bgcolor="#f8f9fc",
        font=dict(family="Inter", size=12),
    )
    st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════
# TABS DE ANÁLISIS
# ════════════════════════════════════════════════════════════
st.markdown("---")
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Métricas del Período",
    "🔗 Correlaciones",
    "💰 Simulación de Inversión",
    "📚 Filosofía del Portafolio",
])

# ── Tab 1: Métricas ──────────────────────────────────────────────────────────
with tab1:
    if activos_sel and not rend_sel.empty:
        met = calcular_metricas(rend_sel, precios_sel)
        met_port = {
            "Nombre":          "Portafolio Ponderado",
            "Peso (%)":        100,
            "Rend. Anual (%)": round(rend_port_anual, 2),
            "Volatilidad (%)": round(vol_port_anual, 2),
            "Sharpe":          round(sharpe_port, 3),
            "Rend. Total (%)": round(rend_total_port, 2),
        }
        met_total = pd.concat([met, pd.DataFrame([met_port], index=["PORTAFOLIO"])])

        def color_sharpe(val):
            if not isinstance(val, (int, float)):
                return ""
            if val >= 1.5: return "background-color: #c8e6c9"
            if val >= 1.0: return "background-color: #fff9c4"
            if val >= 0:   return "background-color: #ffe0b2"
            return "background-color: #ffcdd2"

        # FIX: applymap() fue deprecado en pandas 2.1 → usar map()
        st.dataframe(
            met_total.style.map(color_sharpe, subset=["Sharpe"]),
            use_container_width=True,
            height=280,
        )
        st.caption("🟢 Sharpe ≥ 1.5 excelente · 🟡 ≥ 1.0 bueno · 🟠 ≥ 0 aceptable · 🔴 < 0 negativo")
    else:
        st.info("Selecciona activos en el sidebar para ver métricas.")

# ── Tab 2: Correlaciones ─────────────────────────────────────────────────────
with tab2:
    if activos_sel and len(activos_sel) >= 2:
        corr = rend_sel.corr().round(3)
        nombres_corr = [PORTAFOLIO[t]["nombre"] for t in activos_sel]
        fig_c = go.Figure(
            go.Heatmap(
                z=corr.values, x=nombres_corr, y=nombres_corr,
                colorscale="RdYlGn", zmin=-1, zmax=1,
                text=corr.values.round(2), texttemplate="%{text}", showscale=True,
            )
        )
        fig_c.update_layout(
            title="<b>Matriz de Correlación de Rendimientos</b>",
            height=420, margin=dict(l=10, r=10, t=50, b=10),
        )
        st.plotly_chart(fig_c, use_container_width=True)
        st.markdown(
            """
        <div class="info-box">
        💡 <b>Cómo interpretar:</b> Un valor cercano a <b>-1</b> indica que los activos se mueven en
        direcciones opuestas (excelente para diversificación). Cercano a <b>+1</b> se mueven juntos
        (poca diversificación). La correlación baja entre AGG/GLD y las acciones es la razón clave
        por la que los incluimos.
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.info("Selecciona al menos 2 activos para ver la matriz de correlación.")

# ── Tab 3: Simulación ────────────────────────────────────────────────────────
with tab3:
    col_a, col_b = st.columns([1, 3])
    with col_a:
        inversion = st.number_input(
            "💵 Inversión inicial (USD):",
            min_value=100, max_value=1_000_000, value=10_000, step=500,
        )
        aportacion = st.number_input(
            "📅 Aportación mensual (USD):",
            min_value=0, max_value=10_000, value=200, step=50,
        )
        horizonte_sim = st.slider(
            "📆 Horizonte (años de datos):", min_value=1, max_value=20, value=10
        )

    with col_b:
        fecha_sim   = PRECIOS.index[-1] - timedelta(days=365 * horizonte_sim)
        precios_sim = PRECIOS.loc[PRECIOS.index >= fecha_sim]
        rend_sim    = REND_PORT.loc[REND_PORT.index >= fecha_sim]

        # Simulación con aportaciones mensuales
        valor_sim  = []
        capital    = float(inversion)
        mes_actual = None
        for fecha, rend in rend_sim.items():
            if mes_actual is None or fecha.month != mes_actual:
                capital   += aportacion
                mes_actual = fecha.month
            capital *= 1 + rend
            valor_sim.append(capital)

        serie_sim = pd.Series(valor_sim, index=rend_sim.index)
        serie_bah = inversion * (1 + rend_sim).cumprod()

        fig_s = go.Figure()
        fig_s.add_trace(
            go.Scatter(
                x=serie_sim.index, y=serie_sim.round(0),
                name=f"Con aportaciones ${aportacion}/mes",
                line=dict(color="#1a237e", width=2.5),
                fill="tozeroy", fillcolor="rgba(26,35,126,0.06)",
            )
        )
        fig_s.add_trace(
            go.Scatter(
                x=serie_bah.index, y=serie_bah.round(0),
                name="Solo inversión inicial",
                line=dict(color="#FF5722", width=2, dash="dash"),
            )
        )
        fig_s.add_hline(
            y=inversion, line_dash="dot", line_color="gray",
            annotation_text=f"Inversión inicial ${inversion:,}",
        )

        total_aportado = inversion + aportacion * 12 * horizonte_sim
        ganancia_sim   = serie_sim.iloc[-1] - total_aportado

        fig_s.update_layout(
            title=(
                f"<b>Simulación de Inversión — {horizonte_sim} años</b><br>"
                f'<span style="color:#2e7d32">Valor final: ${serie_sim.iloc[-1]:,.0f} | '
                f"Ganancia: ${ganancia_sim:,.0f}</span>"
            ),
            xaxis=dict(title="Fecha"),
            yaxis=dict(title="Valor (USD)", tickprefix="$"),
            height=420, hovermode="x unified", plot_bgcolor="white",
        )
        st.plotly_chart(fig_s, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Total aportado",  f"${total_aportado:,.0f}")
        c2.metric("Valor final",     f"${serie_sim.iloc[-1]:,.0f}")
        c3.metric("Ganancia neta",   f"${ganancia_sim:,.0f}",
                  f"{(ganancia_sim / total_aportado * 100):.1f}%")

# ── Tab 4: Filosofía ─────────────────────────────────────────────────────────
with tab4:
    st.markdown("### 🎯 ¿Por qué este portafolio?")

    col_i, col_ii = st.columns(2)
    with col_i:
        st.markdown(
            """
        **El inversor joven conservador:**
        - 📅 Horizonte de 15–20 años
        - 🛡️ Tolera algo de volatilidad pero evita especulación
        - 💡 Estrategia pasiva (*buy & hold* + rebalanceo anual)
        - 💸 Contribuciones periódicas mensuales

        **Principios del portafolio:**
        1. **Diversificación real** — 5 clases de activos con correlaciones bajas entre sí
        2. **Costos mínimos** — todos los ETFs tienen expense ratio < 0.20%/año
        3. **Exposición global** — no solo EE.UU., también Europa, Asia y mercados emergentes
        4. **Escudo anti-inflación** — el oro protege el poder adquisitivo en crisis
        5. **Estabilidad** — los bonos reducen la volatilidad global del portafolio
        """
        )
    with col_ii:
        fig_pie = go.Figure(
            go.Pie(
                labels=[f"{t} — {PORTAFOLIO[t]['nombre']}" for t in TICKERS],
                values=PESOS * 100,
                marker_colors=[PORTAFOLIO[t]["color"] for t in TICKERS],
                hole=0.45,
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>Peso: %{value}%<extra></extra>",
            )
        )
        fig_pie.update_layout(
            title="<b>Composición del Portafolio</b>",
            height=380, margin=dict(l=10, r=10, t=50, b=10), showlegend=False,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown(
        """
    <div class="info-box">
    ⚠️ <b>Disclaimer:</b> Esta aplicación es exclusivamente educativa. No constituye
    asesoramiento financiero ni de inversión. Los rendimientos pasados no garantizan
    resultados futuros. Antes de invertir, consulta a un asesor financiero certificado.
    </div>
    """,
        unsafe_allow_html=True,
    )

# ════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#999; font-size:0.82rem'>"
    "📊 Portafolio Joven Conservador · Curso Manejo de Datos · Actuaría · "
    "Desarrollado con Streamlit + yfinance + Plotly"
    "</div>",
    unsafe_allow_html=True,
)
