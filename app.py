from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from scraper.app_D1 import scraping_D1
from scraper.app_exito import scraping_exito
from scraper.app_Makro import scraping_Makro
from scraper.app_olimpica import scraping_olimpica
import pandas as pd
import os

app = Flask(__name__)
CORS(app)
CSV_DIRECTORY = os.path.join(os.getcwd(), 'data')


@app.route('/scrape/D1', methods=['GET'])
def scrape_d1_endpoint():
    try:
        scraping_D1()
        return jsonify({"message": "D1 scraping completed successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/scrape/Exito', methods=['GET'])
def scrape_exito_endpoint():
    try:
        scraping_exito()
        return jsonify({"message": "exito scraping completed successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/scrape/Makro', methods=['GET'])
def scrape_makro_endpoint():
    try:
        scraping_Makro()
        return jsonify({"message": "Makro scraping completed successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/scrape/Olimpica', methods=['GET'])
def scrape_olimpica_endpoint():
    try:
        scraping_olimpica()
        return jsonify({"message": "Olimpica scraping completed successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/csv/<filename>')
def get_csv(filename):
    return send_from_directory(CSV_DIRECTORY, filename)

if __name__ == '__main__':
    app.run(debug=True)
