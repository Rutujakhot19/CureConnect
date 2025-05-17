from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import math
import MySQLdb.cursors
app = Flask(__name__)
app.secret_key = 'ssccxxaass'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'doctors_db'


mysql = MySQL(app)
bcrypt = Bcrypt(app)


def haversine(lat1, lon1, lat2, lon2):
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    R = 6371  
    phi1 = math.radians(lat1)  
    phi2 = math.radians(lat2) 
    delta_phi = math.radians(lat2 - lat1)  
    delta_lambda = math.radians(lon2 - lon1)  

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c  
    return distance


@app.route('/')
def main_front_page():
    return render_template('main_front_page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']

        cur = mysql.connection.cursor()
        try:
            query = """
                SELECT * FROM users 
                WHERE username = %s OR email = %s OR phone = %s
            """
            cur.execute(query, (identifier, identifier, identifier))
            user = cur.fetchone()

            if user:
                stored_password = user[6]  

                if bcrypt.check_password_hash(stored_password, password):
                    session['user_id'] = user[0] 
                    return redirect(url_for('main_front_page')) 
                else:
                    error = "Invalid credentials. Incorrect password."
            else:
                error = "User not found. Please sign up first." 

        except Exception as e:
            error = f"An error occurred during login: {e}" 
        finally:
            cur.close()

    return render_template('login.html', error=error) 


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        phone = request.form['phone']
        dob = request.form['dob']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        # Check if username already exists
        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cur.fetchone()
            if existing_user:
                error = "Username already exists." 
            else:
                # Insert data into database
                query = """
                    INSERT INTO users (name, email, username, phone, dob, password)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cur.execute(query, (name, email, username, phone, dob, password))
                mysql.connection.commit()
                return redirect(url_for('login')) 
        except Exception as e:
            error = f"Error during registration: {e}"
        finally:
            cur.close()

    return render_template('register.html', error=error)


@app.route('/appointment/<int:doctor_id>', methods=['GET', 'POST'])
def appointment_form(doctor_id):
    if request.method == 'POST':
        return redirect(url_for('pay_page', doctor_id=doctor_id))  
    return render_template('appointment_form.html', doctor_id=doctor_id)


@app.route('/doctors-list/<int:hospital_id>')
def doctor_list(hospital_id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id, name, specialization, rating FROM doctors_table WHERE hospital_id = %s', (hospital_id,))
    doctors = cursor.fetchall()
    doctors = [(doctor[0], doctor[1], doctor[2], int(doctor[3]) if doctor[3] is not None else None) for doctor in doctors]
    cursor.close()
    return render_template('doctors_list.html', doctors=doctors)


@app.route('/hospital-list')
def hospital_list():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id, name, city, rating, latitude, longitude FROM hospitals')
    hospitals = cursor.fetchall()
    cursor.close()
    hospitals_data = [(hospital[0], hospital[1], hospital[2], int(round(hospital[3])), hospital[4], hospital[5]) 
                      for hospital in hospitals]
    return render_template('hospital_list.html', hospitals=hospitals_data)


@app.route('/pay-page/<int:doctor_id>', methods=['GET', 'POST'])
def pay_page(doctor_id):
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        contact = request.form['contact']
        email = request.form['email']
        appointment_date = request.form['appointment_date']
        payment_mode = request.form['payment_mode']
        
    if request.method == 'GET':
        return render_template('success.html')
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT doctors_table.id,doctors_table.name, hospitals.name, hospitals.city, '
                   'doctors_table.rating,doctors_table.appointment_price,doctors_table.upi_id'
                   ' FROM hospitals INNER JOIN doctors_table ON hospitals.id = doctors_table.hospital_id '
                   'WHERE doctors_table.id = %s', (doctor_id,))
    doctor = cursor.fetchall()
    cursor.execute('INSERT INTO appointments (user_id,doctor_id,apt_date,name,address) VALUES (%s,%s,%s,%s,%s);',(session['user_id'],doctor[0][0],appointment_date,name,address))
    mysql.connection.commit()
    cursor.close()

    if doctor:
        doctor_info = doctor[0][0:]
        return render_template('pay_page.html', doctor_info=doctor_info,appointment_date=appointment_date)  # Pass doctor_info to template
    else:
        return render_template('pay_page.html', error="Doctor not found.")


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/blood-bank-main-page')
def blood_bank_main_page():
    user_latitude = float(request.args.get('latitude', 0))  
    user_longitude = float(request.args.get('longitude', 0))  

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id, name, location, phone_number, timing, latitude, longitude FROM blood_bank')
    blood_banks = cursor.fetchall()
    cursor.close()

    nearby_blood_banks = []

    for bank in blood_banks:
        bank_id, name, location, phone_number, timing, lat, lon = bank
        
        lat = float(lat)
        lon = float(lon)
        
        distance = haversine(user_latitude, user_longitude, lat, lon)

        if distance <= 50:  
            nearby_blood_banks.append({
                'id': bank_id,
                'name': name,
                'location': location,
                'phone_number': phone_number,
                'timing': timing,
                'distance': round(distance, 2)
            })

    return render_template('blood_bank_main_page.html', blood_banks=nearby_blood_banks)


@app.route('/blood-donate-location')
def blood_donate_location():
    latitude = float(request.args.get('latitude', 0))
    longitude = float(request.args.get('longitude', 0))

    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT id, name, location, phone_number, timing, latitude, longitude FROM blood_bank''')
    blood_banks = cursor.fetchall()
    cursor.close()

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371 
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c  

    nearby_blood_banks = []

    for bank in blood_banks:
        bank_id, name, location, phone_number, timing, lat, lon = bank
        distance = haversine(latitude, longitude, float(lat), float(lon))

        if distance <= 50:  
            nearby_blood_banks.append({
                'id': bank_id,
                'name': name,
                'location': location,
                'phone_number': phone_number,
                'timing': timing,
                'distance': round(distance, 2)  
            })

    return render_template('blood_donate_location.html', blood_banks=nearby_blood_banks)


@app.route('/blood-grp')
def blood_grp():
    user_latitude = float(request.args.get('latitude', 0))
    user_longitude = float(request.args.get('longitude', 0))

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id, name, location, phone_number, timing, latitude, longitude FROM blood_bank')
    blood_banks = cursor.fetchall()

    blood_bank_data = []

    for bank in blood_banks:
        bank_id, name, location, phone_number, timing, lat, lon = bank
        cursor.execute('SELECT blood_group FROM blood_inventory WHERE blood_bank_id = %s', (bank_id,))
        available_groups = cursor.fetchall()
        available_groups_list = [group[0] for group in available_groups]  

        blood_bank_data.append({
            'id': bank_id,
            'name': name,
            'location': location,
            'phone_number': phone_number,
            'timing': timing,
            'available': available_groups_list,
            'latitude': lat,
            'longitude': lon
        })

    cursor.close()

    nearby_blood_banks = []

    for bank in blood_bank_data:
        distance = haversine(user_latitude, user_longitude, bank['latitude'], bank['longitude'])
        if distance <= 50:
            nearby_blood_banks.append(bank)

    return render_template('blood_grp.html', blood_banks=nearby_blood_banks)


@app.route('/blood-receive-location/<int:blood_bank_id>')
def blood_receive_location(blood_bank_id):
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT bb.name, bb.location, bb.phone_number, bb.timing, bi.blood_group, bi.quantity
        FROM blood_bank bb
        LEFT JOIN blood_inventory bi ON bb.id = bi.blood_bank_id
        WHERE bb.id = %s
    ''', (blood_bank_id,))
    blood_info = cursor.fetchall()
    cursor.close()

    if not blood_info:
        return "Blood bank not found", 404

    blood_bank = {
        'name': blood_info[0][0],
        'location': blood_info[0][1],
        'phone_number': blood_info[0][2],
        'timing': blood_info[0][3],
        'available_blood_groups': []
    }

    for row in blood_info:
        blood_group = row[4]
        quantity = row[5]
        blood_bank['available_blood_groups'].append(f'{blood_group}: {quantity} units')

    return render_template('blood_receive_location.html', blood_bank=blood_bank)


@app.route('/list_hospital')
def list_hospital():
    import math

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0  
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance

    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)

    if not latitude or not longitude:
        return render_template('list_hospital.html', error_message="Location not provided, please allow geolocation.")

    cursor = mysql.connection.cursor()
    cursor.execute(''' 
        SELECT hb.hospital_id, hb.hospital_name, hb.location, 
               ba.available_general_beds + ba.available_icu_beds + ba.available_private_rooms AS available_beds, 
               hb.latitude, hb.longitude, hb.contact_number
        FROM hospitals_bed hb
        INNER JOIN bed_availability ba ON hb.hospital_id = ba.hospital_id
    ''')
    hospitals = cursor.fetchall()

    nearby_hospitals = []
    for hospital in hospitals:
        distance = haversine(latitude, longitude, hospital[4], hospital[5])  
        
        if distance <= 50:
            nearby_hospitals.append({
                'hospital_id': hospital[0],  
                'hospital_name': hospital[1], 
                'location': hospital[2],  
                'available_beds': hospital[3],  
                'contact_number': hospital[6],  
                'latitude': hospital[4],  
                'longitude': hospital[5],  
                'distance': round(distance, 2)  
            })
    
    cursor.close()

    return render_template('list_hospital.html', hospitals=nearby_hospitals, error_message=None)


@app.route('/Bed-Status/<int:hospital_id>')
def BedStatus(hospital_id):
    def haversine(lat1, lon1, lat2, lon2):
        from math import radians, sin, cos, sqrt, atan2

        R = 6371.0  
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT hb.hospital_name, hb.location, hb.latitude, hb.longitude, hb.contact_number, 
               ba.available_general_beds, ba.available_icu_beds, ba.available_private_rooms
        FROM hospitals_bed hb
        INNER JOIN bed_availability ba ON hb.hospital_id = ba.hospital_id
        WHERE hb.hospital_id = %s
    ''', (hospital_id,))
    bed_status = cursor.fetchone()
    cursor.close()

    if not bed_status:
        return render_template('error.html', message="Hospital not found"), 404

    hospital_info = {
        'hospital_name': bed_status[0],
        'location': bed_status[1],
        'latitude': bed_status[2],
        'longitude': bed_status[3],
        'contact_number': bed_status[4]
    }
    beds_info = {
        'general_beds': bed_status[5],
        'icu_beds': bed_status[6],
        'private_rooms': bed_status[7]
    }

    user_latitude = float(request.args.get('latitude', 0))
    user_longitude = float(request.args.get('longitude', 0))
    distance_to_user = haversine(user_latitude, user_longitude, hospital_info['latitude'], hospital_info['longitude'])

    google_maps_api_key = "YOUR_SECURE_API_KEY"

    return render_template(
        'BedStatus.html',
        hospital=hospital_info,
        beds=beds_info,
        google_maps_api_key=google_maps_api_key,
        distance=round(distance_to_user, 2)
    )


@app.route('/hospital-list-rating')
def hospital_list_rating():
    user_id = session.get('user_id')
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT  patient_history.id,hospitals.name,doctors_table.name,patient_history.visit_date
        FROM patient_history
        INNER JOIN hospitals ON hospitals.id = patient_history.hospital_id
        INNER JOIN doctors_table ON doctors_table.id = patient_history.doctor_id
        WHERE patient_history.user_id=%s
        ORDER BY patient_history.visit_date DESC;
    ''', (user_id,))
    patient_history = cursor.fetchall()
    cursor.close()
    return render_template('hospital_list_rating.html',hospitals=patient_history)


@app.route('/Doctor-info/<int:id>')
def Doctor_info(id):
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT  hospitals.name,doctors_table.name,patient_history.diagnostis,patient_history.medicines
        FROM patient_history
        INNER JOIN hospitals ON hospitals.id = patient_history.hospital_id
        INNER JOIN doctors_table ON doctors_table.id = patient_history.doctor_id
        WHERE patient_history.id=%s;
    ''', (id,))
    patient_history = cursor.fetchall()
    cursor.close()
    return render_template('Doctor_info.html',hospitals=patient_history)


@app.route('/rating-and-feedback')
def rating_and_feedback():
    return render_template('rating_and_feedback.html')


@app.route('/Hospital-list-patient-history')
def Hospital_list_patient_history():
    user_id = session.get('user_id')
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT  patient_history.id,hospitals.name,doctors_table.name,patient_history.visit_date
        FROM patient_history
        INNER JOIN hospitals ON hospitals.id = patient_history.hospital_id
        INNER JOIN doctors_table ON doctors_table.id = patient_history.doctor_id
        WHERE patient_history.user_id=%s;
    ''', (user_id,))
    patient_history = cursor.fetchall()
    cursor.close()
    return render_template('Hospital_list_patient_history.html',hospitals=patient_history)


@app.route('/Patient-info/<int:id>')
def Patient_info(id):
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT  hospitals.name,doctors_table.name,patient_history.diagnostis,patient_history.medicines
        FROM patient_history
        INNER JOIN hospitals ON hospitals.id = patient_history.hospital_id
        INNER JOIN doctors_table ON doctors_table.id = patient_history.doctor_id
        WHERE patient_history.id=%s;
    ''', (id,))
    patient_history = cursor.fetchall()
    cursor.close()
    return render_template('Patient_info.html',hospitals=patient_history)


@app.route('/get_ride')
def get_ride():
    return render_template('get_ride.html')


@app.route('/book_ride', methods=['POST'])
def book_ride():
    user_id = session.get('user_id')
    data = request.get_json()
    user_latitude = float(data.get('latitude'))
    user_longitude = float(data.get('longitude'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    try:
        cursor.execute('''SELECT * FROM user_driver WHERE user_id = %s AND is_complete = 0''', (user_id,))
        old_entry = cursor.fetchone()
        if old_entry is None:
            cursor.execute('''INSERT INTO notify (user_id, latitude, longitude, is_active)
                            VALUES (%s, %s, %s, %s)''', (user_id, user_latitude, user_longitude, 1))
            mysql.connection.commit()
            
        return jsonify({
                'message': 'Finding Ride !',
                'status': 'Confirmed'
            })
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({
            'message': f'Error occurred while booking the ride: {str(e)}',
            'status': 'Error'
        })
    
    finally:
        cursor.close()

@app.route('/show_ride', methods=['POST'])
def show_ride():
    try:
        user_id = session.get('user_id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''SELECT * FROM user_driver WHERE user_id = %s AND is_complete = 0''', (user_id,))
        newentry = cursor.fetchone()
        driver_id=newentry['driver_id']
        cursor.execute('''SELECT * FROM drivers WHERE id = %s''', (driver_id,))
        driver = cursor.fetchone()
        return jsonify({
                'message': 'Ride booked successfully!',
                'status': 'Confirmed',
                'driver_name':driver['name'],
                'driver_num':driver['phone']
            })
    except TypeError:
        mysql.connection.rollback()
        return jsonify({
            'message': 'Not Accepted Yet / Not Yet Tried to Book',
            'status': 'Error'
        })
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({
            'message': f'Error occurred while booking the ride: {str(e)}',
            'status': 'Error'
        })
    
    finally:
        cursor.close()
if __name__ == '__main__':
    app.run(debug=True,port=4000)