import streamlit as st
import pandas as pd
import numpy as np
import joblib

# 1. Page Configuration
st.set_page_config(page_title="MCA Attendance Forecaster", page_icon="🎓", layout="wide")


# 2. Load Model, Features, and Historical Data
@st.cache_resource
def load_assets():
    model = joblib.load('mca_attendance_model.pkl')
    model_features = joblib.load('model_features.pkl')
    df_history = pd.read_excel('Final_MCA_Attendance_Dataset.xlsx', sheet_name='Attendance_Data')
    return model, model_features, df_history


model, model_features, df_history = load_assets()

# 3. App Header
st.title("🎓 MCA Smart Classroom Attendance Forecaster")
st.markdown(
    "Predict student turnout using the XGBoost machine learning model trained on historical timetable and environmental data.")

# 4. Sidebar - User Inputs
st.sidebar.header("📝 Input Lecture Details")

section = st.sidebar.selectbox("Section", ["A", "B"])
day_of_week = st.sidebar.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
lecture_num = st.sidebar.slider("Lecture Number", 1, 4, 1)
time_of_day = "Morning" if lecture_num <= 2 else "Afternoon"

# Subject & Faculty logic based on section
if section == "A":
    subject = st.sidebar.selectbox("Subject",
                                   ['Python', 'DBMS', 'Web Tech', 'Industry Readiness Program', 'Data Structures',
                                    'Innovation and Entrepreneurship Development', 'Selenium (STQA)',
                                    'Cloud Computing (AWS)', 'AWS COMPUTE SERVICES'])
    faculty_id = st.sidebar.selectbox("Faculty",
                                      ['F_A_1', 'F_A_2', 'F_A_3', 'F_A_4', 'Sohan Dadarkar', 'Sopan Aghav Sir',
                                       'Mr. Keshav Potdar', 'Mr. Kiran Nikam', 'Mr. Sarvesh Deshpande'])
    total_stud = 103
else:
    subject = st.sidebar.selectbox("Subject", ['Python', 'DBMS', 'Java', 'Operating Systems', 'Software Eng',
                                               'Cloud Computing (AWS)', 'Selenium (STQA)'])
    faculty_id = st.sidebar.selectbox("Faculty",
                                      ['F_B_1', 'F_B_2', 'F_B_3', 'F_B_4', 'Mr. Kiran Nikam', 'Mr. Keshav Potdar'])
    total_stud = 102

practical_theory = st.sidebar.selectbox("Session Type", ["Theory", "Practical"])
classroom = st.sidebar.selectbox("Classroom", ["403", "Computer Lab", "Seminar Hall"])
faculty_exp = st.sidebar.slider("Faculty Experience (Years)", 3, 15, 8)
prev_attendance = st.sidebar.slider("Previous Lecture Attendance (%)", 30.0, 100.0, 75.0)
gap_since_prev = 0.0 if lecture_num == 1 else 1.0

st.sidebar.markdown("---")
st.sidebar.subheader("External Factors")
internal_test = st.sidebar.selectbox("Internal Test Week", ["No", "Yes"])
assignment_due = st.sidebar.selectbox("Assignment Due", ["No", "Yes"])
holiday_near = st.sidebar.selectbox("Holiday Before/After", ["No", "Yes"])
weather = st.sidebar.selectbox("Weather Condition", ["Sunny", "Cloudy", "Rainy"])
special_event = st.sidebar.selectbox("Special Event / Guest Lecture", ["No", "Yes"])
week_num = st.sidebar.slider("Week Number of Semester", 1, 10, 5)
day_of_sem = st.sidebar.slider("Day of Semester", 1, 60, 25)

# 5. Prediction Logic
if st.sidebar.button("🔮 Predict Attendance", use_container_width=True):
    # Map Yes/No to 1/0 for Label Encoded features
    binary_map = {"Yes": 1, "No": 0}

    input_dict = {
        'Day of Week': day_of_week,
        'Lecture Number': lecture_num,
        'Subject': subject,
        'Faculty ID': faculty_id,
        'Section': section,
        'Classroom': classroom,
        'Total Enrolled Students': total_stud,
        'Previous Lecture Attendance': prev_attendance,
        'Gap Since Previous Lecture': gap_since_prev,
        'Practical/Theory': practical_theory,
        'Internal Test Week': binary_map[internal_test],
        'Assignment Due': binary_map[assignment_due],
        'Holiday Before/After': binary_map[holiday_near],
        'Weather': weather,
        'Special Event': binary_map[special_event],
        'Faculty Experience': faculty_exp,
        'Week Number': week_num,
        'Day of Semester': day_of_sem,
        'Time of Day': time_of_day
    }

    # Convert to dataframe and One-Hot Encode
    input_df = pd.DataFrame([input_dict])
    input_encoded = pd.get_dummies(input_df)

    # Align with training features (fill missing dummy columns with 0)
    input_encoded = input_encoded.reindex(columns=model_features, fill_value=0)

    # Predict
    prediction = model.predict(input_encoded)[0]
    prediction = np.clip(prediction, 0, 100)  # Ensure it stays between 0-100%
    predicted_students = int(round((prediction / 100.0) * total_stud))

    # Display Results
    st.markdown("### 🎯 Prediction Results")
    col1, col2, col3 = st.columns(3)
    col1.metric("Predicted Attendance %", f"{prediction:.2f}%")
    col2.metric("Estimated Students Present", f"{predicted_students} / {total_stud}")

    if prediction >= 75:
        col3.success("Status: High Attendance Expected 🟢")
    elif prediction >= 55:
        col3.warning("Status: Moderate Attendance 🟡")
    else:
        col3.error("Status: Low Attendance Risk 🔴")

    # 6. Analytics Dashboard Section
    st.markdown("---")
    st.header("📊 Department & Subject Analytics")

    st.subheader(f"1. Historical Attendance Trend for {subject}")
    subject_data = df_history[df_history['Subject'] == subject]
    if not subject_data.empty:
        chart_data = subject_data[['Attendance Percentage']].reset_index(drop=True)
        st.line_chart(chart_data)
    else:
        st.info("Not enough historical data available to plot a trend for this specific subject.")

    g_col1, g_col2 = st.columns(2)
    with g_col1:
        st.subheader("2. Average Attendance by Faculty")
        faculty_avg = df_history.groupby('Faculty ID')['Attendance Percentage'].mean().reset_index().set_index(
            'Faculty ID')
        st.bar_chart(faculty_avg)

    with g_col2:
        st.subheader("3. Previous vs Current Attendance")
        scatter_data = df_history[['Previous Lecture Attendance', 'Attendance Percentage']].dropna()
        st.scatter_chart(scatter_data, x='Previous Lecture Attendance', y='Attendance Percentage')
else:
    st.info(
        "👈 Adjust the lecture parameters in the sidebar and click **Predict Attendance** to see the forecast and analytics.")