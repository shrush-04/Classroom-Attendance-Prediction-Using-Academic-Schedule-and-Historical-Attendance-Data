# Example Row Format

Here are examples of properly formatted rows that comply with the data dictionary and privacy requirements.

### Example 1: Regular Theory Lecture (Weekday)
- **Lecture_ID**: `LEC0001`
- **Date**: `2026-08-03`
- **Day_of_Week**: `Monday`
- **Lecture_Number**: `1`
- **Start_Time**: `09:00`
- **End_Time**: `10:00`
- **Subject**: `MCA301`
- **Faculty_ID**: `F001`
- **Semester**: `Third Semester`
- **Branch**: `MCA`
- **Section**: `A`
- **Classroom**: `CR201`
- **Total_Enrolled_Students**: `60`
- **Students_Present**: `54`
- **Attendance_Percentage**: `90.00`
- **Previous_Lecture_Attendance_Percentage**: `Not_Collected` (first lecture of semester)
- **Gap_Since_Previous_Lecture_Hours**: `Not_Collected`
- **Practical_Theory**: `Theory`
- **Internal_Test_Week**: `0`
- **Assignment_Due**: `0`
- **Holiday_Before_After**: `None`
- **Weather**: `Sunny`
- **Special_Event**: `None`

---

### Example 2: Laboratory Session (Friday)
- **Lecture_ID**: `LEC0015`
- **Date**: `2026-08-07`
- **Day_of_Week**: `Friday`
- **Lecture_Number**: `4`
- **Start_Time**: `13:30`
- **End_Time**: `15:30`
- **Subject**: `MCA305`
- **Faculty_ID**: `F003`
- **Semester**: `Third Semester`
- **Branch**: `MCA`
- **Section**: `B`
- **Classroom**: `Lab B`
- **Total_Enrolled_Students**: `60`
- **Students_Present**: `48`
- **Attendance_Percentage**: `80.00`
- **Previous_Lecture_Attendance_Percentage**: `85.00`
- **Gap_Since_Previous_Lecture_Hours**: `24.0`
- **Practical_Theory**: `Practical`
- **Internal_Test_Week**: `0`
- **Assignment_Due**: `1`
- **Holiday_Before_After**: `Holiday_After` (before weekend or official holiday)
- **Weather**: `Rainy`
- **Special_Event**: `Workshop`

---

### Raw CSV Representation
```csv
Lecture_ID,Date,Day_of_Week,Lecture_Number,Start_Time,End_Time,Subject,Faculty_ID,Semester,Branch,Section,Classroom,Total_Enrolled_Students,Students_Present,Attendance_Percentage,Previous_Lecture_Attendance_Percentage,Gap_Since_Previous_Lecture_Hours,Practical_Theory,Internal_Test_Week,Assignment_Due,Holiday_Before_After,Weather,Special_Event
LEC0001,2026-08-03,Monday,1,09:00,10:00,MCA301,F001,Third Semester,MCA,A,CR201,60,54,90.0,Not_Collected,Not_Collected,Theory,0,0,None,Sunny,None
LEC0015,2026-08-07,Friday,4,13:30,15:30,MCA305,F003,Third Semester,MCA,B,Lab B,60,48,80.0,85.0,24.0,Practical,0,1,Holiday_After,Rainy,Workshop
```
