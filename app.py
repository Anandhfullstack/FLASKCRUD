from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://anand:anand@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Creating model table for our CRUD database
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    user_Accounts = db.relationship('User_Accounts', backref='user', lazy=True)
    user_Transaction_Accounts = db.relationship('User_Transaction_Accounts', backref='user', lazy=True)

    def __init__(self, name, email, phone):

        self.name = name
        self.email = email
        self.phone = phone


class User_Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    def __init__(self, total_amount, type, user_id):


        self.total_amount=total_amount
        self.type = type
        self.user_id = user_id


class User_Transaction_Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transfer_amount = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)

    def __init__(self, transfer_amount, type, user_id):
        self.transfer_amount = transfer_amount
        self.type = type
        self.user_id = user_id

#This is the index route where we are going to
#query on all our employee data
@app.route('/home',methods=['GET', 'POST'])
def Index():
    ses = session.get('id')
    print(ses)
    all_data = User_Transaction_Accounts.query.all()
    if (ses > 0):
        return render_template("index.html", employees=all_data)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email=="ananthagopi003@gmail.com" and password=="12345" :
            session['id'] = 1

            my_data = User.query.get('1')

            #session['useremail'] = my_data.id;
            flash("Welcome to the Panel "+my_data.name)

            return render_template("index.html", employees=all_data)

    flash("Authentication Failed")
    return render_template("login.html")



@app.route('/')
def login():
    return render_template("login.html")


#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        transfer_amount = int(request.form['transfer_amount'])
        user = User.query.get(1)
        user_accounts = User_Accounts.query.get(1)
        tot=user_accounts.total_amount
        tra=transfer_amount
        my_data=""
        print(transfer_amount)
        print(tot)
        print(tot >= tra)
        if tot >= transfer_amount :
            print(transfer_amount)
            my_data = User_Transaction_Accounts(transfer_amount, 1, user.id)
            bal=tot-transfer_amount
            print(bal)
            user_accounts.total_amount=bal
            db.session.add(my_data)
            db.session.commit()
            print(tot)
            flash("Amount Transferred Successfully, Your Balance : "+str(bal))
        else:
            flash("Transaction Failed, Insufficent Fund")
        return redirect(url_for('Index'))


#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = User.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))





#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = User.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('Index'))






if __name__ == "__main__":
    app.run(debug=True)