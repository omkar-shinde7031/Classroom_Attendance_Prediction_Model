# 🎓 Classroom Attendance Prediction
 
### Using Academic Schedule and Historical Attendance Data

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-orange)
![Streamlit](https://img.shields.io/badge/App-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![R²](https://img.shields.io/badge/R%C2%B2-0.971-brightgreen)
![Accuracy](https://img.shields.io/badge/Accuracy-94.2%25-brightgreen)
 

<img width="1880" height="1031" alt="image" src="https://github.com/user-attachments/assets/8933bd9a-1b1f-4842-817e-c5dd7050f578" />
<hr>
<img width="1883" height="1033" alt="image" src="https://github.com/user-attachments/assets/9c9fbcc0-b9ad-4112-801b-e6fe92d736c9" />
<hr>
<img width="1888" height="1025" alt="image" src="https://github.com/user-attachments/assets/d388ec39-68e8-4cea-b148-019f5a04ba37" />



 
> **DSML Capstone Project — MCA Semester 3**
>
> A machine learning pipeline that forecasts classroom attendance for upcoming lectures, deployed as an interactive Streamlit dashboard.
 
---
 
## 📌 Table of Contents
 
- [Overview](#-overview)
- [Key Results](#-key-results)
- [Dataset](#-dataset)
- [Feature Engineering](#-feature-engineering)
- [Key Insights from EDA](#-key-insights-from-eda)
- [Model Performance](#-model-performance)
- [Scheduling Recommendations](#-scheduling-recommendations)
- [Dashboard](#-dashboard)
- [Project Structure](#-project-structure)
- [Installation and Usage](#-installation-and-usage)
- [Tech Stack](#-tech-stack)
- [Future Work](#-future-work)
- [Author](#-author)
- [License](#-license)
---
 
## 🔍 Overview
 
Low attendance is hard to plan around because it is usually only noticed after it has happened. This project predicts attendance **before** a lecture takes place, using the academic schedule and historical attendance patterns.
 
Two complementary approaches are implemented:
 
| Task | Goal | Best Model |
|------|------|------------|
| **Regression** | Predict the exact attendance percentage | XGBoost |
| **Classification** | Predict the attendance band (Low / Medium / High) | XGBoost |
 
All trained models, including the comparison models, are served through a Streamlit dashboard for live prediction and analysis.
 
---
 
## 🏆 Key Results
 
| Metric | Value |
|--------|-------|
| Regression R² (XGBoost) | **0.971** |
| Regression MAE (XGBoost) | **4.08** percentage points |
| Classification Accuracy (XGBoost) | **94.2%** |
| Classification F1 Score (XGBoost) | **0.928** |
| Classification ROC-AUC (XGBoost) | **0.986** |
 
The data was split **chronologically** (earliest 80% for training, most recent 20% for testing), so these numbers reflect genuine forecasting of unseen future lectures rather than random-split performance.
 
---
 
## 📊 Dataset
 
Attendance was collected **manually** across two MCA Semester 3 sections.
 
| Detail | Value |
|--------|-------|
| Total records | 519 lectures |
| Subjects | 12 |
| Sections | 2 (Section A and Section B) |
| Collection period | 20 June 2026 to 15 August 2026 |
| Overall average attendance | 46.7% |
 
**Each record captures:** date, day of week, lecture number, start time, subject, faculty, section, enrollment, and attendance counts.
 
**Contextual factors recorded:** weather, proximity to internal tests, assignment deadlines, and holidays.
 
| File | Description |
|------|-------------|
| `attendance_data_raw.csv` | Raw collected data (519 records) |
| `attendance_data_cleaned.csv` | Cleaned and feature-engineered data, ready for modeling |
 
### Data Cleaning
 
- Imputed missing "previous lecture attendance" values using each subject/section's own average
- Removed columns that carried no signal
- Verified there were no duplicate or impossible records
---
 
## 🛠 Feature Engineering
 
| Feature | Description |
|---------|-------------|
| **Day of Semester / Week Number** | Position of the lecture within the term |
| **Rolling Average** | Average attendance of the previous 3 lectures, smoothing short-term fluctuation |
| **Gap Since Previous Lecture** | Days elapsed since the subject was last held |
| **Consecutive Lecture Count** | Position of the lecture within that day's schedule |
| **Time of Day Cluster** | Before-lunch vs. after-lunch grouping |
| **Attendance Band** | Low / Medium / High label derived from the percentage (classification target) |
 
---
 
## 📈 Key Insights from EDA
 
- **Best day:** Wednesday has the highest average attendance (**52.8%**).
- **Worst day:** Saturday has the lowest (**42.2%**). Attendance declines steadily from Monday through Saturday.
- **Subjects:** AWS Cloud Training has the highest average (89.2%), likely because it is a short, high-interest add-on. Excluding workshops, Mobile Application Development leads (52.6%), while Mini Project (36.1%) and Industry Readiness Program (39.2%) are lowest.
- **Trend:** Attendance was broadly stable across the collection window (47.3% in the first half vs. 46.2% in the second), with both sections tracking each other closely.
### Impact of External Factors
 
| Factor | Condition | Avg. Attendance |
|--------|-----------|-----------------|
| Internal Test Week | No | 33.9% |
| Internal Test Week | **Yes** | **85.5%** |
| Weather | Cloudy / Overcast | ~64–65% |
| Weather | Rainy | 25.3% |
| Holiday Before/After | No | 48.5% |
| Holiday Before/After | **Yes** | **19.6%** |
 
> **Takeaway:** Assessment proximity is the single strongest driver of attendance. Holidays sharply reduce it, and rainy weather more than halves it compared to clear conditions.
 
---
 
## 🤖 Model Performance
 
### Regression
 
| Model | MAE ↓ | RMSE ↓ | MAPE (%) ↓ | R² ↑ |
|-------|-------|--------|------------|------|
| **XGBoost** ⭐ | **4.08** | **5.14** | **13.16** | **0.971** |
| Random Forest | 4.59 | 5.87 | 13.53 | 0.962 |
| Gradient Boosting | 4.79 | 6.25 | 16.18 | 0.957 |
| Decision Tree | 5.24 | 6.84 | 14.88 | 0.949 |
| Linear Regression | 20.60 | 26.98 | 61.42 | 0.200 |
 
Linear Regression performs poorly because most predictors are categorical rather than linearly related to attendance.
 
### Classification
 
| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|-------|----------|-----------|--------|-----|---------|
| **XGBoost** ⭐ | **0.942** | **0.919** | **0.944** | **0.928** | **0.986** |
| Decision Tree | 0.894 | 0.865 | 0.865 | 0.865 | 0.973 |
| Logistic Regression | 0.760 | 0.715 | 0.700 | 0.706 | 0.860 |
| Random Forest | 0.635 | 0.504 | 0.526 | 0.470 | 0.956 |
| SVM | 0.558 | 0.379 | 0.458 | 0.413 | 0.702 |
| k-NN | 0.529 | 0.547 | 0.475 | 0.475 | 0.662 |
| Naive Bayes | 0.510 | 0.495 | 0.555 | 0.470 | 0.780 |
 
---
 
## 🗓 Scheduling Recommendations
 
Based on the findings, the project suggests:
 
1. **Avoid optional or make-up sessions on Saturdays**, which have the lowest attendance.
2. **Schedule high-priority or difficult content on Wednesdays**, which have the highest attendance.
3. **Treat lectures adjacent to holidays as review or optional sessions.**
4. **Build slack into the schedule around forecasted rainy days.**
5. **Place recap and doubt-clearing sessions just before assessments**, when attendance is naturally highest.
6. **Use the dashboard weekly** to flag "Low" attendance bands early and intervene.
---
 
## 💻 Dashboard
 
The Streamlit app (`app.py`) loads pre-trained models and diagnostic charts from the `assets/` folder, so it starts fast and gives reproducible results.
 
| Tab | Contents |
|-----|----------|
| **Overview** | Project objective and headline performance |
| **Exploratory Analysis** | Charts and findings |
| **Regression Models** | Experiment table, comparison charts, individual model inspection |
| **Classification Models** | Experiment table, ROC curves, feature importance |
| **Live Prediction** | Interactive form for forecasting upcoming lectures |
 
<!-- Add a screenshot of your dashboard here:
![Dashboard Screenshot](screenshots/dashboard.png)
-->
 
---
 
## 📁 Project Structure
 
```
classroom-attendance-prediction/
├── app.py                          # Streamlit dashboard
├── requirements.txt                # Python dependencies
├── attendance_data_raw.csv         # Raw collected data
├── attendance_data_cleaned.csv     # Cleaned + engineered data
├── notebook.ipynb                  # Training and analysis notebook
├── assets/                         # Exported models and diagnostic charts
├── DOCUMENTATION.docx              # Full project report
└── README.md
```
 
> Adjust file and folder names above to match your repository.
 
---
 
## 🚀 Installation and Usage
 
### 1. Clone the repository
 
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```
 
### 2. Create a virtual environment (recommended)
 
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```
 
### 3. Install dependencies
 
```bash
pip install -r requirements.txt
```
 
### 4. Run the dashboard
 
```bash
streamlit run app.py
```
 
The app opens at `http://localhost:8501`.
 
### 5. (Optional) Retrain the models
 
Open the training notebook and run all cells. This regenerates the models and charts inside `assets/`.
 
```bash
jupyter notebook notebook.ipynb
```
 
---
 
## 🧰 Tech Stack
 
- **Language:** Python
- **Data handling:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Machine learning:** Scikit-learn, XGBoost
- **Deployment:** Streamlit
---
 
## 🔭 Future Work
 
- Collect data across multiple semesters to improve generalization
- Integrate live weather forecasts for automatic prediction inputs
- Extend to other courses and departments
- Add automated weekly reports flagging low-attendance lectures
---
 
## 👤 Author
 
**Omkar shinde**
MCA Semester 3 — DSML Capstone

- Portfolio: [link](portfolio-s2u1.vercel.app)
- LinkedIn: [link](https://www.linkedin.com/in/omkar-shinde-897750326/?isSelfProfile=true)
---
 
## 📄 License
 
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
 
---
 
⭐ If you found this project useful, consider giving it a star!
