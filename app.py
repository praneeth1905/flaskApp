import email
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SECRET_KEY']="random"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.sqlite3'

db=SQLAlchemy(app)

class users(db.Model):
    id=db.Column('user_id', db.Integer, primary_key=True)
    name=db.Column(db.String(20))
    book=db.Column(db.String(20))
    type=db.Column(db.String(20))
    cost=db.Column(db.Integer)
    quantity=db.Column(db.Integer)

def __init__(self,name,book,type,cost,quantity):
    self.name=name
    self.book=book
    self.type=type
    self.cost=cost
    self.quantity=quantity

@app.route('/',methods=['POST','GET'])
@app.route('/customer',methods=['POST','GET'])
def customer():
    if request.method=='POST':

        user=users(name=request.form.get('name'),book =  request.form.get('book-names'), type=request.form.get('type'), cost =request.form.get('cost'),quantity= request.form.get('quantity'))
        db.session.add(user)
        db.session.commit()
        flash('books added','success')
    return render_template('customer.html')

@app.route('/admin',methods=['POST','GET'])
def admin():
    
    return render_template("admin.html",users=users.query.all())


class database(db.Model):
    id=db.Column(db.Integer,primary_key = True)
    email=db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))

def __init__(self,email,password):
    self.email=email
    self.password=password

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == "POST":
        DB=database(email=request.form.get('email'),password = request.form.get('password'))
        db.session.add(DB)
        db.session.commit()
        flash('registered','success')
    return render_template("register.html")


@app.route('/login',methods=['POST','GET'])
def login():
    email=request.form.get('email')
    password=request.form.get('password')
    d = database.query.filter_by(email=email).first()
    if not d :
        flash('please check details')
        return render_template("login.html",database=database)
    else:
        flash('welcome')
        redirect(url_for('customer'))

    return render_template("login.html",database=database)

if __name__== '__main__':
    db.create_all()
    app.run(debug=True)
    