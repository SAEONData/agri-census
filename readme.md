# 2017 Agriculture Census Dashboard

<span style="color: grey; font-size: smaller;">A South African Risk and Vulnerability Product</span>

## 🌍 Overview

The 2017 Agriculture Census Dashboard is an open-source spatial data product developed for South Africa’s Risk and Vulnerability Atlas (SARVA). It visualizes key agricultural statistics derived from the **Census of Commercial Agriculture 2017**, produced by **Statistics South Africa**. The dashboard provides interactive analytical views for understanding trends across provinces and municipalities.

## 🔎 Views in the Dashboard

- **Home** — Introduction and context of the dashboard
- **Summary** — Aggregated census statistics across spatial regions
- **Indicator Explorer** — Drill-down by indicator, sub-indicator, and sub-sub-indicator
- **Map View** — Spatial visualisation of agriculture-related variables
- **Downloads** — Export filtered datasets for offline use

## 🚀 Getting Started

The recommended way to run the app is through **Dev Containers in VSCode**. However, Docker and manual setups are also supported.

### ✅ Run the App via Dev Container (Recommended for VSCode)

1. Open the project in VSCode
2. Reopen in container (using `.devcontainer/devcontainer.json`)
3. The app will auto-start and be available at `localhost:8501`

### 🐳 Run with Docker Compose (Alternative)

```bash
git clone https://github.com/SAEONData/agri-census.git
cd agri-census
docker-compose up --build
```

Visit [http://localhost:8501](http://localhost:8501) in your browser.

### ⚙️ Manual Setup (Non-Container Users)

1. Create a Python virtual environment
2. Install dependencies from `requirements.txt`
3. Run the app:

```bash
streamlit run app.py
```

## 📁 Repository

GitHub: [SAEONData/agri-census](https://github.com/SAEONData/agri-census)

## 🙏 Acknowledgements

- **Statistics South Africa** for the original 2017 CoCA dataset  
- **SAEON** (South African Environmental Observation Network) for the spatial data pipeline and hosting  
- **Bonolo Mokoatsi & Amelia Hilgart** for original data wrangling and SDG integration  
- Inspired by the national goals of improved agricultural monitoring and SDG alignment

---

> For more information, see the official [CoCA 2017 Fact Sheet (PDF)](http://www.statssa.gov.za/publications/Report-11-02-01/Report-11-02-012017.pdf)
