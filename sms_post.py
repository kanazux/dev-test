#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import json
import base64
import binascii
from flask import g, abort, Flask, jsonify, request


ddd = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '21', '22', '24', '27', '28', '31', '32', '33', '34', '35',
       '37', '38', '41', '42', '43', '44', '45', '46', '47', '48', '49', '51', '53', '54', '55', '61', '62', '63', '64',
       '65', '66', '67', '68', '69', '71', '73', '74', '75', '77', '79', '81', '82', '83', '84', '85', '86', '87', '88',
       '89', '91', '92', '93', '94', '95', '96', '97', '98', '99']

def validate_phone(phone):
    """Validate phone numbers."""

    if len(phone) < 12 or len(phone) > 13 or not phone.startswith("55") or phone[2:4] not in ddd:
        return jsonify({"ERROR": {f"{phone}": "Is not a valid phone number."}})
    return True

def validate_user(user):
    """Validate user hash."""

    if isinstance(user, (str)):
        user = user.encode()

    try:
        base64.binascii.a2b_base64(user)
        return True
    except binascii.Error:
        return jsonify({"ERROR": {f"{user}": "Is not a valid base64 hash."}})

def validate_text(text):
    """Validate text message."""

    if len(text) < 3 or len(text) > 140:
        return jsonify({"ERROR": {f"{text}": "Text is great than 140 characters or less than 3"}})
    return True

app = Flask(__name__)
 
@app.route("/smspost", methods=["POST"])
def smspost():
    """Get data to send sms."""

    try:
        errors = {}
        data = json.loads(request.data)
        validate_phone(data['to'])
        validate_phone(data['from'])
        validate_user(data['user'])
        validate_text(data['text'])
    except json.decoder.JSONDecodeError:
        return jsonify({"ERROR": "This data is not a json format."})
    finally:
        error = sys.exc_info()[0]
        if error == None:
            jsonify({"ERROR": "DATA is empty."})
        return jsonify({"ERROR": f"{error}"})

    return jsonify({"Status": "Send"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=False)