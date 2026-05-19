from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import bcrypt
import re
import os

app = Flask(__name__)
app.secret_key = 'healthcare_secret_key'
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5000 per day", "2000 per hour"]
)

# Feature update branch

# MySQL Configuration

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')

mysql = MySQL(app)

# Input Sanitisation Function

def is_valid_input(value):
    return re.match(r'^[a-zA-Z0-9 @._-]+$', value)

# Home Route

@app.route('/')
def home():
    return render_template('index.html')

# Login Route

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

	# Input Sanitisation

        if not is_valid_input(email):
            return """
	    <script>
            	alert('Invalid input detected');
            	window.location.href = '/login';
            </script>
            """

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cur.fetchone()

        cur.close()

        if user:
            
            if user[5] == 'disabled':

                return """
                <script>
                    alert('Your account has been disabled by admin.');
                    window.location.href = '/login';
                </script>
                """

            stored_password = user[3]

            if bcrypt.checkpw(
                password.encode('utf-8'),
                stored_password.encode('utf-8')
            ):

                session['user_email'] = email
                session['role'] = user[4]

                if session['role'] == 'admin':
                    return redirect('/admin')

                return redirect('/dashboard')

            else:
                return """
                <script>
                    alert('Invalid Email or Password');
                    window.location.href = '/login';
                </script>
                """
        else:
            return """
            <script>
                alert('Invalid Email or Password');
                window.location.href = '/login';
            </script>
            """
    return render_template('login.html')

# Register Route

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']

        hashed_password = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
        )

        cur = mysql.connection.cursor()

        cur.execute(
            "INSERT INTO users(fullname, email, password) VALUES(%s, %s, %s)",
            (fullname, email, hashed_password)
        )

        mysql.connection.commit()

        cur.close()

        return """
        <script>
            alert('Registration Successful!');
            window.location.href = '/login';
        </script>
        """

    return render_template('register.html')

#dashboard route

@app.route('/dashboard')
def dashboard():

    if 'user_email' not in session:
        return redirect('/login')

    return render_template('dashboard.html')

#appointment route

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():

    if 'user_email' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    # Fetch doctors

    cur.execute("SELECT * FROM doctors")

    doctors = cur.fetchall()

    if request.method == 'POST':

        patient_name = request.form['patient_name']
        doctor_name = request.form['doctor_name']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        symptoms = request.form['symptoms']

        cur.execute(
            """
            INSERT INTO appointments
            (patient_name, doctor_name, appointment_date, appointment_time, symptoms, user_email)

            VALUES(%s, %s, %s, %s, %s, %s)
            """,
            (
                patient_name,
                doctor_name,
                appointment_date,
                appointment_time,
                symptoms,
                session['user_email']
            )
        )

        mysql.connection.commit()

        cur.close()

        return """
        <script>
            alert('Appointment Booked Successfully!');
            window.location.href = '/dashboard';
        </script>
        """

    cur.close()

    return render_template(
        'appointment.html',
        doctors=doctors
    )

# History Route
@app.route('/history')
def history():

    if 'user_email' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM appointments WHERE user_email=%s",
        (session['user_email'],)
    )

    appointments = cur.fetchall()

    cur.close()

    return render_template(
        'history.html',
        appointments=appointments
    )

# doctor route
@app.route('/doctors')
def doctors():

    if 'user_email' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM doctors")

    doctors = cur.fetchall()

    cur.close()

    return render_template(
        'doctors.html',
        doctors=doctors
    )

# Profile Route
@app.route('/profile', methods=['GET', 'POST'])
def profile():

    if 'user_email' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        fullname = request.form['fullname']

        cur.execute(
            """
            UPDATE users
            SET fullname=%s
            WHERE email=%s
            """,
            (
                fullname,
                session['user_email']
            )
        )

        mysql.connection.commit()

        return """
        <script>
            alert('Profile Updated Successfully!');
            window.location.href = '/profile';
        </script>
        """

    cur.execute(
        "SELECT * FROM users WHERE email=%s",
        (session['user_email'],)
    )

    user = cur.fetchone()

    cur.close()

    return render_template(
        'profile.html',
        user=user
    )

# Notifications Route
@app.route('/notifications')
def notifications():

    if 'user_email' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute(
        """
        SELECT * FROM notifications
        WHERE user_email=%s
        ORDER BY created_at DESC
        """,
        (session['user_email'],)
    )

    notifications = cur.fetchall()

    cur.close()

    return render_template(
        'notifications.html',
        notifications=notifications
    )

# Records Route
@app.route('/records')
def records():

    if 'user_email' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute(
        """
        SELECT * FROM medical_records
        WHERE user_email=%s
        """,
        (session['user_email'],)
    )

    records = cur.fetchall()

    cur.close()

    return render_template(
        'records.html',
        records=records
    )


# Admin Route

