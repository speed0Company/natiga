from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Path to your .xlsx file
excel_file_path = 'نتيجة الثانوية 24.xlsx'  # Replace with the actual file path

# Load the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file_path)

# Define a function to search by name or student ID and get the student details
def search_students(search_type, search_value):
    if search_type == 'name':
        filtered_df = df[df['الاسم'].str.contains(search_value, na=False)]
    elif search_type == 'student_id':
        filtered_df = df[df['رقم الجلوس'] == search_value]
    else:
        return []  # Invalid search type

    results = []
    for index, row in filtered_df.iterrows():
        percentage = (row['الدرجة'] / 410) * 100  # Calculate the percentage
        results.append({
            'arabic_name': row['الاسم'],
            'student_id': row['رقم الجلوس'],
            'grade': row['الدرجة'],
            'percentage': percentage,
            'student_case': row['student_case'],
            'student_case_desc': row['student_case_desc'],
            'c_flage': row['c_flage']
        })
    return results

@app.route('/search', methods=['GET'])
def search():
    name = request.args.get('name')
    student_id = int(request.args.get('student_id'))

    if name:
        students = search_students('name', name)
        return jsonify(students)
    elif student_id:
        students = search_students('student_id', student_id)
        return jsonify(students)
    else:
        return jsonify({'error': 'Either name or student_id parameter is required'}), 400

if __name__ == '__main__':
    app.run(debug=True)
