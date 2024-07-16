from flask import Flask, render_template, redirect, url_for, request, abort, make_response, session, jsonify
from werkzeug.wrappers.response import ResponseStream
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # 创建app实例

'''
# 第一节
@app.route('/hello/<name>/')
def hello_name(name):
    return f'hello {name}'

@app.route('/blog/<int:postID>/') # 带变量
def show_blog(postID):
    return f'Blog Number: {postID:d}'

@app.route('/rev/<float:revNo>/')
def revision(revNo):
    return f'Revision Number: {revNo:f}'
    
@app.route('/flask') # 没有斜杠，如果输入URL后面带杠就404报错
def hello_flask():
    return 'hello flask'

@app.route('/python/') # 有斜杠，URL标准写法
def hello_python():
    return 'hello python'

@app.route('/')
def index():
    # return 'hello world' # 最初始的显示
    return render_template('index1.html') # 使用模板后，目录下需要有一个templates目录存放
'''

'''
# 第二节 往模板里面传参数
@app.route('/')
def index():
    t_int = 18
    t_str = 'curry'
    t_list = [1, 5, 4, 3, 2]
    t_dict = {
        'name':'durant',
        'age':28
    }
    return render_template('index2.html',
                           t_int=t_int,
                           t_str=t_str,
                           t_list=t_list,
                           t_dict=t_dict)
'''

'''
# 第三节 Flask静态文件
# 涉及基础模板base.html，扩展index3.html，css静态文件main.css
@app.route('/')
def index():
    return render_template('index3.html') #这是静态文件
'''

'''
# 第四节 URL构建
@app.route('/admin/')
def hello_admin():
    return 'hello admin'

@app.route('/guest/<guest>/')
def hello_guest(guest):
    return f'hello guest {guest}'

@app.route('/guest/<name>/')
def hello_user(name):
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest',guest=name)) # 这里输入hello_guest的参数
'''

'''
# 第五节 将表单数据提交到模板
@app.route('/')
def student():
    return render_template('index5.html')

@app.route('/result/', methods=['POST','GET'])
def result():
    if request.method == 'POST': # 这个定义在index5.html中
        rst = request.form # 从index5.html中传递form数据回来
        return render_template('result5.html',result=rst) # 往result5.html中传递参数

'''

'''
# 第六节 URL重定向与错误
@app.route('/')
def index():
    return render_template('index7.html')

@app.route('/login/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin':
            return redirect(url_for('success'))
        else:
            abort(404)
    elif request.method == 'GET':
        return redirect(url_for('index'))
    
@app.route('/success/')
def success():
    return 'logged in successfully'
    
'''

'''
# 第七节 cookie和response
@app.route('/set_cookies/')
def set_cookie():
    resp = make_response('success')
    resp.set_cookie('aaa_key','aaa_value',max_age=3600)
    return resp

@app.route('/get_cookies/')
def get_cookie():
    cookie_1= request.cookies.get("aaa_key")
    return cookie_1

@app.route('/delete_cookies/')
def del_cookie():
    resp = make_response('del success')
    resp.delete_cookie("aaa_key")
    return resp
'''

'''
# 第八节 session(会话)
# session也是存在cookies里,session id是加密的
app.secret_key = '123456'

@app.route('/')
def index():
    if 'username' in session:
        user = session['username']
        return '登录用户名是：' + user + '<br>' + "<b><a href='/logout'>点击这里注销</a></b>"
    return "您暂未登录，<br><a href='/login'><b>点击这里登录</b></a>"
    
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST': # 提交表单
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    elif request.method == 'GET': # 刷新页面
        return render_template('index7.html')

@app.route('/logout')
def logout():
    logout = session.pop('username',None)
    return redirect(url_for('index'))
'''

# 第九节 sqlalchemy，网页与数据库交互
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    task_id = db.Column(db.String(100), primary_key=True)
    version = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Task {self.task_id}, Version {self.version}>'

@app.before_request
def create_tables():
    db.create_all()
    # 删除之前插入的数据，防止重复插入
    db.session.query(Task).delete()
    db.session.commit()
    # 填充初始数据
    initial_data = [
        ("id_01", "v01"),
        ("id_02", "v02"),
        ("id_03", "v03"),
        ("id_04", "v04"),
        ("id_05", "v02"),
        ("id_06", "v04"),
        ("id_07", "v07"),
        ("id_08", "v07"),
        ("id_09", "v09"),
        ("id_10", "v06")
    ]
    for task_id, version in initial_data:
        task = Task(task_id=task_id, version=version)
        db.session.add(task)
    db.session.commit()

@app.route('/update_or_insert', methods=['POST'])
def update_or_insert():
    data = request.get_json()
    task_id = data.get('task_id')
    version = data.get('version')

    if not task_id or not version:
        return jsonify({"error": "Task ID and version are required"}), 400

    task = Task.query.filter_by(task_id=task_id).first()

    if task:  # task_id相同，提示是否覆盖
        return jsonify({"error": f"Task ID '{task_id}' already exists."}), 400
    else:
        # task_id不同，检查version
        task_with_version = Task.query.filter_by(version=version).first()
        if task_with_version:  # version相同, 报错
            return jsonify({"error": f"Version '{version}' already exists for a different task ID."}), 400
        else:  # 直接插入
            new_task = Task(task_id=task_id, version=version)
            db.session.add(new_task)
            db.session.commit()
            return jsonify({"msg": "Task added successfully"}), 201

@app.route('/force_update', methods=['POST'])
def force_update():
    data = request.get_json()
    task_id = data.get('task_id')
    version = data.get('version')

    if not task_id or not version:
        return jsonify({"error": "Task ID and version are required"}), 400

    task = Task.query.filter_by(task_id=task_id).first()
    if task:
        task.version = version
        db.session.commit()
        return jsonify({"msg": "Task updated successfully"}), 200
    else:
        return jsonify({"error": "Task ID does not exist"}), 400

@app.route('/')
def index():
    return render_template('index8.html')

if __name__ == '__main__':
    app.run(debug=True)