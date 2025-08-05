import configparser
import json
import sqlite3
import logging
from flask import Flask, jsonify



# ------------------------------
# Configuration
# ------------------------------

CONFIG_FILE = "config.ini"       # Path to the .ini configuration file
DB_FILE = "config_data.db"       # SQLite database file

# ------------------------------
# Logging Setup
# ------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# ------------------------------
# Initialize Flask App
# ------------------------------
app = Flask(__name__)

# ------------------------------
# Function: Parse Configuration File
# ------------------------------
def parse_config(file_path):

    """
    Parses the given .ini configuration file and returns data as a dictionary.
    
    Args:
        file_path (str): Path to the configuration file.

    Returns:
        dict: Parsed configuration data.
    """
        
    config=configparser.ConfigParser()
    parsed_data = {}

    try:
        config.read(file_path)
        for section in config.sections():
            parsed_data[section] = dict(config[section])
        logging.info("Configuration file parsed successfully.")
        return parsed_data
    except FileNotFoundError:
        logging.error("Configuration file not found.")
    except Exception as e:
        logging.exception(f"Error reading configuration file: {e}")
    
    return {}

# ------------------------------
# Function: Save Config Data to SQLite DB
# ------------------------------

def save_to_db(data):
    """
    Saves the parsed configuration dictionary into an SQLite database in JSON format.

    Args:
        data (dict): Parsed configuration data.
    """

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        #Create Table if does not exist

        cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS config_data (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       json_data TEXT NOT NULL
            )
    ''')
        
        # Clear previous entries (optional - for simplicity)
        cursor.execute("DELETE FROM config_data")

         # Insert new data
        json_string = json.dumps(data)
        cursor.execute("INSERT INTO config_data (json_data) VALUES (?)", (json_string,))

        conn.commit()
        conn.close()
        logging.info("Configuration data saved to SQLite database.")


    except sqlite3.Error as db_error:
        logging.error(f"SQLite database error: {db_error}")
    except Exception as e:
        logging.exception(f"Unexpected error while saving to DB: {e}")



# ------------------------------
# API Endpoint: GET /config
# ------------------------------

@app.route('/config', methods=['GET'])
def get_config():

    """
    GET endpoint to retrieve the latest configuration data from the database.

    Returns:
        JSON response containing config data or an error message.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT json_data FROM config_data ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if row:
            logging.info("Configuration data retrieved successfully from database.")
            return jsonify(json.loads(row[0]))
        else:
            logging.warning("No Configuration data found in the database. ")
            return jsonify({"error": "No configuration found. "}), 404
        
    except Exception as e:
        logging.exception("Failed to fetch configuration from database.")
        return jsonify({"error": f"Failed to fetch configuration: {str(e)}"}), 500
        
# ------------------------------
# Main Script Execution
# ------------------------------

if __name__ == "__main__":
    logging.info("Starting configuration parser... ")

    # Step 1: Parse the configuration file
    config_data = parse_config(CONFIG_FILE)

    if config_data:
        # Step 2: Log parsed data
        logging.info("Parsed configuration data: ")
        for section, items in config_data.items():
            logging.info(f"[{section}]")
            for key, value in items.items():
                logging.info(f"{key} = {value}")

        # Step 3: Save the data to the database
            save_to_db(config_data)

        # Step 4: Run the Flask app
        logging.info("Starting Flask API server at http://localhost:5000/config")
        app.run(debug=True)
    else:
        logging.error("No valid configuration data to process. Exiting.")

