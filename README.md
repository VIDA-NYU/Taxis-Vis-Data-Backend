<div align="center">
  <img src="./public/repo_icon.png" alt="Taxis Vis Icon" width="150"/>
  <h1><strong>Taxis Vis</strong></h1>
  <h4>📊 Data Analysis Backend (Django + Pandas)</h4>

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Version](https://img.shields.io/badge/Version-0.2.0_alpha-red?style=for-the-badge)
</div>

---

## 🚀 **Overview**

The **Data Analysis Backend** is a **Django + Pandas** service that performs **analytics** on taxi trip data.  
Once the **Taxis Vis Frontend** filters taxi trips, it sends a subset of trips here for **statistical** and **graphical
** analysis,  
including **histograms, box plots, scatter plots, and time-series visualizations**, _to name a few_.

> [!NOTE]
> The **Geospatial backend is no longer needed** since **DuckDB-WASM** handles spatial queries directly in the
> frontend.  
> This backend is **strictly** for **data analysis & visualization**—not spatial filtering.

---

## 📦 **Installation & Setup**

### **🔧 Prerequisites**

- **Python** (>=3.8)
- **Django** (installed via `uv` or `pip`)
- *(Recommended)* **UV** for seamless virtual environment management
- **Pandas** (for handling data operations)

### **🛠️ Steps to Set Up**

1️⃣ **Clone this repository**:

```bash
git clone https://github.com/VIDA-NYU/Taxis-Vis-Data-Backend.git
cd Taxis-Vis-Data-Backend
```

2️⃣ **Install dependencies** using **UV**:

```bash
uv lock
uv sync
```

3️⃣ **Run the Django server**:

```bash
# With UV (recommended)
uv run python manage.py runserver

# Or manually if using pip/venv (though make sure to be in the correct environment)
python manage.py runserver
```

💡 By default, the backend runs on **http://127.0.0.1:8000**.

---

## 📊 **How It Works: Data Flow**

1️⃣ **User applies filters in the Frontend (Taxis Vis UI).**  
2️⃣ **Frontend sends a filtered subset of trips (CSV) to this Django backend.**  
3️⃣ **Django processes the CSV using Pandas** and generates **Plotly-compatible JSON** for visualization.  
4️⃣ **Frontend receives the JSON** and renders the requested charts dynamically.

---

## 🌐 **Available API Endpoints**

Each endpoint expects a **multipart/form-data** `POST` request containing:

- **`file`** → The CSV file with filtered taxi trip data.
- *(Optional parameters)* like thresholds, bin sizes, etc.

| **Endpoint**                                      | **Function**                              |
|---------------------------------------------------|-------------------------------------------|
| **`/api/visualisation/trip-duration-histogram/`** | Generates a histogram of trip durations.  |
| **`/api/visualisation/fare-distribution-box/`**   | Box plot distribution of fare amounts.    |
| **`/api/visualisation/distance-fare-scatter/`**   | Scatter plot of distance vs fare.         |
| **`/api/visualisation/time-series-line/`**        | Line chart showing trip volume over time. |

💡 Each response returns **Plotly JSON**, allowing easy embedding in the **Taxis Vis** UI.

---

## 📖 **Further Reading & Resources**

- **[Frontend (React) README](https://github.com/VIDA-NYU/Taxis-Vis-Frontend)** → The user-facing interface that
  triggers these analysis requests.
- **[Original Taxis Vis Paper (IEEE)](https://ieeexplore.ieee.org/abstract/document/6634127/)** → Research behind the
  system.

---

**Happy Analysing!**  
_The Taxis Vis Team_ 🚀