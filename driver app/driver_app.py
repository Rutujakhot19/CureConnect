from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import MySQLdb.cursors
from haversine import haversine, Unit


app = Flask(__name__)

# Configure secret key
app.secret_key = 'ssccxxaass'

# Configure database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'doctors_db'

# Initialize MySQL and Bcrypt
mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    # Redirect to login page by default
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM drivers WHERE email = %s or username = %s', (email,email,))
        driver = cursor.fetchone()
        cursor.close()
        
        if driver and bcrypt.check_password_hash(driver['password'], password):
            session['loggedin'] = True
            session['id'] = driver['id']
            session['email'] = driver['email']
            session['name'] = driver['name']
            session['username'] = driver['username']
            session['is_active'] = driver['is_active']
            
            return redirect(url_for('dashboard'))
        else:
            msg = 'Incorrect email/password!'
    
    return render_template('login.html', msg=msg)



@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form:
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        phone = request.form['phone']
        dob = request.form['dob']
        password = request.form['password']
        
        latitude = 0.0000000
        longitude = 0.0000000
        is_active = True
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM drivers WHERE email = %s', (email,))
        account = cursor.fetchone()
        
        if account:
            msg = 'Account already exists!'
        else:
            cursor.execute('SELECT * FROM drivers WHERE username = %s', (username,))
            account = cursor.fetchone()
            if account:
                msg = 'Username already exists!'
            else:
                cursor.execute('SELECT * FROM drivers WHERE phone = %s', (phone,))
                account = cursor.fetchone()
                if account:
                    msg = 'Phone number already exists!'
                else:
                    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                    
                    try:
                        cursor.execute(
                            'INSERT INTO drivers (name, email, username, phone, dob, password, latitude, longitude, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                            (name, email, username, phone, dob, hashed_password, latitude, longitude, is_active)
                        )
                        mysql.connection.commit()
                        flash('You have successfully registered! Please login to continue.')
                        return redirect(url_for('login'))
                    except Exception as e:
                        msg = f'Registration error: {str(e)}'
    
    return render_template('register.html', msg=msg)

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT is_active FROM drivers WHERE id = %s', (session['id'],))
        driver = cursor.fetchone()
        
        if driver:
            session['is_active'] = driver['is_active']
            
        return render_template('dashboard.html', name=session['name'], username=session['username'], 
                              is_active=session['is_active'])
    return redirect(url_for('login'))



@app.route('/update_location', methods=['POST'])
def update_location():
    if 'loggedin' in session:
        try:
            data = request.get_json()
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            
            # Update location in database
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE drivers SET latitude = %s, longitude = %s WHERE id = %s', 
                         (latitude, longitude, session['id']))
            mysql.connection.commit()
            
            return jsonify({'status': 'success', 'message': 'Location updated successfully'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    return jsonify({'status': 'error', 'message': 'Not logged in'}), 401


@app.route('/update_trips', methods=['POST'])
def update_trips():
    nearby=[]
    if session['is_active']:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM notify',)
        notifications = cursor.fetchall()
        if notifications:
            for notification in notifications:
                if notification['is_active']:
                    distance_km = haversine(
                        (latitude, longitude),
                        (float(notification['latitude']), float(notification['longitude'])),
                        unit=Unit.KILOMETERS
                    )
                    if distance_km < 4000:
                            nearby.append({
                                'id': notification['id'],
                                'name': notification['user_id'],
                                'distance' :distance_km,
                                'latitude': notification['latitude'],
                                'longitude': notification['longitude']
                            })
    return jsonify({'nearby': nearby})

@app.route('/update_status', methods=['POST'])
def update_status():
    if 'loggedin' in session:
        try:
            data = request.get_json()
            is_active = data.get('is_active')
            
            # Update status in database
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE drivers SET is_active = %s WHERE id = %s', 
                         (is_active, session['id']))
            mysql.connection.commit()
            
            # Update session
            session['is_active'] = is_active
            
            return jsonify({'status': 'success', 'message': 'Status updated successfully'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    return jsonify({'status': 'error', 'message': 'Not logged in'}), 401

@app.route('/get_trips', methods=['POST'])
def get_trips():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_driver WHERE is_complete = 0 AND driver_id = %s', (session['id'],))
        trip=cursor.fetchone()
        if trip:
            cursor.execute('SELECT name,phone FROM users WHERE id = %s', (trip['user_id'],))
            customer=cursor.fetchone()
            mysql.connection.commit()
            return jsonify({
                'id' : trip['id'],
                'name': customer['name'],
                'num': customer['phone'],
                'from' : str(trip['latitude']) +"," + str(trip['longitude']),
                'to' : str(trip['driver_lat']) +"," + str(trip['driver_long'])
                })
        return 

@app.route('/accept_trip', methods=['POST'])
def accept_trip():
    if 'loggedin' in session:
        try:
            data = request.get_json()
            n_id=data.get('id')
            user_id = data.get('user_id')
            driver_latitude = data.get('driver_latitude')
            driver_longitude = data.get('driver_longitude')
            trip_latitude = data.get('trip_latitude')
            trip_longitude = data.get('trip_longitude')
            session['is_active']=0
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE drivers SET is_active = 0 WHERE id = %s', (session['id'],))
            cursor.execute('UPDATE notify SET is_active = 0 WHERE id = %s', (n_id,))
            cursor.execute('Insert INTO user_driver (user_id, driver_id, latitude, longitude, driver_lat, driver_long, is_complete) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                                    (user_id,session['id'],trip_latitude,trip_longitude,driver_latitude,driver_longitude,0))
            mysql.connection.commit()
            
            return jsonify({'status': 'success', 'message': 'Status updated successfully'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    return jsonify({'status': 'error', 'message': 'Not logged in'}), 401


@app.route('/start_trip', methods=['POST'])
def start_trip():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_driver WHERE is_complete = 0 AND driver_id = %s', (session['id'],))
        trip=cursor.fetchone()
        cursor.execute('SELECT name FROM users WHERE id = %s', (trip['user_id'],))
        customer=cursor.fetchone()
        mysql.connection.commit()
        return jsonify({
            'id' : trip['id'],
            'name': customer['name'],
            'from' : str(trip['latitude']) +"," + str(trip['longitude']),
            'to' : str(trip['driver_lat']) +"," + str(trip['driver_long'])
            })


@app.route('/completed_trip', methods=['POST'])
def completed_trip():
    if 'loggedin' in session:
        try:
            data = request.get_json()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE drivers SET is_active = 1 WHERE id = %s', (session['id'],))
            cursor.execute('UPDATE user_driver SET is_complete = 1 WHERE id = %s', (data.get('id'),))
            mysql.connection.commit()
            return jsonify({'status': 'success', 'message': 'Status updated successfully'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    return jsonify({'status': 'error', 'message': 'Not logged in'}), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=8010)