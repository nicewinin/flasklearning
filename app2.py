from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# 第四天学习Flask，学习数据库与前后段数据传输
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)

@app.before_request
def db_create_all(): # 在请求前创建所有的表格
    with app.app_context():
        db.create_all()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task_id = db.Column(db.String(50), nullable = False)
    route_choice = db.Column(db.String(100), nullable = False)
    score = db.Column(db.Float, nullable = False)
    
    
    def __repr__(self):
        return f"Task(id={self.id}, task_id='{self.task_id}', route_choice='{self.route_choice}', score={self.score})"
    
@app.route('/get_tasks',methods=['GET'])
def get_tasks():
    try:
        # tasks = Task.query.filter_by(id=id).all() # 这3种filter方法都可以针对确定的id查询
        # tasks = Task.query.filter(Task.id==id).all()
        # tasks = db.session.query(Task).filter(Task.id==id).all()
        tasks = db.session.query(Task).all()
        if not tasks:
            return jsonify({'message': 'No Tasks Found'})
        else:
            result = []
            for task in tasks:
                result.append({
                    'id':task.id,
                    'task_id':task.task_id,
                    'route_choice':task.route_choice,
                    'score':task.score
                })
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/get_tasks/all') # 不要什么方法，直接跳转
def get_tasks_all():
    return redirect(url_for('get_tasks'))

@app.route('/add_tasks', methods=['POST'])
def add_tasks():
    # 在网页上通过json传递数据
    data = request.get_json() # data是字典列表
    print("\n===============\n",data,"\n===============\n")
    for data_ in data:
        id = data_['id'] # 主键，保证唯一性
        if db.session.query(Task).filter(Task.id==id).first():
            return jsonify({'message': f'ID.{id} already exists'}), 400
        
        task_id = data_['task_id']
        route_choice = data_['route_choice']
        score = data_['score']
        if not id or not task_id or not route_choice or not score:
            return jsonify({'message': 'Missing Data'}), 400
        
        task = Task(id=id,task_id=task_id, route_choice=route_choice, score=score)
        db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Add Successfully'})

@app.route('/del_tasks',methods=['POST'])
def del_tasks():
    # data数据格式{“command”: "del_all"}{"command":"del_id","id":123}
    data = request.get_json() # data是字典型数据
    if data['command'] == 'del_all':
        tasks = db.session.query(Task).all()
        for task in tasks:
            db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'All tasks deleted successfully'})
    elif data['command'] == 'del_id':
        del_id = data['id']
        need_delete_task = db.session.query(Task).filter(Task.id==del_id).first()
        if not need_delete_task:
            return jsonify({'message': 'Task not found'}), 404
        else:
            db.session.delete(need_delete_task)
            db.session.commit()
        return jsonify({'message': f'Task with ID.{del_id} deleted successfully'})
    
@app.route('/update_tasks',methods=['POST'])
def update_tasks():
    data = request.get_json()
    # data数据{"id":123,"task_id":"C09","route_choice":"C09_71","score":90}
    if not db.session.query(Task).filter(Task.id==data['id']).first():
        return jsonify({'message': 'Task not found'}), 404
    
    # 通过更新查询的属性，实现对表单的更新
    update_query = db.session.query(Task).filter(Task.id==data['id']).first()
    update_query.task_id = data['task_id']
    update_query.route_choice = data['route_choice']
    update_query.score = data['score']
    
    db.session.commit()
    return jsonify({'message': f"ID.{data['id']} Updated successfully"})
 
    

if __name__ == '__main__':
    # print(app.url_map) # 获得路由与视图函数的映射关系
    app.run(debug=True)