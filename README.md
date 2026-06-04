# 📊 InflasiID - Aplikasi Analisis Runtun Waktu Ekonometrika Multivariat

Aplikasi web interaktif untuk analisis **Inflasi YoY (%)** dan **Nilai Tukar USD/IDR** Indonesia menggunakan model ekonometrika **VECM (Vector Error Correction Model)** dengan Streamlit.



---

## ✨ Fitur Utama

### 🏠 **Halaman Beranda (Home Dashboard)**
- **KPI Cards**: Menampilkan metrik terkini:
  - Inflasi YoY Terkini
  - Nilai Tukar USD/IDR Terkini
  - Total Observasi Data
  - Puncak Inflasi (Peak Point)
  - Kurs Tertinggi
- Dashboard interaktif dengan desain modern sesuai Figma

### 📊 **Halaman Dataset**
- **File Uploader**: Upload dataset CSV atau Excel
- **Data Preprocessing**: Otomatis membersihkan dan memformat data
- **Tabel Interaktif**: Tampilan paginasi dengan 10 baris per halaman
- **Download Option**: Export data ke CSV
- Kolom yang ditampilkan:
  - NO | TANGGAL | PERIODE | TAHUN | BULAN | INFLASI YOY (%) | NILAI TUKAR USD/IDR (RP)

### 📈 **Halaman Grafik (Visualization)**
- **Chart 1**: Pergerakan Historis Inflasi YoY (%)
  - Garis merah dengan area fill
  - Anotasi peak point (5.95% Sep 2022)
- **Chart 2**: Pergerakan Historis Nilai Tukar USD/IDR
  - Garis biru gelap dengan area fill
  - Anotasi peak point (Rp 17.134 Apr 2026)
- Interactive hover dan zoom capability

### 🔮 **Halaman Forecasting & Prediksi**
Implementasi lengkap dari notebook dengan UI yang intuitif:

#### Panel Kiri - Input Configuration:
- Pilih Variabel (Nilai Tukar USD/IDR / Inflasi YoY %)
- Pilih Model (VECM)
- Metode Evaluasi (MAPE)
- Horizon Prediksi (1-12 bulan, default 6)
- Tombol "Jalankan Prediksi" dengan progress spinner

#### Panel Kanan - Analisis Results:
1. **TEST 1: Uji Stasioneritas (ADF & KPSS)**
   - Tabel p-value ADF Level & KPSS Level
   - Kesimpulan stasioneritas per variabel
   - Indikasi I(1) atau I(0)

2. **TEST 2: Uji Kointegrasi Johansen**
   - Tabel evaluasi deterministic terms (-1, 0, 1)
   - Rank Kointegrasi (r)
   - Status hubungan jangka panjang

3. **Evaluasi Akurasi Model (Out-of-Sample)**
   - Metrik: MAE, RMSE, MAPE
   - Data train: Jan 2020 - Des 2023
   - Data test: Jan 2024 - Apr 2026

4. **Proyeksi Masa Depan (Interactive Chart)**
   - Visualisasi dengan Plotly
   - Confidence Interval (±5%)
   - Tabel nilai proyeksi per bulan

---

## 🔧 Spesifikasi Teknis

### Framework & Library
- **Streamlit**: Framework web app Python
- **Pandas & NumPy**: Data processing
- **Plotly**: Interactive visualization
- **Statsmodels**: Ekonometrika (ADF, KPSS, Johansen, VECM)
- **Scikit-learn**: Metrics evaluasi (MAE, RMSE, MAPE)

### Dataset
- **Periode**: Januari 2020 - April 2026 (76 observasi bulanan)
- **Variabel**:
  - `inflasi_yoy_persen`: Tingkat inflasi year-on-year (%)
  - `nilai_tukar_usd_idr`: Nilai tukar USD/IDR (Rp)
- **Format**: CSV atau Excel

### Model Ekonometrika
- **VECM (Vector Error Correction Model)**
  - Untuk data I(1) dengan kointegrasi
  - Tangkap hubungan jangka panjang (cointegrating relations)
  - Dinamika jangka pendek (adjustment speed)
  
- **Uji Stasioneritas**: ADF (Augmented Dickey-Fuller) & KPSS
- **Uji Kointegrasi**: Johansen Cointegration Test
- **Forecast Evaluation**: MAE, RMSE, MAPE

---

## 📦 Instalasi & Setup

### Prasyarat
- **Python 3.8+** (direkomendasikan 3.10+)
- **pip** atau **conda**
- **Virtual Environment** (opsional tapi disarankan)

### Step 1: Clone/Download Files
```bash
# Jika menggunakan git
git clone <repository_url>
cd inflasi-id

# Atau copy files: app.py, requirements.txt
```

### Step 2: Buat Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

Atau install individual:
```bash
pip install streamlit pandas numpy plotly statsmodels scikit-learn scipy
```

