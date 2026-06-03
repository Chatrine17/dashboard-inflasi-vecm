"""
InflasiID - Analisis Inflasi & Nilai Tukar Indonesia
Streamlit App: VECM Time Series Analysis Dashboard
"""

import io
import warnings
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.vector_ar.vecm import VECM, select_coint_rank, select_order as vecm_select_order
from statsmodels.tsa.vector_ar.var_model import VAR

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="InflasiID – Analisis Runtun Waktu",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL STYLE
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1b2d 0%, #162035 60%, #1a2847 100%);
    border-right: 1px solid #243050;
}
[data-testid="stSidebar"] * { color: #c8d6f0 !important; }

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Main content bg */
[data-testid="stAppViewContainer"] > .main {
    background: #f0f4fb;
}

/* Card base */
.card {
    background: white;
    border-radius: 16px;
    padding: 20px 24px;
    box-shadow: 0 2px 12px rgba(15,27,45,0.08);
    margin-bottom: 16px;
}

/* Metric cards */
.metric-card {
    background: white;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(15,27,45,0.07);
    border-left: 4px solid #4f7ef8;
    height: 100%;
}
.metric-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #8a99b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 1.6rem;
    font-weight: 800;
    color: #0f1b2d;
    line-height: 1.1;
    font-family: 'JetBrains Mono', monospace;
}
.metric-sub {
    font-size: 0.72rem;
    color: #8a99b8;
    margin-top: 6px;
}
.metric-live-dot {
    display: inline-block;
    width: 7px; height: 7px;
    background: #22c55e;
    border-radius: 50%;
    margin-right: 5px;
    animation: blink 1.4s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #1e3a8a 0%, #3b5fc0 50%, #6366f1 100%);
    border-radius: 18px;
    padding: 32px 36px;
    color: white;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hero-banner::after {
    content: '';
    position: absolute;
    right: -60px; top: -60px;
    width: 240px; height: 240px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
}
.hero-title {
    font-size: 1.9rem;
    font-weight: 800;
    margin: 0 0 8px 0;
    line-height: 1.2;
}
.hero-sub {
    font-size: 0.9rem;
    opacity: 0.82;
    margin: 0;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 30px;
    padding: 4px 14px;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 14px;
}

/* Accent cards */
.accent-red {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
    border-radius: 14px;
    padding: 22px;
}
.accent-blue {
    background: linear-gradient(135deg, #0ea5e9, #0284c7);
    color: white;
    border-radius: 14px;
    padding: 22px;
}
.accent-label {
    font-size: 0.7rem;
    font-weight: 700;
    opacity: 0.85;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}
.accent-value {
    font-size: 1.8rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    margin: 4px 0 2px 0;
}
.accent-sub { font-size: 0.72rem; opacity: 0.8; }

/* Section header */
.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f1b2d;
    margin-bottom: 4px;
    border-left: 4px solid #4f7ef8;
    padding-left: 12px;
}
.section-sub {
    font-size: 0.8rem;
    color: #8a99b8;
    margin-bottom: 20px;
    margin-left: 16px;
}

/* Table styling */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

/* Status badges */
.badge-green {
    display: inline-block;
    background: #dcfce7; color: #16a34a;
    border-radius: 20px; padding: 3px 12px;
    font-size: 0.75rem; font-weight: 700;
}
.badge-red {
    display: inline-block;
    background: #fee2e2; color: #dc2626;
    border-radius: 20px; padding: 3px 12px;
    font-size: 0.75rem; font-weight: 700;
}
.badge-blue {
    display: inline-block;
    background: #dbeafe; color: #1d4ed8;
    border-radius: 20px; padding: 3px 12px;
    font-size: 0.75rem; font-weight: 700;
}

/* Forecasting result boxes */
.test-box {
    background: white;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(15,27,45,0.07);
    margin-bottom: 16px;
}
.test-tag {
    display: inline-block;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 10px;
}
.tag-test1 { background: #e0f2fe; color: #0369a1; }
.tag-test2 { background: #f0fdf4; color: #15803d; }
.tag-eval  { background: #faf5ff; color: #7e22ce; }
.tag-forecast { background: #fff7ed; color: #c2410c; }

.note-box {
    background: linear-gradient(135deg, #06b6d4, #0ea5e9);
    border-radius: 12px;
    padding: 14px 20px;
    color: white;
    font-size: 0.82rem;
    font-weight: 600;
}

/* Info list items */
.info-item {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 14px 0;
    border-bottom: 1px solid #f0f4fb;
}
.info-icon {
    width: 38px; height: 38px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
}
.info-icon-blue { background: #dbeafe; }
.info-icon-purple { background: #ede9fe; }
.info-icon-green { background: #dcfce7; }
.info-text-title { font-weight: 700; color: #0f1b2d; font-size: 0.88rem; }
.info-text-sub { color: #8a99b8; font-size: 0.78rem; margin-top: 2px; }

/* Sidebar logo area */
.sidebar-logo {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 0 20px 0;
}
.sidebar-logo-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #4f7ef8, #6366f1);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
}
.sidebar-logo-text { font-size: 1.15rem; font-weight: 800; color: white !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADING (OTOMATIS DARI LOKAL)
# ─────────────────────────────────────────────
import os

@st.cache_data
def load_local_data():
    file_excel = "dataset_final.xlsx"
    file_csv = "dataset_final.csv"
    
    # Coba baca file Excel dulu, kalau tidak ada baru CSV
    if os.path.exists(file_excel):
        df = pd.read_excel(file_excel)
    elif os.path.exists(file_csv):
        with open(file_csv, 'r', encoding='utf-8', errors='replace') as f:
            lines = [ln.rstrip(";").rstrip(",").rstrip() for ln in f.readlines()]
        df = pd.read_csv(io.StringIO("\n".join(lines)))
    else:
        return None, None, None, None

    df.columns = df.columns.str.strip().str.lower()
    
    tanggal_col = next((c for c in df.columns if "tanggal" in c or "date" in c), None)
    inflasi_col = next((c for c in df.columns if "inflasi" in c or "inflation" in c), None)
    kurs_col = next((c for c in df.columns if "tukar" in c or "kurs" in c or "exchange" in c or "rate" in c), None)

    if not all([tanggal_col, inflasi_col, kurs_col]):
        return None, None, None, None

    df[tanggal_col] = pd.to_datetime(df[tanggal_col])
    df[inflasi_col] = pd.to_numeric(df[inflasi_col], errors="coerce")
    df[kurs_col] = pd.to_numeric(df[kurs_col], errors="coerce")
    df = df.dropna(subset=[inflasi_col, kurs_col])
    df = df.sort_values(tanggal_col).reset_index(drop=True)
    
    return df, tanggal_col, inflasi_col, kurs_col

@st.cache_data
def prepare_model_data(df: pd.DataFrame, tanggal_col: str, inflasi_col: str, kurs_col: str) -> pd.DataFrame:
    model_df = df[[tanggal_col, inflasi_col, kurs_col]].copy()
    model_df = model_df.set_index(tanggal_col)
    model_df.columns = ["inflasi yoy %", "nilai tukar usd idr"]
    model_df.index = pd.to_datetime(model_df.index)
    model_df = model_df.sort_index()
    return model_df

# Inisialisasi otomatis dataset saat aplikasi berjalan
if "df" not in st.session_state or st.session_state.df is None:
    df, t_col, i_col, k_col = load_local_data()
    if df is not None and not df.empty:
        st.session_state.df = df
        st.session_state.tanggal_col = t_col
        st.session_state.inflasi_col = i_col
        st.session_state.kurs_col = k_col
        st.session_state.model_data = prepare_model_data(df, t_col, i_col, k_col)
    else:
        st.session_state.df = None

# ─────────────────────────────────────────────
# VECM ANALYSIS ENGINE
# ─────────────────────────────────────────────
def run_stationarity_tests(data_model: pd.DataFrame):
    results = []
    for col in data_model.columns:
        adf_res = adfuller(data_model[col], regression="c", autolag="AIC")
        try:
            kpss_res = kpss(data_model[col], regression="c", nlags="auto")
            kpss_p = kpss_res[1]
        except Exception:
            kpss_p = None

        adf_p = adf_res[1]
        if adf_p < 0.05:
            conclusion = "Stasioner di level"
            status = "green"
        else:
            conclusion = "Non-stasioner, perlu differencing"
            status = "red"

        results.append({
            "Variabel": "Inflasi YoY (%)" if "inflasi" in col else "Nilai Tukar USD/IDR",
            "ADF Level p-value": round(adf_p, 3),
            "KPSS Level p-value": round(kpss_p, 3) if kpss_p else "N/A",
            "Kesimpulan": conclusion,
            "Status": status,
        })
    return results


def run_johansen_test(data_model: pd.DataFrame, k_ar_diff: int):
    DET_ORDER = -1
    try:
        ct = select_coint_rank(data_model, det_order=DET_ORDER, k_ar_diff=k_ar_diff, method="trace", signif=0.05)
        rank = ct.rank
    except Exception:
        rank = 1
    return rank, DET_ORDER


def get_optimal_lag(data_model: pd.DataFrame, max_lags: int) -> int:
    try:
        lo = vecm_select_order(data_model, maxlags=max_lags, deterministic="ci")
        p = int(lo.aic) if lo.aic is not None else 1
        return max(1, p)
    except Exception:
        return 1


def run_vecm_forecast(data_model: pd.DataFrame, horizon: int, cutoff: str = "2023-12-31"):
    n_obs = len(data_model)
    max_lags = min(12, max(2, n_obs // 6))

    p_level = get_optimal_lag(data_model, max_lags)
    k_ar_diff = max(0, p_level - 1)

    # Stationarity
    stat_results = run_stationarity_tests(data_model)

    # Johansen
    coint_rank, det_order = run_johansen_test(data_model, k_ar_diff)

    det_string = "nc" if det_order == -1 else "ci"

    # Train/Test split
    train_data = data_model.loc[:cutoff]
    test_data = data_model.loc[cutoff:].iloc[1:]

    # Fit on train
    model_train = VECM(train_data, k_ar_diff=k_ar_diff, coint_rank=max(1, coint_rank), deterministic=det_string).fit()
    preds_raw = model_train.predict(steps=len(test_data))

    # Metrics
    metrics = []
    for i, col in enumerate(data_model.columns):
        actual = test_data.iloc[:, i].values
        pred = preds_raw[:, i]
        mae = mean_absolute_error(actual, pred)
        rmse = np.sqrt(mean_squared_error(actual, pred))
        try:
            mape = mean_absolute_percentage_error(actual, pred) * 100
        except Exception:
            mape = np.nan
        metrics.append({
            "Variabel": "Inflasi YoY" if i == 0 else "Nilai Tukar USD/IDR",
            "MAE": round(mae, 3),
            "RMSE": round(rmse, 3),
            "MAPE (%)": round(mape, 2) if not np.isnan(mape) else "N/A",
        })

    # Future forecast – fit on full data
    model_full = VECM(data_model, k_ar_diff=k_ar_diff, coint_rank=max(1, coint_rank), deterministic=det_string).fit()
    future_preds = model_full.predict(steps=horizon)

    last_date = data_model.index[-1]
    future_dates = pd.date_range(start=last_date + pd.offsets.MonthBegin(1), periods=horizon, freq="MS")

    future_df = pd.DataFrame(future_preds, columns=["inflasi yoy %", "nilai tukar usd idr"], index=future_dates)

    # Confidence bands (±1 std of residuals * sqrt(step))
    resid_std = model_full.resid.std(axis=0)
    ci_bands = []
    for step in range(1, horizon + 1):
        ci_bands.append(resid_std * np.sqrt(step) * 1.96)
    ci_df = pd.DataFrame(ci_bands, columns=["ci_inflasi", "ci_kurs"], index=future_dates)

    return {
        "stat_results": stat_results,
        "coint_rank": coint_rank,
        "det_order": det_order,
        "metrics": metrics,
        "future_df": future_df,
        "ci_df": ci_df,
        "train_data": train_data,
        "test_data": test_data,
        "preds_raw": preds_raw,
        "data_model": data_model,
    }


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">📈</div>
        <span class="sidebar-logo-text">InflasiID</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    page = st.radio(
        "Navigasi",
        ["🏠  Beranda", "📋  Dataset", "📊  Grafik", "🔮  Forecasting"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.72rem; color:#4a6080; line-height:1.7;'>
    <b style='color:#8a99b8'>Model:</b> VECM / VAR<br>
    <b style='color:#8a99b8'>Uji:</b> ADF, KPSS, Johansen<br>
    <b style='color:#8a99b8'>Metrik:</b> MAE, RMSE, MAPE<br>
    <b style='color:#8a99b8'>Data:</b> Jan 2020 – Apr 2026
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE – hold uploaded data across pages
# ─────────────────────────────────────────────
if "df" not in st.session_state:
    st.session_state.df = None
    st.session_state.tanggal_col = None
    st.session_state.inflasi_col = None
    st.session_state.kurs_col = None
    st.session_state.model_data = None


# ─────────────────────────────────────────────
# HELPER: require dataset loaded
# ─────────────────────────────────────────────
def require_data():
    if st.session_state.df is None:
        st.info("📋 Silakan unggah dataset di halaman **Dataset** terlebih dahulu.")
        st.stop()

# ═══════════════════════════════════════════════
# PAGE LOGIC
# ═══════════════════════════════════════════════

if page == "🏠  Beranda":
    # 1. Kotak Biru (Hero Banner)
    st.markdown("""
    <div class="hero-banner" style="text-align: center;">
        <div class="hero-badge" style="margin: 0 auto 14px auto; display: inline-block;">🌟 Dashboard Analisis</div>
        <p class="hero-title" style="font-size: 2.8rem; line-height: 1.3; margin-bottom: 10px;">Analisis Inflasi dan<br>Nilai Tukar Indonesia</p>
        <p class="hero-sub" style="font-size: 1.1rem;">Analisis Runtun Waktu dengan Model VECM/VAR</p>
    </div>
    """, unsafe_allow_html=True)

    # Blok Kredit Tim Menggunakan Fitur Bawaan Streamlit (Sangat Aman & Anti Error)
    st.markdown("""
    <div style="background: white; border-radius: 16px; padding: 24px; border-left: 5px solid #1e3a8a; box-shadow: 0 4px 15px rgba(0,0,0,0.04); margin-bottom: 24px;">
        <h3 style="margin-top: 0; color: #0f1b2d; font-size: 1.5rem; margin-bottom: 5px; font-weight: 800;">Project Analisis Runtun Waktu</h3>
        <div style="color: #4f7ef8; font-weight: 700; font-size: 1rem; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 0.05em;">S-1 Matematika | Universitas Negeri Medan</div>
    </div>
    """, unsafe_allow_html=True)

    # Membuat grid 2x2 tanpa HTML (Pasti Berhasil)
    col_nama1, col_nama2 = st.columns(2)
    with col_nama1:
        st.info("👤 Agnes Margareta Nainggolan (4233530003)")
        st.info("👤 Cindy Injilia S (4233230007)")
    with col_nama2:
        st.info("👤 Chatrine Zefania Manurung (4233230015)")
        st.info("👤 Luviarti Manurung (4233530015)")
        
    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.df is not None:
        df = st.session_state.df
        inflasi_col = st.session_state.inflasi_col
        kurs_col = st.session_state.kurs_col
        tanggal_col = st.session_state.tanggal_col

        latest_inflasi = df[inflasi_col].iloc[-1]
        latest_kurs = df[kurs_col].iloc[-1]
        total_obs = len(df)
        latest_date = df[tanggal_col].iloc[-1].strftime("%B %Y")
        date_min = df[tanggal_col].iloc[0].strftime("%b %Y")
        date_max = df[tanggal_col].iloc[-1].strftime("%b %Y")
        peak_inflasi = df[inflasi_col].max()
        peak_inflasi_date = df.loc[df[inflasi_col].idxmax(), tanggal_col].strftime("%B %Y")
        peak_kurs = df[kurs_col].max()
        peak_kurs_date = df.loc[df[kurs_col].idxmax(), tanggal_col].strftime("%B %Y")

        # Top metric cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color:#4f7ef8;">
                <div class="metric-label"><span class="metric-live-dot"></span>Inflasi YoY Terkini</div>
                <div class="metric-value" style="color:#ef4444;">{latest_inflasi:.2f}%</div>
                <div class="metric-sub">📅 {latest_date}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color:#0ea5e9;">
                <div class="metric-label"><span class="metric-live-dot"></span>Nilai Tukar USD/IDR</div>
                <div class="metric-value" style="color:#0f1b2d;">Rp {latest_kurs:,.0f}</div>
                <div class="metric-sub">📅 {latest_date}</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card" style="border-left-color:#8b5cf6;">
                <div class="metric-label">Total Observasi</div>
                <div class="metric-value" style="color:#7c3aed;">{total_obs} bulan</div>
                <div class="metric-sub">📅 {date_min} – {date_max}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col4, col5 = st.columns(2)
        with col4:
            st.markdown(f"""
            <div class="accent-red">
                <div class="accent-label">📈 Puncak Inflasi</div>
                <div class="accent-value">{peak_inflasi:.2f}%</div>
                <div class="accent-sub">📅 {peak_inflasi_date}</div>
            </div>""", unsafe_allow_html=True)
        with col5:
            st.markdown(f"""
            <div class="accent-blue">
                <div class="accent-label">💵 Kurs Tertinggi</div>
                <div class="accent-value">Rp {peak_kurs:,.0f}</div>
                <div class="accent-sub">📅 {peak_kurs_date}</div>
            </div>""", unsafe_allow_html=True)

    else:
        # Placeholder metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""<div class="metric-card"><div class="metric-label">Inflasi YoY Terkini</div>
            <div class="metric-value" style="color:#ef4444;">–</div><div class="metric-sub">Unggah dataset</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div class="metric-card"><div class="metric-label">Nilai Tukar USD/IDR</div>
            <div class="metric-value">–</div><div class="metric-sub">Unggah dataset</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div class="metric-card" style="border-left-color:#8b5cf6;"><div class="metric-label">Total Observasi</div>
            <div class="metric-value" style="color:#7c3aed;">–</div><div class="metric-sub">Unggah dataset</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Ringkasan
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Ringkasan Analisis</div><br>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-item">
        <div class="info-icon info-icon-blue">📊</div>
        <div>
            <div class="info-text-title">Dataset Lengkap</div>
            <div class="info-text-sub">Data inflasi YoY dan nilai tukar USD/IDR selama 76 bulan dari Januari 2020 hingga April 2026</div>
        </div>
    </div>
    <div class="info-item">
        <div class="info-icon info-icon-purple">📈</div>
        <div>
            <div class="info-text-title">Visualisasi Data</div>
            <div class="info-text-sub">Grafik tren historis inflasi dan nilai tukar dengan anotasi poin-poin penting</div>
        </div>
    </div>
    <div class="info-item">
        <div class="info-icon info-icon-green">🔮</div>
        <div>
            <div class="info-text-title">Prediksi & Forecasting</div>
            <div class="info-text-sub">Model VECM/VAR dengan uji stasioneritas dan kointegrasi untuk prediksi nilai masa depan</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE: DATASET
# ═══════════════════════════════════════════════
elif page == "📋  Dataset":
    require_data()
    st.markdown('<div class="section-title">Eksplorasi Dataset</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Data inflasi dan nilai tukar Indonesia dimuat secara otomatis dari sistem</div>', unsafe_allow_html=True)

    if st.session_state.df is not None:
        df = st.session_state.df
        inflasi_col = st.session_state.inflasi_col
        kurs_col = st.session_state.kurs_col
        tanggal_col = st.session_state.tanggal_col

        # Build display table
        bulan_map = {1:"Januari",2:"Februari",3:"Maret",4:"April",5:"Mei",6:"Juni",
                     7:"Juli",8:"Agustus",9:"September",10:"Oktober",11:"November",12:"Desember"}
        display_df = pd.DataFrame()
        display_df["NO"] = range(1, len(df) + 1)
        display_df["TANGGAL"] = df[tanggal_col].dt.strftime("%Y-%m-%d")
        display_df["PERIODE"] = df[tanggal_col].dt.strftime("%Y-%m")
        display_df["TAHUN"] = df[tanggal_col].dt.year
        display_df["BULAN"] = df[tanggal_col].dt.month.map(bulan_map)
        display_df["INFLASI YOY (%)"] = df[inflasi_col].map("{:.2f}%".format)
        display_df["NILAI TUKAR USD/IDR (RP)"] = df[kurs_col].map(lambda x: f"Rp {x:,.0f}")

        st.dataframe(display_df, use_container_width=True, hide_index=True, height=420)

        date_min = df[tanggal_col].iloc[0].strftime("%b %Y")
        date_max = df[tanggal_col].iloc[-1].strftime("%b %Y")
        st.markdown(f"<div style='color:#8a99b8; font-size:0.8rem; margin-top:8px;'>📊 {len(df)} observasi · {date_min} – {date_max}</div>", unsafe_allow_html=True)

        # Tombol Download Export
        csv_out = display_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Export CSV", csv_out, file_name="dataset_inflasiid.csv", mime="text/csv")

# ═══════════════════════════════════════════════
# PAGE: GRAFIK
# ═══════════════════════════════════════════════
elif page == "📊  Grafik":
    require_data()

    st.markdown('<div class="section-title">Visualisasi Tren & Analisis Pola Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Grafik pergerakan historis untuk justifikasi uji stasioneritas</div>', unsafe_allow_html=True)

    df = st.session_state.df
    inflasi_col = st.session_state.inflasi_col
    kurs_col = st.session_state.kurs_col
    tanggal_col = st.session_state.tanggal_col

    # --- Grafik 1: Inflasi ---
    peak_idx = df[inflasi_col].idxmax()
    peak_date = df.loc[peak_idx, tanggal_col]
    peak_val = df.loc[peak_idx, inflasi_col]

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df[tanggal_col], y=df[inflasi_col],
        mode="lines",
        name="Data Historis",
        line=dict(color="#e11d48", width=2),
        fill="tozeroy",
        fillcolor="rgba(225,29,72,0.08)",
    ))
    fig1.add_trace(go.Scatter(
        x=[peak_date], y=[peak_val],
        mode="markers+text",
        marker=dict(color="#e11d48", size=10, symbol="circle"),
        text=[f"{peak_val:.2f}% ({peak_date.strftime('%b %Y')})"],
        textposition="top right",
        textfont=dict(size=11, color="#e11d48", family="Plus Jakarta Sans"),
        showlegend=False,
    ))
    fig1.update_layout(
        title=dict(text="Pergerakan Historis Inflasi YoY (%)", font=dict(size=15, family="Plus Jakarta Sans", color="#0f1b2d"), x=0),
        xaxis=dict(showgrid=True, gridcolor="#f0f4fb", title=""),
        yaxis=dict(showgrid=True, gridcolor="#f0f4fb", title="Inflasi (%)"),
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="left", x=0),
        margin=dict(l=0, r=10, t=50, b=40),
        height=320,
        font=dict(family="Plus Jakarta Sans"),
    )
    fig1.add_annotation(text="Periode Januari 2020 – April 2026", xref="paper", yref="paper",
                        x=0, y=1.08, showarrow=False, font=dict(size=11, color="#8a99b8"))

    st.markdown('<div class="card" style="padding: 20px 24px;">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Grafik 2: Nilai Tukar ---
    kurs_peak_idx = df[kurs_col].idxmax()
    kurs_peak_date = df.loc[kurs_peak_idx, tanggal_col]
    kurs_peak_val = df.loc[kurs_peak_idx, kurs_col]

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df[tanggal_col], y=df[kurs_col],
        mode="lines",
        name="Data Historis",
        line=dict(color="#1e3a8a", width=2),
        fill="tozeroy",
        fillcolor="rgba(30,58,138,0.07)",
    ))
    fig2.add_trace(go.Scatter(
        x=[kurs_peak_date], y=[kurs_peak_val],
        mode="markers+text",
        marker=dict(color="#1e3a8a", size=10),
        text=[f"Rp {kurs_peak_val:,.0f} ({kurs_peak_date.strftime('%b %Y')})"],
        textposition="top left",
        textfont=dict(size=11, color="#1e3a8a", family="Plus Jakarta Sans"),
        showlegend=False,
    ))
    fig2.update_layout(
        title=dict(text="Pergerakan Historis Nilai Tukar USD/IDR", font=dict(size=15, family="Plus Jakarta Sans", color="#0f1b2d"), x=0),
        xaxis=dict(showgrid=True, gridcolor="#f0f4fb", title=""),
        yaxis=dict(showgrid=True, gridcolor="#f0f4fb", title="Nilai Tukar (Rp)"),
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="left", x=0),
        margin=dict(l=0, r=10, t=50, b=40),
        height=320,
        font=dict(family="Plus Jakarta Sans"),
    )
    fig2.add_annotation(text="Periode Januari 2020 – April 2026", xref="paper", yref="paper",
                        x=0, y=1.08, showarrow=False, font=dict(size=11, color="#8a99b8"))

    st.markdown('<div class="card" style="padding: 20px 24px;">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="note-box">
        💡 <b>Catatan:</b> Grafik digunakan untuk justifikasi uji stasioneritas data
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE: FORECASTING
# ═══════════════════════════════════════════════
elif page == "🔮  Forecasting":
    require_data()

    st.markdown('<div class="section-title">Forecasting & Prediksi</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Analisis proyeksi menggunakan model VECM/VAR</div>', unsafe_allow_html=True)

    model_data = st.session_state.model_data

    left_col, right_col = st.columns([1, 2.5], gap="large")

    # ── LEFT PANEL ──
    with left_col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Pengaturan Analisis**")
        st.markdown("<br>", unsafe_allow_html=True)

        variabel_options = ["Nilai Tukar USD/IDR", "Inflasi YoY (%)", "Keduanya"]
        variabel = st.selectbox("Variabel", variabel_options, index=0)

        model_choice = st.selectbox("Model", ["VECM", "VAR (Fallback)"], index=0)

        eval_method = st.selectbox("Metode Evaluasi", ["MAPE", "MAE", "RMSE"], index=0)

        horizon = st.number_input("Horizon Prediksi (bulan)", min_value=1, max_value=24, value=6, step=1)

        cutoff_default = "2023-12-31"
        cutoff = st.text_input("Tanggal Cutoff Train", value=cutoff_default,
                               help="Format: YYYY-MM-DD")

        run_btn = st.button("▶  Jalankan Prediksi", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── RIGHT PANEL ──
    with right_col:
        if run_btn:
            with st.spinner("Menjalankan analisis ekonometrika... ⚙️"):
                try:
                    results = run_vecm_forecast(model_data, horizon=int(horizon), cutoff=cutoff)
                    st.session_state.vecm_results = results
                except Exception as e:
                    st.error(f"❌ Error saat menjalankan model: {e}")
                    st.stop()

        if "vecm_results" in st.session_state:
            results = st.session_state.vecm_results

            # ── TEST 1: Stasioneritas ──
            st.markdown("""
            <div class="test-box">
                <span class="test-tag tag-test1">TEST 1</span>
                <strong>Uji Stasioneritas (ADF & KPSS)</strong>
            """, unsafe_allow_html=True)

            t1c1, t1c2, t1c3, t1c4 = st.columns([2, 1.2, 1.2, 1.8])
            t1c1.markdown("<div style='font-size:0.75rem;color:#8a99b8;font-weight:700;'>VARIABEL</div>", unsafe_allow_html=True)
            t1c2.markdown("<div style='font-size:0.75rem;color:#8a99b8;font-weight:700;'>ADF Level p-value</div>", unsafe_allow_html=True)
            t1c3.markdown("<div style='font-size:0.75rem;color:#8a99b8;font-weight:700;'>KPSS Level p-value</div>", unsafe_allow_html=True)
            t1c4.markdown("<div style='font-size:0.75rem;color:#8a99b8;font-weight:700;'>KESIMPULAN</div>", unsafe_allow_html=True)

            st.markdown("<hr style='margin:8px 0;border-color:#f0f4fb;'>", unsafe_allow_html=True)
            for row in results["stat_results"]:
                badge_cls = "badge-green" if row["Status"] == "green" else "badge-red"
                c1, c2, c3, c4 = st.columns([2, 1.2, 1.2, 1.8])
                c1.markdown(f"<div style='font-size:0.82rem;font-weight:600;color:#0f1b2d;padding:4px 0;'>{row['Variabel']}</div>", unsafe_allow_html=True)
                c2.markdown(f"<div style='font-size:0.82rem;text-align:center;'>{row['ADF Level p-value']}</div>", unsafe_allow_html=True)
                c3.markdown(f"<div style='font-size:0.82rem;text-align:center;'>{row['KPSS Level p-value']}</div>", unsafe_allow_html=True)
                c4.markdown(f"<span class='{badge_cls}' style='font-size:0.72rem;'>{row['Kesimpulan']}</span>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            # ── TEST 2: Kointegrasi ──
            st.markdown("""
            <div class="test-box">
                <span class="test-tag tag-test2">TEST 2</span>
                <strong>Uji Kointegrasi Johansen</strong>
            """, unsafe_allow_html=True)

            k1, k2, k3 = st.columns(3)
            k1.metric("Rank Kointegrasi (r)", results["coint_rank"])
            k2.metric("Det Order", results["det_order"])
            conclusion_text = "Terdapat hubungan jangka panjang" if results["coint_rank"] >= 1 else "Tidak ada hubungan jangka panjang"
            badge_c = "badge-green" if results["coint_rank"] >= 1 else "badge-red"
            k3.markdown(f"<div style='margin-top:8px;'><span class='{badge_c}'>{conclusion_text}</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # ── EVALUATION ──
            st.markdown("""
            <div class="test-box">
                <span class="test-tag tag-eval">EVALUATION</span>
                <strong>Evaluasi Akurasi Model (Out-of-Sample)</strong>
            """, unsafe_allow_html=True)

            e1, e2, e3, e4 = st.columns([2, 1, 1, 1])
            e1.markdown("<div style='font-size:0.75rem;color:#8a99b8;font-weight:700;'>VARIABEL</div>", unsafe_allow_html=True)
            e2.markdown("<div style='font-size:0.75rem;color:#8a99b8;font-weight:700;text-align:center;'>MAE</div>", unsafe_allow_html=True)
            e3.markdown("<div style='font-size:0.75rem;color:#8a99b8;font-weight:700;text-align:center;'>RMSE</div>", unsafe_allow_html=True)
            e4.markdown("<div style='font-size:0.75rem;color:#8a99b8;font-weight:700;text-align:center;'>MAPE (%)</div>", unsafe_allow_html=True)
            st.markdown("<hr style='margin:8px 0;border-color:#f0f4fb;'>", unsafe_allow_html=True)

            for m in results["metrics"]:
                m1, m2, m3, m4 = st.columns([2, 1, 1, 1])
                m1.markdown(f"<div style='font-size:0.82rem;font-weight:600;color:#0f1b2d;padding:4px 0;'>{m['Variabel']}</div>", unsafe_allow_html=True)
                m2.markdown(f"<div style='text-align:center;font-size:0.82rem;'>{m['MAE']}</div>", unsafe_allow_html=True)
                m3.markdown(f"<div style='text-align:center;font-size:0.82rem;'>{m['RMSE']}</div>", unsafe_allow_html=True)
                mape_val = m['MAPE (%)']
                mape_color = "#16a34a" if isinstance(mape_val, float) and mape_val < 15 else "#dc2626"
                m4.markdown(f"<div style='text-align:center;font-size:0.82rem;font-weight:700;color:{mape_color};'>{mape_val}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # ── FORECAST CHART ──
            future_df = results["future_df"]
            ci_df = results["ci_df"]
            data_model_full = results["data_model"]

            # Determine which variables to plot
            if variabel == "Nilai Tukar USD/IDR":
                plot_cols = [("nilai tukar usd idr", "Nilai Tukar USD/IDR", "#1e3a8a", "ci_kurs")]
            elif variabel == "Inflasi YoY (%)":
                plot_cols = [("inflasi yoy %", "Inflasi YoY (%)", "#e11d48", "ci_inflasi")]
            else:
                plot_cols = [
                    ("nilai tukar usd idr", "Nilai Tukar USD/IDR", "#1e3a8a", "ci_kurs"),
                    ("inflasi yoy %", "Inflasi YoY (%)", "#e11d48", "ci_inflasi"),
                ]

            for col_name, col_label, col_color, ci_col in plot_cols:
                hist_tail = data_model_full[col_name].iloc[-18:]

                fig = go.Figure()
                # Historical
                fig.add_trace(go.Scatter(
                    x=hist_tail.index, y=hist_tail.values,
                    mode="lines", name="Historis 18 bulan",
                    line=dict(color=col_color, width=2),
                ))
                # Confidence band
                upper = future_df[col_name] + ci_df[ci_col]
                lower = future_df[col_name] - ci_df[ci_col]
                fig.add_trace(go.Scatter(
                    x=list(future_df.index) + list(future_df.index[::-1]),
                    y=list(upper) + list(lower[::-1]),
                    fill="toself",
                    fillcolor="rgba(99,102,241,0.12)",
                    line=dict(color="rgba(0,0,0,0)"),
                    showlegend=True,
                    name="Confidence Interval",
                ))
                # Forecast line
                fig.add_trace(go.Scatter(
                    x=future_df.index, y=future_df[col_name],
                    mode="lines+markers", name="Proyeksi VECM",
                    line=dict(color="#6366f1", width=2.5, dash="dot"),
                    marker=dict(size=6),
                ))
                last_hist = pd.DataFrame({"x": [hist_tail.index[-1]], "y": [hist_tail.values[-1]]})
                fig.add_trace(go.Scatter(
                    x=last_hist["x"], y=last_hist["y"],
                    mode="markers", marker=dict(color=col_color, size=8), showlegend=False,
                ))

                period_label = f"{future_df.index[0].strftime('%b %Y')} – {future_df.index[-1].strftime('%b %Y')}"
                fig.update_layout(
                    title=dict(text=f"Proyeksi {col_label} ({period_label})", font=dict(size=14, family="Plus Jakarta Sans", color="#0f1b2d"), x=0),
                    xaxis=dict(showgrid=True, gridcolor="#f0f4fb"),
                    yaxis=dict(showgrid=True, gridcolor="#f0f4fb"),
                    plot_bgcolor="white", paper_bgcolor="white",
                    legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="left", x=0),
                    margin=dict(l=0, r=10, t=50, b=40),
                    height=320,
                    font=dict(family="Plus Jakarta Sans"),
                )

                st.markdown('<div class="test-box"><span class="test-tag tag-forecast">FORECAST</span>', unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style="background:white; border-radius:16px; padding:48px; text-align:center; color:#8a99b8; box-shadow:0 2px 10px rgba(15,27,45,0.07);">
                <div style="font-size:2.5rem; margin-bottom:12px;">🔮</div>
                <div style="font-weight:700; font-size:1rem; color:#4a6080; margin-bottom:6px;">Siap Menjalankan Analisis</div>
                <div style="font-size:0.85rem;">Atur parameter di panel kiri, lalu klik <strong>"Jalankan Prediksi"</strong></div>
            </div>
            """, unsafe_allow_html=True)
