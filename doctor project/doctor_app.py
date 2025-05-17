from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import bcrypt

app = Flask(__name__)
app.secret_key = 'ssccxxaass'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'doctors_db'


mysql = MySQL(app)
Bcrypt = Bcrypt(app)


@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM appointments WHERE doctor_id = %s AND is_complete= 0 AND DATE(apt_date) = CURDATE()", (session['id'],))
    appointments=cursor.fetchall()
    
    return render_template('appointments.html',appointments=appointments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username,password)
        cursor = mysql.connection.cursor()
        
        cursor.execute("SELECT password_hash,doctor_id FROM doctor_login WHERE username = %s", (username,))
        doctor=cursor.fetchone()
        stored_hash = doctor[0]
        dr_id = doctor[1]
        if stored_hash==password:
            session['username'] = username
            session['id']=dr_id
            # print(session['id'])
            # print(f"Session set for hospital user: {session}")  
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials. Please try again.", "danger")
        

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        d_id = request.form['id']
        username = request.form['username']
        password = request.form['password']
        
        if not d_id  or not username or not password:
            flash("All fields are required", "danger")
            return redirect(url_for('register'))
        # Connect to the database
        cursor = mysql.connection.cursor()

        try:
            cursor.execute("SELECT * FROM doctor_login WHERE username = %s OR doctor_id = %s", (username, d_id))

            existing_user = cursor.fetchone()
            print(existing_user)
            if existing_user:
                flash("Username, Id already exists. Please choose a different one.", "danger")
                return redirect(url_for('register'))

            
            cursor.execute(""" 
                    INSERT INTO doctor_login (doctor_id,password_hash,username) 
                    VALUES (%s,%s, %s)
                """, (d_id,username, password))

            mysql.connection.commit()
            flash("Registration successful! You can now log in.", "success")
        except Exception as e:
            mysql.connection.rollback()
            flash(f"Error: {str(e)}", "danger")
        finally:
            cursor.close()

        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/option')
def option():
    appointment_id = request.args.get('id') 
    if not appointment_id:
        return "Appointment ID is missing", 400  
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT id, user_id, doctor_id, apt_date, address, name
        FROM appointments
        WHERE id = %s
    """, (appointment_id,))
    
    appointment = cursor.fetchall()
    cursor.close()

    if not appointment:
        return "Appointment not found", 404
    print(appointment)
    return render_template('option.html', appointment=appointment[0])

@app.route('/history')
def history():
    p_id=request.args.get('id')
    user_id = request.args.get('user')
    
     
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT * FROM patient_history WHERE user_id=%s
    """, (user_id,))
    
    historys = cursor.fetchall()
    cursor.execute("""
        SELECT id, user_id, doctor_id, apt_date, address, name
        FROM appointments
        WHERE id = %s
    """, (p_id,))
    name = cursor.fetchone()[5]
    cursor.close()
    if not historys:
        return "Appointment not found", 404
    return render_template('history.html', historys=historys,name=name)

@app.route('/diagnosis',methods=['GET'])
def diagnosis():
    p_id=request.args.get('id')
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT id, user_id, doctor_id, apt_date, address, name
        FROM appointments
        WHERE id = %s
    """, (p_id,))
    name = cursor.fetchone()[5]
    cursor.close()
    if not name:
        return "Appointment not found", 404
    return render_template('diagnosis.html',name=name,aid=p_id)

@app.route('/submit_diagnosis', methods=['POST'])
def submit_diagnosis():
    pid = request.form.get('id')
    diagnostics = request.form.get('feedback')
    medicines = request.form.get('medicines')
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT id, user_id, doctor_id, apt_date, address, name
        FROM appointments
        WHERE id = %s
    """, (pid,))
    apt = cursor.fetchone()
    did=apt[2]
    cursor.execute("""
        SELECT hospital_id
        FROM doctors_table
        WHERE id = %s
    """, (did,))
    hid = cursor.fetchone()
    
    insert_query = """
        INSERT INTO patient_history (
             user_id, hospital_id, doctor_id, visit_date, diagnostis, medicines
        ) VALUES ( %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(insert_query, (
        apt[1],
        hid,
        did,
        apt[3],
        diagnostics,
        medicines
    ))
    query="""UPDATE appointments SET is_complete = 1 WHERE id = %s"""
    cursor.execute(query, (pid,))
    mysql.connection.commit()
    cursor.close()
    
    print(f"Appointment ID: {pid}")
    print(f"Diagnostics: {diagnostics}")
    print(f"Medicines: {medicines}")
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=8100)