### Step 4: Prepare Dataset
- Pastikan file CSV/Excel ada di directory yang sama, atau
- Dataset akan auto-load dari directory default

---

## 🚀 Cara Menjalankan

### Run Local
```bash
streamlit run app.py
```

Aplikasi akan membuka di browser secara otomatis di `http://localhost:8501`

### Run di Streamlit Cloud (Deploy)
1. Push files ke GitHub
2. Go to https://streamlit.io/cloud
3. Deploy aplikasi dari GitHub repository
4. Share link ke users

### Command Line Options
```bash
# Run dengan custom port
streamlit run app.py --server.port 8000

# Run tanpa browser opening
streamlit run app.py --logger.level=debug

# Run dengan theme
streamlit run app.py --theme.base="light"
```

---

## 📖 Panduan Penggunaan

### Scenario 1: Analisis Dataset Default
1. **Klik "🏠 Beranda"** → Lihat dashboard dengan metrik terkini
2. **Klik "📊 Dataset"** → Dataset default sudah ter-load
3. **Klik "📈 Grafik"** → Lihat visualisasi tren inflasi dan kurs
4. **Klik "🔮 Forecasting"** → Jalankan prediksi VECM

### Scenario 2: Upload Dataset Custom
1. **Klik "📊 Dataset"** → Upload file CSV atau Excel
   - Format harus memiliki kolom: tanggal, inflasi, kurs
   - Pastikan data ter-cleanup (tidak ada missing values)
2. **Klik "📈 Grafik"** → Grafik otomatis update dengan data baru
3. **Klik "🔮 Forecasting"** → Analisis dengan model VECM

### Scenario 3: Menjalankan Forecast
1. **Klik "🔮 Forecasting"**
2. **Panel Kiri**:
   - Pilih variabel yang ingin diprediksi
   - Pilih model (default: VECM)
   - Atur horizon prediksi (default: 6 bulan)
3. **Klik "▶️ Jalankan Prediksi"**
4. **Tunggu processing** (±10-30 detik tergantung ukuran data)
5. **Lihat hasil** di panel kanan:
   - Test 1: Stasioneritas
   - Test 2: Kointegrasi
   - Evaluasi Akurasi
   - Grafik & Tabel Proyeksi

---

## 📁 Struktur Aplikasi

```
InflasiID/
├── app.py                           # Main Streamlit application
├── requirements.txt                 # Python dependencies
├── README.md                        # Documentation (file ini)
└── data/
    └── dataset_final_inflasi_nilai_tukar_Jan2020_-_Apr2026.csv  # 
```

### Struktur Code dalam app.py

#### 1. **Configuration & Imports**
- Streamlit setup dengan page config
- Import library ekonometrika & visualization
- Custom CSS styling untuk UI

#### 2. **State Management**
- Session state untuk data caching
- Forecast result storage

#### 3. **Utility Functions**

**Data Processing:**
- `load_default_data()`: Load dataset default dengan caching
- `preprocess_data()`: Cleaning & normalization

**Econometric Analysis:**
- `perform_stationarity_tests()`: ADF & KPSS tests
- `perform_cointegration_test()`: Johansen test
- `estimate_vecm()`: VECM model estimation
- `generate_forecast()`: Forecast generation & evaluation

**Visualization:**
- `create_chart_inflasi()`: Inflasi chart dengan Plotly
- `create_chart_kurs()`: Kurs chart dengan Plotly
- `create_forecast_chart()`: Forecast visualization

#### 4. **Navigation & Pages**

**Page 0: Sidebar Navigation**
- Menu selection: Beranda | Dataset | Grafik | Forecasting
- Info box aplikasi

**Page 1: Beranda (Home)**
- Dashboard dengan 5 KPI cards
- 3 info boxes untuk ringkasan

**Page 2: Dataset**
- File uploader (CSV/Excel)
- Data info cards
- Interactive paginated table
- Download button

**Page 3: Grafik**
- 2 interactive Plotly charts
- Peak point annotations
- Grid & hover details

**Page 4: Forecasting**
- 2-column layout (input | result)
- Form controls untuk konfigurasi
- 4-step analysis results:
  - Stationarity tests
  - Cointegration test
  - Accuracy metrics
  - Forecast visualization

#### 5. **Footer**
- Info footer dengan credits

---

## 🔬 Detail Metodologi

### 1. Preprocessing Data
- Rename & lowercase columns
- Detect tanggal, inflasi, kurs columns automatically
- Convert to datetime index
- Handle missing values (dropna)
- Subset untuk 2 variabel utama

### 2. Uji Stasioneritas (ADF & KPSS)
**ADF Test (Augmented Dickey-Fuller)**:
- H0: Data memiliki unit root (non-stasioner)
- H1: Data stasioner
- p-value < 0.05 → Reject H0 → Stasioner

**KPSS Test (Kwiatkowski-Phillips-Schmidt-Shin)**:
- H0: Data stasioner
- H1: Data memiliki unit root
- p-value > 0.05 → Fail to reject H0 → Stasioner

