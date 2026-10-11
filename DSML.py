import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta

def generate_comprehensive_attendance_dataset():
    # Set random seed for reproducibility
    np.random.seed(42)
    
    start_date = datetime(2026, 6, 17)
    end_date = datetime(2026, 8, 17)
    
    # Generate operational dates (excluding Sundays)
    current_date = start_date
    dates = []
    while current_date <= end_date:
        if current_date.weekday() != 6: # Exclude Sunday
            dates.append(current_date)
        current_date += timedelta(days=1)
        
    muharram_date = datetime(2026, 6, 26)
    
    subjects_sec_a = ['Python', 'DBMS', 'Web Tech', 'Industry Readiness Program', 'Data Structures']
    subjects_sec_b = ['Python', 'DBMS', 'Java', 'Operating Systems', 'Software Eng']
    
    lecture_times = [
        (time(9, 15), time(10, 15)),
        (time(10, 15), time(11, 15)),
        (time(11, 30), time(12, 30)),
        (time(13, 30), time(14, 30))
    ]
    
    records = []
    
    for d in dates:
        if d == muharram_date:
            continue # Skip Muharram holiday on 26th June 2026
            
        day_name = d.strftime('%A')
        is_test_week = 'Yes' if 10 <= d.day <= 14 and d.month == 7 else 'No'
        holiday_near = 'Yes' if day_name == 'Saturday' or (d.day == 15 and d.month == 8) else 'No'
        
        for section, total_stud, subs in [('A', 103, subjects_sec_a), ('B', 102, subjects_sec_b)]:
            prev_perc = 78.0
            
            for l_idx in range(4): # 4 lectures per day per section
                start_t, end_t = lecture_times[l_idx]
                
                sub = np.random.choice(subs)
                faculty_id = f"F_{section}_{l_idx+1}"
                if sub == 'Industry Readiness Program':
                    faculty_id = 'Sohan Dadarkar'
                    
                is_special = 'No'
                practical_theory = 'Theory' if l_idx < 3 else 'Practical'
                
                # Custom Timetable & Guest Session Injection Rules
                if d >= datetime(2026, 7, 13) and d <= datetime(2026, 8, 13) and day_name == 'Monday' and l_idx == 1:
                    sub = 'Innovation and Entrepreneurship Development'
                    faculty_id = 'Sopan Aghav Sir'
                    is_special = 'Yes'
                elif d >= datetime(2026, 7, 27) and d <= datetime(2026, 8, 7) and day_name in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] and l_idx == 0:
                    sub = 'Selenium (STQA)'
                    faculty_id = 'Mr. Keshav Potdar'
                elif d >= datetime(2026, 8, 2) and start_t >= time(13, 30) and day_name in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                    sub = 'Cloud Computing (AWS)'
                    faculty_id = 'Mr. Kiran Nikam'
                elif d == datetime(2026, 8, 8) and l_idx == 0:
                    sub = 'AWS COMPUTE SERVICES'
                    faculty_id = 'Mr. Sarvesh Deshpande'
                    is_special = 'Yes'
                
                # Classroom Allocation Logic:
                # 403 for theory, Computer Lab for practicals, Seminar Hall for seminars/guest lectures
                if is_special == 'Yes' or 'Seminar' in sub or 'Guest' in sub:
                    classroom = 'Seminar Hall'
                elif practical_theory == 'Practical':
                    classroom = 'Computer Lab'
                else:
                    classroom = '403'
                
                # Attendance Percentage Modeling
                base_att = 76.0
                if day_name == 'Monday': base_att -= 8.0
                if day_name == 'Saturday': base_att -= 12.0
                if is_test_week == 'Yes': base_att += 6.0
                
                att_perc = np.clip(base_att + np.random.normal(0, 8), 35.0, 98.0)
                present_count = int(round((att_perc / 100.0) * total_stud))
                att_perc = round((present_count / total_stud) * 100.0, 2)
                
                records.append({
                    'Date': d.strftime('%Y-%m-%d'),
                    'Day of Week': day_name,
                    'Lecture Number': l_idx + 1,
                    'Start Time': start_t.strftime('%H:%M:%S'),
                    'End Time': end_t.strftime('%H:%M:%S'),
                    'Subject': sub,
                    'Faculty ID': faculty_id,
                    'Semester': 'III',
                    'Branch': 'MCA',
                    'Section': section,
                    'Classroom': classroom,
                    'Total Enrolled Students': total_stud,
                    'Students Present': present_count,
                    'Attendance Percentage': att_perc,
                    'Previous Lecture Attendance': round(prev_perc, 2),
                    'Gap Since Previous Lecture': 0.0 if l_idx == 0 else 1.0,
                    'Practical/Theory': practical_theory,
                    'Internal Test Week': is_test_week,
                    'Assignment Due': 'Yes' if np.random.rand() < 0.25 else 'No',
                    'Holiday Before/After': holiday_near,
                    'Weather': np.random.choice(['Sunny', 'Cloudy', 'Rainy'], p=[0.5, 0.3, 0.2]),
                    'Special Event': is_special,
                    'Faculty Experience': np.random.randint(3, 15),
                    'Week Number': (d - start_date).days // 7 + 1,
                    'Day of Semester': (d - start_date).days + 1,
                    'Time of Day': 'Morning' if start_t.hour < 12 else 'Afternoon'
                })
                prev_perc = att_perc
                
    df = pd.DataFrame(records)
    output_filename = "Final_MCA_Attendance_Dataset.xlsx"
    df.to_excel(output_filename, sheet_name='Attendance_Data', index=False)
    print(f"Dataset successfully generated with {len(df)} records and saved as {output_filename}!")

if __name__ == '__main__':
    generate_comprehensive_attendance_dataset()