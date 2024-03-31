from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

def fetch_last_n_data(column_name, n=5):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sensors"
        )

        if connection.is_connected():
            cursor = connection.cursor()
            n = request.args.get('n', default=5, type=int)
            query = f"SELECT {column_name} FROM sensor_data ORDER BY timestamp DESC LIMIT {n};"

            cursor.execute(query)
            data = cursor.fetchall()

            # Convert fetched data to a list of values
            fetched_data = [record[0] for record in data]

            # Return data as JSON
            return {column_name: fetched_data}

    except mysql.connector.Error as error:
        print("Error while connecting to MySQL database:", error)

    finally:

        if connection.is_connected():
            cursor.close()
            connection.close()

    return {"error": f"Failed to fetch {column_name} data."}

@app.route('/temperature', methods=['GET'])
def temperature():
    return jsonify(fetch_last_n_data("temperature"))

@app.route('/humidity')
def humidity():
    return jsonify(fetch_last_n_data("humidity"))

@app.route('/moisture')
def moisture():
    return jsonify(fetch_last_n_data("moisture"))

@app.route('/all')
def all():
    data1=fetch_last_n_data("moisture")
    data2=fetch_last_n_data("temperature")
    data3=fetch_last_n_data("humidity")
    return jsonify({"moister":data1,"temperature":data2,"humidity":data3})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
