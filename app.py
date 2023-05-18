#!/usr/bin/python3.9
from flask import Flask
from flask import jsonify
from models.admin import admin_c
from  modules.setlogs import setlogger
import modules.init_opts as options
import logging
import sys 

config = None
if len(sys.argv) > 1: 
    config = options.opts(sys.argv[1])
    print(config.port)
else:
    config = options.opts("none")
logger = setlogger("flask_app",config.log_type)
app = Flask(__name__)
app.register_blueprint(admin_c,url_prefix='/admin')
app.logger.debug("init complete...")
app.run(host='0.0.0.0', port=config.port,debug=config.dbg_flag)#,ssl_context='adhoc')
