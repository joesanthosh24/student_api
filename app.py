# student_service.py

from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

students = {
    '1': {'id': '1', 'name': 'Joe', 'grade': 'A'},
    '2': {'id': '2', 'name': 'Mike', 'email': 'B'}
}

@app.route('/')
def hello():
    return "Hello from Student service"

@app.route('/student/<id>')
def student(id):
    student_info = students.get(id, {})
    return jsonify(student_info)

@app.route('/student', methods=['POST'])
def create_studnet():
    data = request.json
    name = data.get('name')
    grade = data.get('grade')

    new_student_id = str(uuid.uuid1())

    students[new_student_id] = { 'id': new_student_id, 'name': name, 'grade': grade }

    return jsonify({
        'new_student': students[new_student_id],
        'all_students': students
    })

@app.route('/students/<id>', methods=['PUT'])
def update_student(id):
    student_ids = list(students.keys())

    if id in student_ids:
        data = request.json
        grade = students[id]['grade']
        name = students[id]['name']
        if data.get('grade'):
            grade = data.get('grade')
        if data.get('name'):
            name = data.get('name')

        students[id] = { 'grade': grade, 'name': name }

        return jsonify({
            'updated_student': students[id],
            'all_students': students
        })
    
    return jsonify('Student with this id does not exist')

@app.route('/students/<id>', methods=['DELETE'])
def delete_student(id):
    students_obj = list(students.keys())

    if id in students_obj:
        student_to_delete = students[id]
        students.pop(id)

        return jsonify({
            'deleted_student': student_to_delete,
            'all_students': students
        })
    
    return jsonify({'Student with this id does not exist'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
