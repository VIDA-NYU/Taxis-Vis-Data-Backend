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

The **Data Analysis Backend** is created with **Django** and managed by **UV** (Astral's _very-fast_ environment
tool).  
It can generate histograms, scatter plots, and other visualisations from filtered taxi trip data.  
This backend also ensures a **future-proof design**, allowing for the integration of machine learning models to improve
insights.

---

## 📦 **Installation**

### **Pre-requisites**

1. Install **UV**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

Note: Can be further explored here [UV](https://docs.astral.sh/uv/getting-started/installation/#installing-uv).

2. Install **Python** and **pip** on your system.

---

### ⚙️ **Setup**

1. Clone the repository:
   ```bash
   git clone https://github.com/VIDA-NYU/Taxis-Vis-Data-Backend.git
   cd Taxis-Vis-Data-Backend
   ```

2. Prepare the environment:  
   Lock and sync dependencies using **UV**:
   ```bash
   uv lock
   uv sync
   ```

3. Start the backend server:
   ```bash
   uv run python manage.py runserver
   ```

> [!NOTE]
> All environment handling is managed dynamically by **UV**, so you do not need to activate any virtual environment
> explicitly.

---

## 🌍 **Technology Stack**

| **Feature**              | **Details**                                                                                                                                                                      |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Framework**            | Django REST API for backend functionality.                                                                                                                                       |
| **Data Analysis**        | Pandas for flexible and efficient data handling [![GitHub Repo stars](https://img.shields.io/github/stars/pandas-dev/pandas?style=social)](https://github.com/pandas-dev/pandas) |
| **Numerical Processing** | NumPy for foundational numerical computations [![GitHub Repo stars](https://img.shields.io/github/stars/numpy/numpy?style=social)](https://github.com/numpy/numpy)               |

---

## Limitations 🚧

| **Limitation**         | **Details**                                                                                                                                        |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| **Dataset Dependency** | Relies on the structure of the current dataset. Improving flexibility for any taxi trip database requires configurable column mappings.            |
| **Platform Testing**   | Tested on 🍎 **macOS Sequoia** on an Apple Silicon-based machine. Compatibility on other platforms like Linux is anticipated; Windows is untested. |

---

## 📖 **Further Reading**

For detailed context and broader system architecture, refer to:  
➡️ [Frontend README](https://github.com/VIDA-NYU/Taxis-Vis-Frontend)