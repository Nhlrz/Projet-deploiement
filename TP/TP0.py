from flask import Flask, jsonify, rquest

app = Flask (__name__)
sutdents =[
   {"id": 1, "prenom": "Samir", "age":31},
  {"id" :2, "prenom": "safa", "age": 22} 
] 
#on défini la racine de l'API
@app.route('/')
def home():
    return "C'est cool REST !"

@app.route('/students', methods=['GET'])
deg get_students():
    return jsonify(students)

@app.route('/students', methods=['POST'])
def add_student():
    new_student = request.get_json()
    new_student[id]=len(students) +1
    students.append(new_student)
    return new_student, 201


@app.route('/students/<int:id>', methods=['GET'])
def get_student_byid(id):
    student = next(s for s in students if s['id']==id , None)
    if student :
        return jsonify(student)
    return jsonify({"erreur" : " L'étudiant n'a pas été trouvé"} ), 404

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = next(s for s in students if s['id']==id , None)
    if not student :
        return jsonify({"erreur" : " L'étudiant n'a pas été trouvé"} ), 404
    data = request.get_json()
    student.update(data)
    return jsonify(student)


def delete_student(id):
    global students
    students =[s for s in students if s['id'] != id]
    return jsonify({"message" : "Ok"} ), 200  

if __name__ =='main': 
    app.run(debug=True)
