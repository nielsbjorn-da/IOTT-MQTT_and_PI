import sqlite3


def initialize_db():
    # Initialize connection to DB and create cursor
    connection = sqlite3.connect("SensorValues.db")
    cursor = connection.cursor()

    # Generating tables for obtained values from the SenseHat
    res = cursor.execute("SELECT name FROM sqlite_master WHERE name='temperature'")
    if res.fetchone() is None:
        cursor.execute("CREATE TABLE temperature(t, timestamp, automatic)")

    res = cursor.execute("SELECT name FROM sqlite_master WHERE name='humidity'")
    if res.fetchone() is None:
        cursor.execute("CREATE TABLE humidity(h, timestamp, automatic)")

    res = cursor.execute("SELECT name FROM sqlite_master WHERE name='pressure'")
    if res.fetchone() is None:
        cursor.execute("CREATE TABLE pressure(p, timestamp, automatic)")

    res = cursor.execute("SELECT name FROM sqlite_master WHERE name='colour'")
    if res.fetchone() is None:
        cursor.execute("CREATE TABLE colour(red,green, blue, brightness, timestamp, automatic)")

    return connection, cursor

def close_connection(connection):
    connection.close()

def insert_values_temperature(connection, cursor, temp, timestamp, automatic):
    cursor.execute("""
        INSERT INTO temperature (t, timestamp, automatic) VALUES
            (?, ?, ?)
    """, (temp, timestamp, automatic))

    connection.commit()


def insert_values_humidity(connection, cursor, humi, timestamp, automatic):
    cursor.execute("""
            INSERT INTO humidity (h, timestamp, automatic) VALUES
                (?, ?, ?)
        """, (humi, timestamp, automatic))

    connection.commit()


def insert_values_pressure(connection, cursor, pressure, timestamp, automatic):
    cursor.execute("""
                INSERT INTO pressure (p, timestamp, automatic) VALUES
                    (?, ?, ?)
            """, (pressure, timestamp, automatic))

    connection.commit()


def insert_values_colour(connection, cursor, red, green, blue, brightness, timestamp, automatic):
    cursor.execute("""
                    INSERT INTO colour (red, green, blue, brightness, timestamp, automatic) VALUES
                        (?, ?, ?, ?, ?, ?)
                """, (red, green, blue, brightness, timestamp, automatic))

    connection.commit()
