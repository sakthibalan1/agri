from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def update_database(temperature, humidity, moisture):
    try:

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sensors"
        )

        if connection.is_connected():

            cursor = connection.cursor()

            query = "INSERT INTO sensor_data (timestamp, temperature, humidity, moisture) VALUES (NOW(), %s, %s, %s);"
            
            cursor.execute(query, (temperature, humidity, moisture))

            connection.commit()

            print("Data inserted successfully into the database.")

    except mysql.connector.Error as error:
        print("Error while connecting to MySQL database:", error)

    finally:

        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/values', methods=['POST'])
def receive_sensor_values():
    data = request.json
    if 'temperature' in data and 'humidity' in data and 'moisture' in data:
        temperature = data['temperature']
        humidity = data['humidity']
        moisture = data['moisture']
        
        update_database(temperature, humidity, moisture)

        return jsonify({"message": "Sensor values received and updated in the database."}), 200
    else:
        return jsonify({"error": "Invalid JSON data. Expected 'temperature', 'humidity', and 'moisture' keys."}), 400

if __name__ == '__main__':
    app.run()