**Kombinasi ADF & KPSS**:
- I(0): ADF p < 0.05 AND KPSS p ≥ 0.05 → Stasioner
- I(1): ADF p ≥ 0.05 AND KPSS p < 0.05 → Integrado first order

### 3. Uji Kointegrasi Johansen
**Concept**: Apakah ada hubungan jangka panjang antar variabel?

**Trace Test**:
- H0: r = 0 (tidak ada kointegrasi)
- Jika reject H0 → Ada minimal 1 hubungan kointegrasi
- Rank (r) = jumlah cointegrating relationships

**Det_order Options**:
- `-1` (nc): No constant → Tidak ada trend
- `0` (ci): Constant in integrating relation
- `1` (cit): Constant & trend

**Output**:
- Rank kointegrasi (r)
- Keterangan: r=0 (no cointegration), r≥1 (cointegration found)

### 4. VECM Estimation
**Model Spesifikasi**:
```
VECM: Δy_t = α β' y_{t-1} + Σ Γ_i Δy_{t-i} + u_t
```

Dimana:
- `α`: Adjustment speed (kecepatan penyesuaian)
- `β'`: Cointegrating vector (hubungan jangka panjang)
- `Γ_i`: Dinamika jangka pendek
- `u_t`: Error term

**Lag Selection**: Menggunakan AIC criterion
**Rank Selection**: Johansen trace test (5% significance)

### 5. Model Validation
**Diagnostic Tests**:
- Whiteness (No autocorrelation): p > 0.05
- Normality (Jarque-Bera): p > 0.05
- Homoscedasticity (ARCH-LM): p > 0.05
- Eigenvalue stability: All roots < 1 in modulus

### 6. Forecast Evaluation
**Metrics**:
- **MAE** (Mean Absolute Error): Rata-rata error absolute
- **RMSE** (Root Mean Squared Error): Penalti untuk large errors
- **MAPE** (Mean Absolute Percentage Error): Percentage error (%)

**Sample**: Out-of-sample dari 2024-2026 untuk evaluasi objektif

---

#
### Test 2: Kointegrasi
```
Det Order | Rank Kointegrasi (r) | Keterangan
-1        | 1                    | Ada 1 hubungan jangka panjang
0         | 1                    | Ada 1 hubungan jangka panjang
1         | 0                    | Tidak ada hubungan jangka panjang
```

### Evaluasi Akurasi
```
Variabel              | MAE   | RMSE  | MAPE
Inflasi YoY (%)       | 0.234 | 0.312 | 8.45%
Nilai Tukar USD/IDR   | 145.57| 198.23| 0.89%
```

---

## 🎯 Rekomendasi Penggunaan

### ✅ Cocok untuk:
- Analisis statistik inflasi & nilai tukar
- Forecast jangka pendek (3-6 bulan)
- Presentasi data ke stakeholder
- Research & academic purposes
- Decision support untuk fiscal/monetary policy

### ⚠️ Keterbatasan:
- Hanya 2 variabel (univariate lebih robust untuk multiple vars)
- Forecast horizon terbatas (max 12 bulan)
- Asumsi linear relationship
- Tidak handle structural breaks

### 📈 Improvement Ideas:
- Add more variables (GDP, interest rate, etc.)
- Implement ARIMAX untuk external variables
- Structural break detection (Bai-Perron)
- IRF & FEVD analysis visualization
- Export report ke PDF/Word
- Real-time data integration (API)

---

## 📚 References

1. **VECM Model**:
   - Johansen, S. (1991). Estimation and Hypothesis Testing of Cointegration Vectors
   - Engle, R. F., & Granger, C. W. (1987). Co-integration and Error Correction

2. **Stationarity Tests**:
   - Dickey, D. A., & Fuller, W. A. (1979). Distribution of the Estimators for Autoregressive Time Series
   - Kwiatkowski, D., et al. (1992). Testing the Null Hypothesis of Stationarity

3. **Software & Libraries**:
   - Streamlit Documentation: https://docs.streamlit.io/
   - Statsmodels Docs: https://www.statsmodels.org/
   - Plotly Docs: https://plotly.com/python/

---


---

## 📄 License

Aplikasi ini dibuat untuk keperluan analisis akademik dan bisnis. Diizinkan untuk digunakan dan dimodifikasi sesuai kebutuhan.

---

## 🙏 Terima Kasih

Terima kasih telah menggunakan **InflasiID**!

Semoga analisis yang dihasilkan dapat memberikan insight berharga untuk pemahaman dinamika ekonomi Indonesia, khususnya dalam aspek inflasi dan nilai tukar mata uang.

**Happy Forecasting! 🚀**

---

**Versi**: 1.0  
**Last Updated**: Juni 2026  
**Author**: Anggota 4 - Coding & Integrasi Sistem
