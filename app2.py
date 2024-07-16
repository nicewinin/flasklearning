from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


# 第四天学习Flask，学习数据库与前后段数据传输
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task_id = db.Column(db.String(50), nullable = False)
    route_choice = db.Column(db.String(100), nullable = False)
    score = db.Column(db.Float, nullable = False)
    
    
    def __repr__(self):
        return f"Task(id={self.id}, task_id='{self.task_id}', route_choice='{self.route_choice}', score={self.score})"
    
@app.route('/get_tasks',methods=['GET'])
def get_tasks():
    tasks = Task.query.filter_by(id=123).all()
    result = []
    for task in tasks:
        result.append({
            'id':task.id,
            'task_id':task.task_id,
            'route_choice':task.route_choice,
            'score':task.score
        })
    print("\n===============\n",result,"\n===============\n")
    return result

@app.route('/add_tasks', methods=['POST'])
def add_tasks():
    # 在网页上通过json传递数据
    data = request.get_json()
    print("\n===============\n",data,"\n===============\n")
    id = data['id']
    task_id = data['task_id']
    route_choice = data['route_choice']
    score = data['score']
    if not id or not task_id or not route_choice or not score:
        return jsonify({'message': 'Missing Data'}), 400
    task = Task(id=id,task_id=task_id, route_choice=route_choice, score=score)
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Add Successfully'})

@app.route('/del_tasks',methods=['POST'])
def def_tasks():
    data = request.get_json() # data是自典型数据
    del_id = data['id'] 
    print(del_id,'\n',type(del_id))
    tasks = Task.query.filter_by(id=del_id).all()
        
    if not tasks:
        return jsonify({'message': 'Task not found'}), 404
    
    for task in tasks:        
        db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Deletion successful'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)