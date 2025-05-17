from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'ssccxxaass'

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  
        password="admin", 
        database="doctors_db"
    )
    return conn


@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()

        if username == 'admin' and password == 'admin123':
            session['username'] = 'admin' 
            session['user_type'] = 'superuser' 
            print(f"Session set for superuser: {session}")  
            return redirect(url_for('home'))
        
        cursor.execute("SELECT * FROM hospital_users WHERE username = %s AND password = %s", (username, password))
        hospital_user = cursor.fetchone()

        cursor.execute("SELECT * FROM bloodbank_users WHERE username = %s AND password = %s", (username, password))
        bloodbank_user = cursor.fetchone()

        if hospital_user:
            session['username'] = username
            session['user_type'] = 'hospital'  
            print(f"Session set for hospital user: {session}")  
            return redirect(url_for('home'))
        elif bloodbank_user:
            session['username'] = username
            session['user_type'] = 'blood_bank' 
            print(f"Session set for blood bank user: {session}") 
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials. Please try again.", "danger")
        
        conn.close()

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        phone = request.form['phone']
        dob = request.form['dob']
        password = request.form['password']
        user_type = request.form['user_type']  

        if not name or not email or not username or not phone or not dob or not password or not user_type:
            flash("All fields are required", "danger")
            return redirect(url_for('register'))

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            if user_type == 'Hospital User':
                cursor.execute("SELECT * FROM hospital_users WHERE username = %s OR email = %s OR phone = %s", (username, email, phone))
            elif user_type == 'Blood Bank User':
                cursor.execute("SELECT * FROM bloodbank_users WHERE username = %s OR email = %s OR phone = %s", (username, email, phone))

            existing_user = cursor.fetchone()

            if existing_user:
                flash("Username, Email, or Phone already exists. Please choose a different one.", "danger")
                return redirect(url_for('register'))

            if user_type == 'Hospital User':
                cursor.execute(""" 
                    INSERT INTO hospital_users (name, email, username, phone, dob, password) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (name, email, username, phone, dob, password))
            elif user_type == 'Blood Bank User':
                cursor.execute("""
                    INSERT INTO bloodbank_users (name, email, username, phone, dob, password)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (name, email, username, phone, dob, password))

            conn.commit()
            flash("Registration successful! You can now log in.", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error: {str(e)}", "danger")
        finally:
            conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None) 
    return redirect(url_for('home'))

@app.route('/add-hospital', methods=['GET', 'POST'])
def add_hospital():
    if request.method == 'POST':
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            name = request.form['hospital_name']
            city = request.form['city']
            rating = request.form['rating']
            latitude = request.form['lat']
            longitude = request.form['long']

            cursor.execute("INSERT INTO hospitals (name, city, rating, latitude, longitude) VALUES (%s, %s, %s, %s, %s)",
                           (name, city, rating, latitude, longitude))
            conn.commit()

            bb_name = request.form['bb_name']
            bb_location = request.form['bb_location']
            bb_phone = request.form['phone']
            bb_timing = request.form['timing']
            bb_lat = request.form['bb_lat']
            bb_long = request.form['bb_long']

            cursor.execute("INSERT INTO blood_bank (name, location, phone_number, timing, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s) ",
                           (bb_name, bb_location, bb_phone, bb_timing, bb_lat, bb_long))
            conn.commit()

            flash("Hospital and Blood Bank data added successfully!", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error: {str(e)}", "danger")
        finally:
            conn.close()

        return redirect(url_for('add_hospital'))

    return render_template('add_hospital_bloodbank.html')


@app.route('/add-doctor', methods=['GET', 'POST'])
def add_doctor():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM hospitals")
    hospitals = cursor.fetchall()

    if request.method == 'POST':
        try:
            name = request.form['name']
            specialization = request.form['specialization']
            rating = request.form['rating']
            hospital_id = request.form['hospital_id']
            appointment_count = request.form['appointment_count']
            appointment_price = request.form['price']
            upi_id = request.form['upi_id']

            cursor.execute("""
                SELECT id FROM doctors_table WHERE name = %s AND hospital_id = %s
            """, (name, hospital_id))
            existing_doctor = cursor.fetchone()

            if existing_doctor:
                cursor.execute("""
                    UPDATE doctors_table 
                    SET specialization = %s, rating = %s, appointment_count = %s, 
                        appointment_price = %s, upi_id = %s
                    WHERE name = %s AND hospital_id = %s
                """, (specialization, rating, appointment_count, appointment_price, upi_id, name, hospital_id))
            else:
                cursor.execute("""
                    INSERT INTO doctors_table (name, specialization, rating, hospital_id, appointment_count, appointment_price, upi_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (name, specialization, rating, hospital_id, appointment_count, appointment_price, upi_id))
            conn.commit()

            bed_hospital_id = request.form['hospital_id']
            general = request.form['general']
            icu = request.form['icu']
            private = request.form['private']

            cursor.execute("""
                DELETE FROM bed_availability WHERE hospital_id = %s
            """, (bed_hospital_id,))
            
            cursor.execute("""
                INSERT INTO bed_availability (hospital_id, available_general_beds, available_icu_beds, available_private_rooms)
                VALUES (%s, %s, %s, %s)
            """, (bed_hospital_id, general, icu, private))
            conn.commit()

            flash("Doctor and Bed Availability added or updated successfully!", "success")

        except Exception as e:
            conn.rollback()
            flash(f"Error: {str(e)}", "danger")
        finally:
            conn.close()

        return redirect(url_for('add_doctor'))

    return render_template('add_doctor_beds.html', hospitals=hospitals)

@app.route('/blood-stock', methods=['GET', 'POST'])
def blood_stock():
    if request.method == 'POST':
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            blood_bank_name = request.form['blood_bank_name']
            cursor.execute("SELECT id FROM blood_bank WHERE name = %s", (blood_bank_name,))
            blood_bank = cursor.fetchone()
            if not blood_bank:
                flash(f"Blood bank '{blood_bank_name}' not found!", "danger")
                return redirect(url_for('blood_stock'))

            blood_bank_id = blood_bank[0]
            blood_group = request.form['blood_group']
            quantity = request.form['quantity']

            cursor.execute(""" 
                SELECT id FROM blood_inventory 
                WHERE blood_bank_id = %s AND blood_group = %s
            """, (blood_bank_id, blood_group))
            existing_record = cursor.fetchone()

            if existing_record:
                cursor.execute(""" 
                    UPDATE blood_inventory
                    SET quantity = %s
                    WHERE blood_bank_id = %s AND blood_group = %s
                """, (quantity, blood_bank_id, blood_group))
            else:
                cursor.execute(""" 
                    INSERT INTO blood_inventory (blood_bank_id, blood_group, quantity) 
                    VALUES (%s, %s, %s)
                """, (blood_bank_id, blood_group, quantity))

            conn.commit()
            flash("Blood stock added/updated successfully!", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error: {str(e)}", "danger")
        finally:
            conn.close()

        return redirect(url_for('blood_stock'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM blood_bank")
    blood_banks = cursor.fetchall()

    cursor.execute("SELECT bi.id, bb.name AS blood_bank_name, bi.blood_group, bi.quantity FROM blood_inventory bi JOIN blood_bank bb ON bi.blood_bank_id = bb.id")
    blood_data = cursor.fetchall()

    conn.close()

    return render_template('manage_blood_stock.html', blood_banks=blood_banks, blood_data=blood_data)


if __name__ == '__main__':
    app.run(debug=True,port=5010)