@app.route('/admin')
def admin():

    if 'user_email' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return redirect('/dashboard')

    cur = mysql.connection.cursor()

    # Total Users
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    # Total Appointments
    cur.execute("SELECT COUNT(*) FROM appointments")
    total_appointments = cur.fetchone()[0]

    # Total Doctors
    cur.execute("SELECT COUNT(*) FROM doctors")
    total_doctors = cur.fetchone()[0]

    cur.close()

    return render_template(
        'admin.html',
        total_users=total_users,
        total_appointments=total_appointments,
        total_doctors=total_doctors
    )

# Admin Appointments Route
@app.route('/admin/appointments')
def admin_appointments():

    if 'user_email' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return redirect('/dashboard')

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM appointments")

    appointments = cur.fetchall()

    cur.close()

    return render_template(
        'admin_appointments.html',
        appointments=appointments
    )

# Delete Appointment Route
@app.route('/delete_appointment/<int:id>')
def delete_appointment(id):

    if 'user_email' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return redirect('/dashboard')

    cur = mysql.connection.cursor()

    # Get appointment details first

    cur.execute(
        "SELECT * FROM appointments WHERE id=%s",
        (id,)
    )

    appointment = cur.fetchone()

    user_email = appointment[6]
    doctor_name = appointment[2]

    # Insert notification

    message = f"Your appointment with {doctor_name} was cancelled by admin."

    cur.execute(
        """
        INSERT INTO notifications(user_email, message)
        VALUES(%s, %s)
        """,
        (user_email, message)
    )

    # Delete appointment

    cur.execute(
        "DELETE FROM appointments WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    cur.close()

    return """
    <script>
        alert('Appointment Cancelled Successfully!');
        window.location.href = '/admin/appointments';
    </script>
    """

# Admin Users Route
@app.route('/admin/users')
def admin_users():

    if 'user_email' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return redirect('/dashboard')

    cur = mysql.connection.cursor()

    cur.execute(
        """
        SELECT users.fullname,
            users.email,
            users.role,
            users.status,
            COUNT(appointments.id)

        FROM users

        LEFT JOIN appointments
        ON users.email = appointments.user_email

        GROUP BY users.fullname,
                users.email,
                users.role,
                users.status
        """
    )

    users = cur.fetchall()

    cur.close()

    return render_template(
        'admin_users.html',
        users=users
    )

#disable user route
@app.route('/disable_user/<path:email>')
def disable_user(email):

    if 'user_email' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return redirect('/dashboard')

    cur = mysql.connection.cursor()

    cur.execute(
        """
        UPDATE users
        SET status='disabled'
        WHERE email=%s
        """,
        (email,)
    )

    mysql.connection.commit()

    cur.close()

    return """
    <script>
        alert('User Disabled Successfully!');
        window.location.href='/admin/users';
    </script>
    """

#enable user route
@app.route('/enable_user/<path:email>')
def enable_user(email):

    if 'user_email' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return redirect('/dashboard')

    cur = mysql.connection.cursor()

    cur.execute(
        """
        UPDATE users
        SET status='active'
        WHERE email=%s
        """,
        (email,)
    )

    mysql.connection.commit()

    cur.close()

    return """
    <script>
        alert('User Enabled Successfully!');
        window.location.href='/admin/users';
    </script>
    """

# Admin Records Route
@app.route('/admin/records')
def admin_records():

    if 'user_email' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return redirect('/dashboard')

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM medical_records ORDER BY visit_date DESC"
    )

    records = cur.fetchall()

    cur.close()

    return render_template(
        'admin_records.html',
        records=records
    )

# Admin Doctors Route
@app.route('/admin/doctors')
def admin_doctors():

    if 'user_email' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return redirect('/dashboard')

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM doctors")

    doctors = cur.fetchall()

    cur.close()

    return render_template(
        'admin_doctors.html',
        doctors=doctors
    )

# Add Doctors Route
@app.route('/admin/add_doctor', methods=['GET', 'POST'])
def add_doctor():

    if 'user_email' not in session:
        return redirect('/login')

    if session['role'] != 'admin':
        return redirect('/dashboard')

    if request.method == 'POST':

        doctor_name = request.form['doctor_name']
        specialization = request.form['specialization']
        experience = request.form['experience']
        availability = request.form['availability']

        cur = mysql.connection.cursor()

        cur.execute(
            """
            INSERT INTO doctors
            (doctor_name, specialization, experience, availability)

            VALUES(%s, %s, %s, %s)
            """,
            (
                doctor_name,
                specialization,
                experience,
                availability
            )
        )

        mysql.connection.commit()

        cur.close()

        return """
        <script>
            alert('Doctor Added Successfully!');
            window.location.href='/admin/doctors';
        </script>
        """

    return render_template('add_doctor.html')

# Logout Route
@app.route('/logout')
def logout():

    session.clear()

    return """
    <script>
        alert('Logged Out Successfully!');
        window.location.href = '/login';
    </script>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
