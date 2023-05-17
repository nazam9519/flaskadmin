#!/usr/bin/python3.9
from flask import Flask
from flask import jsonify
from models.admin import admin_c
from  modules.setlogs import setlogger
import logging

logger = setlogger("flask_app",logging.DEBUG)
app = Flask(__name__)
app.register_blueprint(admin_c,url_prefix='/admin')
app.logger.debug("init complete...")
app.run(host='0.0.0.0', port=105,debug=True)#,ssl_context='adhoc')
