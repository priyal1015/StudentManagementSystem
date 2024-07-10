from flask import Flask, request, render_template, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentid = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    emailid = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email address already registered')
        
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user:
            if user.check_password(password):
                session['email'] = user.email
                return redirect(url_for('add_student'))
            else:
                return render_template('login.html', error='Invalid email or password')
        else:
            return render_template('login.html', error='User not registered. Please register first.')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        students = Student.query.all()
        return render_template('dashboard.html', students=students)
    
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'email' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        studentid = request.form['studentid']
        name = request.form['name']
        year = request.form['year']
        course = request.form['course']
        emailid = request.form['emailid']
        address = request.form['address']
        mobile = request.form['mobile']

        new_student = Student(studentid=studentid, name=name, year=year, course=course, emailid=emailid, address=address, mobile=mobile)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('add_student.html')

@app.route('/update_student/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    if 'email' not in session:
        return redirect(url_for('login'))

    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        student.studentid = request.form['studentid']
        student.name = request.form['name']
        student.year = request.form['year']
        student.course = request.form['course']
        student.emailid = request.form['emailid']
        student.address = request.form['address']
        student.mobile = request.form['mobile']
        
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('update_student.html', student=student)

@app.route('/delete_student/<int:id>', methods=['POST'])
def delete_student(id):
    if 'email' not in session:
        return redirect(url_for('login'))

    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()

    return redirect(url_for('dashboard'))

@app.route('/students')
def students():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    students = Student.query.all()
    return render_template('students.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)
