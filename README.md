<div align="center">
  <img src="./public/repo_icon.png" alt="Taxis Vis Icon" width="150"/>
  <h1><strong>Taxis Vis</strong></h1>
  <h4>Data Analysis Backend (Django + Pandas) 📊</h4>

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Version](https://img.shields.io/badge/Version-0.2.0_alpha-red?style=for-the-badge)
</div>

---

## 🚀 **Overview**

The **Data Analysis Backend** is a **Django** + **Pandas** service that receives **CSV** data from
the [Taxis Vis Frontend](https://github.com/VIDA-NYU/Taxis-Vis-Frontend). Once the frontend (or the Node geospatial
backend) has filtered taxi trips, that subset is uploaded here for further analytics—**histograms, box plots, scatter
plots, pie charts**, and more. We transform your CSV into **Plotly-friendly JSON** for easy rendering on the frontend.

> ![NOTE]
> The heavy-lifting for geospatial queries (e.g., polygon/line-based filters) is done in the **GeoSpatial Node.js +
DuckDB** backend. This Django service strictly focuses on data analysis once the relevant CSV subset is sent over.

> ![NOTE]
> The following features are in **alpha** stage. Therefore, these are not covering **all* the features mentioned in the
> paper. However, the infrastructure allows for replicating them all mentioned in the paper.
---

## 🎛️ **Configuration & Required Columns**

Unlike the geospatial backend, you usually don’t need to configure custom JSON files here. Instead:

1. **`data_analysis_backend_required_columns`**  
   The Node backend defines certain columns that your CSV must include so that these analysis endpoints can function.
   These columns (e.g., `"trip_distance"`, `"fare_amount"`, etc.) must appear in the CSV you send to Django.

2. **CSV Format**  
   When the frontend or Node backend posts data to these endpoints, they include a file (CSV) in the form-data. We
   expect the columns named the same way the Node backend promised (based on `filtered_trips_output_columns` in
   `dataset.json`).

**If these required columns are missing**, the respective endpoint will reject the request or report an error indicating
which columns are not found.

---

## 📦 **Installation**

### **Pre-requisites**

- **Python** (>=3.8) and **pip**.
- *(Highly recommended)* **UV** for environment management without having to deal with the fuss of creating an env
  yourself!

### **Steps to Set Up**

1. **Clone** this repository:
   ```bash
   git clone https://github.com/VIDA-NYU/Taxis-Vis-Data-Backend.git
   cd Taxis-Vis-Data-Backend
   ```
2. **Install** dependencies using **pip** or **UV**:
   ```bash
   uv lock
   uv sync
   ```

3. **Run** the Django server:
   ```bash
   # With UV:
   uv run python manage.py runserver # without the need to activate the environment yourself. UV does it for you!

   # Or directly:
   python manage.py runserver # assuming you have the environment activated
   ```
   By default, it listens on **http://127.0.0.1:8000**.

---

## 🌐 **Endpoints in a Nutshell**

Each endpoint expects a **multipart/form-data** POST containing:

- **`file`**: The CSV of filtered trips.
- *(Optionally)* any other parameters your analyses might need (e.g., thresholds).

Common endpoints:

1. **`/api/visualisation/trip-duration-histogram/`**  
   Generates a histogram of trip durations (in minutes).

2. **`/api/visualisation/fare-distribution-box/`**  
   Box plot distribution of fare amounts.

3. **`/api/visualisation/distance-fare-scatter-plot/`**  
   Scatter plot analyzing the relationship between trip distance and fare amount.

4. **`/api/visualisation/time-series-line/`**  
   Line chart tracking how many trips happened across different days (or time units).

... and several others, all focused on exploring numeric columns from the CSV.

---

## 💡 **Data Flow**: How the CSV Arrives Here

1. A user on the **Taxis Vis Frontend** draws polygons or sets time filters → This triggers a request to the **Node
   Geospatial Backend**.
2. The Node backend returns a list of trips that match those geospatial/time conditions.
3. The user then chooses an analysis type (e.g., “Trip Duration Histogram”) on the frontend.
4. The frontend creates a CSV out of the filtered trips and posts it to **this Django** backend (e.g.,
   `/visualisation/trip-duration-histogram/`).
5. **Django** reads that CSV into a Pandas DataFrame, performs the analysis, and returns **Plotly** chart data (in JSON)
   to the frontend.

---

## **When Adding a New Dataset**

There’s typically **no** need to modify this Django project if:

- You keep the required columns from `dataset.json` in your Node backend.
- The CSV posted to this Django backend includes those columns.

As long as the new dataset respects the Node backend’s `data_analysis_backend_required_columns` and the final CSV for
analysis has those columns, Django can produce the charts with no extra configuration.

---

## Design Philosophy 💡

We focus on **simplicity and performance**:

- **Django** for the REST API endpoints and easy request handling.
- **Pandas** for the tabular transformations—straightforward to manipulate CSV data in-memory. Future version could even
  think passing this into an ML-e.g.-Scikit Pipeline for ML-based analysis of taxis-trips data.
- Minimal, well-defined endpoints that produce Plotly-friendly JSON, so the frontend can easily embed dynamic charts.

Since the time-intensive or complex geospatial tasks happen in the Node.js + DuckDB backend, we keep the **data analysis
** layer lightweight but still robust enough to handle typical data-exploration tasks (histograms, box plots, etc.).

---

## Limitations 🚧

| **Limitation**            | **Details**                                                                                                                                    |
|---------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| **Memory Usage**          | Large CSV uploads (tens/hundreds of MB) can consume significant memory in Python. For extremely large data, you may want chunked or streaming. |
| **Real-time Analytics**   | Currently processes data in a “batch” fashion (file upload). No real-time streaming integration is provided.                                   |
| **Must Maintain Columns** | The Node backend’s `data_analysis_backend_required_columns` must exist in your CSV. If you rename or remove them, analyses here will break.    |
| **Python Dependencies**   | This project relies on fairly standard packages. But ensure your environment is correct if you face import errors.                             |

---

## 📖 **Further Reading**

- [Frontend (React) README](https://github.com/VIDA-NYU/Taxis-Vis-Frontend) – The user-facing side that triggers these
  analysis requests.
- [GeoSpatial (Node.js + DuckDB) Backend README](https://github.com/VIDA-NYU/Taxis-Vis-Geospatial-Backend) – Where the
  filtering & queries happen.
- [Original Taxis Vis Paper (IEEE)](https://ieeexplore.ieee.org/abstract/document/6634127/) – The 2013 research concept
  behind it all.

---

**Happy Analysing!**  
_The Taxis Vis Team_  