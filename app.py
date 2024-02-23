from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL configurations
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'smart-campus'
}

Toddate = ""

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    date = request.args.get('date')
    block = request.args.get('block')
    if date and block:
        try:
            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM classrooms WHERE date = %s"
            cursor.execute(query, (date,))
            bookings = cursor.fetchall()
            cursor.close()
            connection.close()
            booked_rooms = [101, 103, 105]
            return render_template('dashboard.html', date=date, bookings=get_booked_rooms())
        except mysql.connector.Error as error:
            return str(error)
    return render_template('dashboard.html', date=None, bookings=None)

@app.route('/submit_login', methods=['POST'])
def submit_login():
    Toddate = request.form['date']
    block = request.form['block']
    return redirect(url_for('dashboard', date=Toddate))

@app.route('/book_room', methods=['POST'])
def book_room():
    try:
        connection = mysql.connector.connect(host="localhost",user="root",password="",database="smart-campus")
        cursor = connection.cursor()

        staff_name = request.form.get('staffName')
        dept_name = request.form.get('deptName')
        start_time = request.form.get('startTime')
        end_time = request.form.get('endTime')
        date = Toddate
        room_number = request.form.get('roomNumber')

        print(f"Staff Name: {staff_name}")
        print(f"Department: {dept_name}")
        print(f"Date: {date}")
        print(f"Start Time: {start_time}")
        print(f"End Time: {end_time}")
        print(f"Room Number: {room_number}")

        # Insert the booking details into the classrooms table
        insert_query = "INSERT INTO classrooms (room_name, class_name, date, start_time, end_time, booked_by) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (room_number, dept_name, date, start_time, end_time, staff_name,))

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'success': True, 'message': 'Room booked successfully'})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_booked_rooms')
def get_booked_rooms():
    try:
        connection = mysql.connector.connect(host="localhost",user="root",password="",database="smart-campus")
        cursor = connection.cursor()
        cursor.execute("SELECT room_name FROM classrooms")  # Adjust your SQL query as needed
        booked_rooms = []
        for i in cursor.fetchall():
            booked_rooms.append(int(i[0]))
        cursor.close()
        connection.close()
        print(booked_rooms)
        return booked_rooms
    except Exception as e:
        return []


if __name__ == '__main__':
    app.run(debug=True)
