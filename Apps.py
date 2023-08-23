from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
# Establish the connection
conn = sqlite3.connect('Aadhar_detail.db')
cursor = conn.cursor()

# Creating table
cursor.execute('''CREATE TABLE IF NOT EXISTS ADHAR 
               (adhar_no INTEGER PRIMARY KEY NOT NULL,
               name VARCHAR(30),
               address TEXT,
               age INTEGER,
               mobile_no INTEGER,
               gender VARCHAR(6),
               dose INTEGER
               )''')


print("Table created successfully")




@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/enterdata')
def new_data():
    return render_template('covid.html')


@app.route('/insertdata', methods=['POST','GET'])
def insertdata():
 
    msg = ""
    if request.method == 'POST':
        
        try:
            adhar_no = request.form['adhar_no']
            name = request.form['name']
            address = request.form['address']
            age = request.form['age']
            mobile_no = request.form['mobile_no']
            gender = request.form['gender']
            dose = request.form['dose']
            with sqlite3.connect('Aadhar_detail.db') as conn:
             cursor = conn.cursor()
            # Inserting values
             cursor.execute('''INSERT INTO ADHAR (adhar_no, name, address, age, mobile_no, gender, dose)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (adhar_no, name, address, age, mobile_no, gender, dose))
             conn.commit()
             msg = 'Data added successfully '
        except:
            conn.rollback()
            msg = "Error. Adhar number already exists."
            
        finally:
           # return render_template("result.html", msg=msg)
           print("msg value:", msg)
           return render_template("result.html", msg=msg)

@app.route('/enteradharno')
def enter_aadhar():
   return render_template('enter_aadhar.html')

  
@app.route('/viewcontent')
def viewcontent():
   return render_template('viewdata.html')
  

@app.route('/viewdata',methods=['POST'])
def viewdata():
    adhar_no = request.form['adhar_no']
    conn = sqlite3.connect('Aadhar_detail.db')
    conn.row_factory= sqlite3.Row
    cursor = conn.cursor() 
    cursor.execute('SELECT * FROM ADHAR WHERE adhar_no = ?', (adhar_no,))
    result = cursor.fetchone()
    return render_template("viewdata.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)
