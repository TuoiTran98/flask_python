from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
    
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'doan'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)



@app.route('/')
def index(name=None):
    return render_template('index.html',name=name)

@app.route('/getdata')
def parse(name=None):
    import getData
    print("done")
    return render_template('index.html',name=name)

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/createData', methods=['POST','GET'])
def createData():

        id = request.form['id']
        name = request.form['name']
        gender = request.form['gender']
        dateofbirth = request.form['dateofbirth']
        phonenumber = request.form['phonenumber']

        if id and name and gender and dateofbirth and phonenumber:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM employee WHERE id="+ str(id))
            result = cursor.fetchall()

            isRecorExist = 0
            for x in result:
                isRecorExist = 1
            if(isRecorExist == 0):
                cursor.execute("INSERT INTO employee(id, name, gender, dateofbirth, phonenumber) VALUES("+ str(id) + ",'"+str(name)+"','"+str(gender)+"','"+str(dateofbirth)+"','"+str(phonenumber)+"')")               
            else:
                cursor.execute("UPDATE employee SET name='" + str(name) + "', gender='" + str(gender) + "' , dateofbirth='" + str(dateofbirth) + "', phonenumber='" + str(phonenumber) + "'WHERE id="+str(id))

            conn.commit()
            conn.close()
            return ("Successful")
        else:
            return("Enter the required fields")
@app.route('/TrainingData')
def parse1(name=None):
	import TrainingData
	print("done")
	return render_template('index.html',name=name)

@app.route('/RecognitionData')
def parse2(name=None):
	import RecognitionData
	print("done")
	return render_template('index.html',name=name)

if __name__ == '__main__':
    app.run()
    app.debug = True