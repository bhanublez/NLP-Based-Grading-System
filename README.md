## 🧠 AGSAI – Automated Grading System using AI

A web-based intelligent system that predicts student performance using machine learning. Built with Python, Flask, and Scikit-learn, this project helps educators evaluate and analyze student data with real-time feedback and predictive insights.

---

## 🚀 Project Setup & Installation

Follow the steps below to run the project locally:

### 1. 📁 Clone the Repository
```bash
git clone https://github.com/bhanublez/NLP-Based-Grading-System
cd NLP-Based-Grading-System
```

### 2. 🛠️ Create a Virtual Environment
```bash
# For Windows:
python -m venv venv
venv\Scripts\activate

# For Linux/Mac:
python3 -m venv venv
source venv/bin/activate
```

### 3. 📦 Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. 🗂️ Create Required Directories
```bash
mkdir -p static/uploads static/css static/images
```

### 5. ▶️ Run the Application
```bash
python app.py
```

Then open your browser and go to:  
**http://127.0.0.1:5000/**

---

## 📌 Features

- ML-based performance prediction
- Dashboards for Admin, Teacher, and Student
- Visual analytics using Plotly & Chart.js
- Alerts & feedback system
- Secure login & session management

---

## 📚 Technologies Used

- **Frontend:** HTML5, CSS3, JS, Bootstrap 5
- **Backend:** Flask, Python 3.8
- **ML:** Scikit-learn, Pandas, NumPy
- **Database:** MySQL 8.0 + SQLAlchemy ORM
- **Visualization:** Chart.js, Plotly

---
