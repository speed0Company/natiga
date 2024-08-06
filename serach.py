from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Path to your .xlsx file
excel_file_path = 'نتيجة الثانوية 24.xlsx'  # Replace with the actual file path

# Load the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file_path)

# Define a function to search by partial name and get the student details
def search_by_partial_name(partial_name):
    filtered_df = df[df['الاسم'].str.contains(partial_name, na=False)]
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
    if name:
        students = search_by_partial_name(name)
        return jsonify(students)
    else:
        return jsonify({'error': 'Name parameter is required'}), 400

@app.route('/search/<name>', methods=['GET'])
def search_by_name_route(name):
    students = search_by_partial_name(name)
    return jsonify(students)

if __name__ == '__main__':
    app.run(debug=True)
