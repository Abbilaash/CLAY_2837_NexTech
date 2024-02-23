from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL configurations
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'smart-campus'
}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/hour', methods=['GET', 'POST'])
def hour():
    if request.method == 'POST':
        # Handle form submission for hourly booking
        staff_name = request.form['staff_name']
        representative_name = request.form['representative_name']
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        try:
            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor()

            insert_query = "INSERT INTO hourly_bookings (staff_name, representative_name, date, start_time, end_time) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (staff_name, representative_name, date, start_time, end_time))

            connection.commit()
            cursor.close()
            connection.close()

            return "Hourly booking successful!"
        except Exception as e:
            return str(e)

    return render_template('hour.html')

def check_booking(room_id):
    return False

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', check_booking=check_booking)



if __name__ == '__main__':
    app.run(debug=True)
