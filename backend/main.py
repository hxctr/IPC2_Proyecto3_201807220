from flask import Flask, request
from manage import Manager
from flask.json import jsonify
from xml.etree import ElementTree as ET

import sys

manager = Manager()

app = Flask(__name__)

@app.route('/')
def index():
    return "API with Flask is working good"

@app.route('/add', methods=['POST'])
def adding_bill():
    
    xml = request.data.decode('utf-8')
    root = ET.XML(xml)
    
    for element in root:
        for subelement in element.iter('DTE'):
            date= str(subelement.find('TIEMPO').text.strip())
            reference = str(subelement.find('REFERENCIA').text.strip())
            sender_nit = str(subelement.find('NIT_EMISOR').text.strip())
            receiver_nit = str(subelement.find('NIT_RECEPTOR').text.strip())
            value = str(subelement.find('VALOR').text.strip())
            iva  = str(subelement.find('IVA').text.strip())
            total = str(subelement.find('TOTAL').text.strip())

            manager.add_bill(date, reference, sender_nit, receiver_nit, value, iva, total)
    return jsonify({'ok': True,'msg':'Data sent successfully'}), 200

@app.route('/send', methods=['GET'])
def send_data():
    manager.get_authorization()
    return jsonify({'msg':'File succesfully created'}), 200

@app.route('/reset', methods=['GET'])
def reset_data():
    manager.reset_authorization()
    return jsonify({'ok':True,'msg':'File successfully reset'}), 200


@app.route('/showall', methods=['GET'])
def get_bills():
    bills = manager.get_bills()
    return jsonify(bills), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)