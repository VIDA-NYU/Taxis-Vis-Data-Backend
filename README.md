<div align="center">
  <img src="./public/repo_icon.png" alt="Taxis Vis Icon" width="150"/>
  <h1><strong>Taxis Vis</strong></h1>
  <h4>Data Analysis Backend 📊</h4>

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![UV](https://img.shields.io/badge/UV-00B1D2?style=for-the-badge&logo=uv&logoColor=white)
![Version](https://img.shields.io/badge/Version-0.1.0_alpha-red?style=for-the-badge)
</div>

______

<div align="center">

_Greetings_ from the **Taxis Vis Data Analysis Backend**! This project is a component of the larger Taxis Vis
initiative, which
draws inspiration from the paper [*Visual Exploration of Big Spatio-Temporal Urban Data: A Study of New York City Taxi
Trips*](https://ieeexplore.ieee.org/abstract/document/6634127/).
We aim to _revive_ the paper using _modern_ open-source tools.

</div>

---

## 🚀 **Overview**

The **Data Analysis Backend** is built with **Django** and managed by **UV** (Astral's _very-fast_ environment
tool).  
It can generate histograms, scatter plots, box plots, pie charts, and other visualisations from filtered taxi trip
data.  
This backend ensures a **future-proof design**, allowing for the integration of machine learning models to improve
insights and handle diverse datasets through configurable mappings.

---

## 📦 **Installation**

### **Pre-requisites**

1. **Install UV:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   *Note: Explore more about UV [here](https://docs.astral.sh/uv/getting-started/installation/#installing-uv).*

2. **Install Python and pip:**

   Ensure Python (>=3.8) and pip are installed on your system. You can download Python from
   the [official website](https://www.python.org/downloads/) or use a package manager like `apt`, `brew`, or `choco`
   based on your OS.

---

### ⚙️ **Setup**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/VIDA-NYU/Taxis-Vis-Data-Backend.git
   cd Taxis-Vis-Data-Backend
   ```

2. **Prepare the Environment:**

   Lock and synchronize dependencies using **UV**:
   ```bash
   uv lock
   uv sync
   ```

   *Note: UV manages the environment dynamically, eliminating the need for explicit virtual environment activation.*

3. **Start the Backend Server:**
   ```bash
   uv run python manage.py runserver
   ```

   The server should now be running locally, typically accessible at `http://127.0.0.1:8000/`.

---

## 🌍 **Technology Stack**

| **Feature**                | **Details**                                                                                                                                                                                                                                     |
|----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Framework**              | Django REST API for backend functionality.                                                                                                                                                                                                      |
| **Data Analysis**          | Pandas for flexible and efficient data handling [![GitHub Repo stars](https://img.shields.io/github/stars/pandas-dev/pandas?style=social)](https://github.com/pandas-dev/pandas)                                                                |
| **Numerical Processing**   | NumPy for foundational numerical computations [![GitHub Repo stars](https://img.shields.io/github/stars/numpy/numpy?style=social)](https://github.com/numpy/numpy)                                                                              |
| **Geospatial Processing**  | Shapely for geometric operations [![GitHub Repo stars](https://img.shields.io/github/stars/shapely/shapely?style=social)](https://github.com/shapely/shapely)                                                                                   |
| **Visualisation**          | Custom Plotly-based functions for generating interactive charts [![Plotly](https://img.shields.io/badge/Plotly-3776AB?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)                                                    |
| **API Handling**           | Django REST Framework for building robust APIs [![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-000000?style=for-the-badge&logo=django-rest-framework&logoColor=white)](https://www.django-rest-framework.org/) |
| **Environment Management** | UV by Astral for environment management [![UV](https://img.shields.io/badge/UV-00B1D2?style=for-the-badge&logo=uv&logoColor=white)](https://docs.astral.sh/uv/)                                                                                 |

---

## 🎛️ **Configuration for Multiple Datasets**

One of the key strengths of the **Taxis Vis Data Analysis Backend** is its ability to handle multiple datasets through
configurable JSON files. By modifying or adding new configuration files, you can seamlessly integrate different taxi
trip datasets without altering the core backend logic.

### **a. Configuration Files Structure**

Each dataset you wish to analyse should have its own JSON configuration file stored in the `config/` directory. These
configuration files define how the backend maps and processes the dataset's columns.

**Example Configuration (`nyc_taxis_2015_dataset.json`):**

```json
{
   // Basically, key is generally the logical name and value is the column name in the dataset
   "datetime_columns": {
      "pickup": "tpep_pickup_datetime",
      "dropoff": "tpep_dropoff_datetime"
   },
   "location_columns": {
      "pickup": "pickup_coordinates",
      "dropoff": "dropoff_coordinates"
   },
   "required_columns": {
      "trip_distance": "trip_distance",
      "fare_amount": "fare",
      "passenger_count": "passenger_count",
      "payment_type": "payment_type",
      "tip_amount": "tip_amount"
   }
}
```

**Key Sections:**

- **`datetime_columns`:** Maps logical datetime fields to the dataset's column names.
- **`location_columns`:** Maps logical location fields (pickup/dropoff) to the dataset's JSON columns containing
  coordinates.
- **`required_columns`:** Specifies essential columns for analysis, mapping logical names to dataset column names.

### **b. Adding a New Dataset Configuration**

To integrate a new dataset, follow these steps:

1. **Create a New Configuration File:**

   - Navigate to the `config/` directory.
   - Create a new JSON file, e.g., `city_taxis_2020_dataset.json`.

2. **Define the Configuration:**

   Populate the JSON file with the appropriate mappings based on the new dataset's structure.

   **Example (`city_taxis_2020_dataset.json`):**

   ```json
   {
     "datetime_columns": {
       "pickup": "pickup_datetime",
       "dropoff": "dropoff_datetime"
     },
     "location_columns": {
       "pickup": "pickup_location",
       "dropoff": "dropoff_location"
     },
     "required_columns": {
       "trip_distance": "distance_miles",
       "fare_amount": "fare",
       "passenger_count": "passengers",
       "payment_type": "payment_method",
       "tip_amount": "tip"
     }
   }
   ```

3. **Save and Validate:**

   Ensure the JSON is valid. Use tools like [JSONLint](https://jsonlint.com/) for validation.

### **c. Using a Specific Configuration in API Requests**

When making API requests to perform analyses, specify the desired configuration by including the `config_name`parameter.
If not specified, the backend defaults to `nyc_taxis_2015_dataset`.

**Example API Request Payload:**

```bash
POST /visualisation/trip-duration-histogram/
Content-Type: multipart/form-data

file: <your_csv_file>
config_name: city_taxis_2020_dataset
```

**Parameters:**

- **`file` (required):** The CSV file containing taxi trip data.
- **`config_name` (optional):** The name of the configuration file (without `.json` extension). Defaults to
  `nyc_taxis_2015_dataset` if not provided.

–––––

## 📖 **Usage**

The backend exposes several API endpoints to perform various analyses on the taxi trip data. Each endpoint expects a CSV
file and optionally a `config_name` to specify the dataset configuration.

### **Available API Endpoints**

1. **Trip Duration Histogram**
   - **URL:** `/visualisation/trip-duration-histogram/`
   - **Method:** `POST`
   - **Description:** Generates a histogram showing the distribution of trip durations in minutes.

2. **Peak Hours Bar Chart**
   - **URL:** `/visualisation/peak-hours-bar/`
   - **Method:** `POST`
   - **Description:** Generates a bar chart displaying the number of trips per pickup hour, highlighting peak hours
     based on a threshold.

3. **Fare Distribution Box Plot**
   - **URL:** `/visualisation/fare-distribution-box/`
   - **Method:** `POST`
   - **Description:** Generates a box plot illustrating the distribution of fare amounts.

4. **Passenger Count Pie Chart**
   - **URL:** `/visualisation/passenger-count-pie/`
   - **Method:** `POST`
   - **Description:** Generates a pie chart showing the distribution of passenger counts.

5. **Payment Type Pie Chart**
   - **URL:** `/visualisation/payment-type-pie/`
   - **Method:** `POST`
   - **Description:** Generates a pie chart depicting the distribution of payment types.

6. **Tip Amount Box Plot**
   - **URL:** `/visualisation/tip-amount-box/`
   - **Method:** `POST`
   - **Description:** Generates a box plot for tip amounts.

7. **Distance vs. Fare Scatter Plot**
   - **URL:** `/visualisation/distance-fare-scatter-plot/`
   - **Method:** `POST`
   - **Description:** Generates a scatter plot to analyse the relationship between trip distance and fare amount.

8. **Time Series Line Chart**
   - **URL:** `/visualisation/time-series-line/`
   - **Method:** `POST`
   - **Description:** Generates a line chart showing the number of trips over time (daily).

### **Making API Requests**

Use tools like **cURL**, **Postman**, or frontend interfaces to make `POST` requests to the desired endpoints.

**Example Using cURL:**

```bash
curl -X POST http://127.0.0.1:8000/visualisation/trip-duration-histogram/ \
  -F 'file=@/path/to/your/taxi_trips.csv' \
  -F 'config_name=city_taxis_2020_dataset'
```

**Response:**

```json
{
   "chart": {
      "data": [
         {
            "x": [
               /* list of trip durations */
            ],
            "type": "histogram",
            "name": "Trip Durations",
            "nbinsx": 50,
            "marker": {
               "color": "rgba(100, 149, 237, 0.7)"
            }
         }
      ],
      "layout": {
         "title": "Distribution of Trip Durations (Minutes)",
         "xaxis": {
            "title": "Trip Duration (Minutes)"
         },
         "yaxis": {
            "title": "Frequency"
         }
      }
   }
}
```

_Or simply run the backend runserver script!_

---

## Limitations 🚧

| **Limitation**           | **Details**                                                                                                                                        |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| **Platform Testing**     | Tested on 🍎 **macOS Sequoia** on an Apple Silicon-based machine. Compatibility on other platforms like Linux is anticipated; Windows is untested. |
| **Real-Time Processing** | Currently optimised for batch processing of CSV files. Real-time data streams require further development.                                         |

---

## 📖 **Further Reading**

For detailed context and broader system architecture, refer to:  
➡️ [Frontend README](https://github.com/VIDA-NYU/Taxis-Vis-Frontend)

Explore the inspiring paper:  
➡️ [Visual Exploration of Big Spatio-Temporal Urban Data: A Study of New York City Taxi Trips](https://ieeexplore.ieee.org/abstract/document/6634127/)

---

**Happy Exploring! 🚖**