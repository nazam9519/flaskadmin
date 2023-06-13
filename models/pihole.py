from flask import Blueprint
from flask import jsonify
from flask import request
import os
from flask import Blueprint
from flask import jsonify
from flask import request
from flask.logging import default_handler
import subprocess 
import signal
import shutil
import logging

phole_c = Blueprint('pihole',__name__)
pipath = os.environ['PICONFIG']
bkpath = os.environ['PVM']
d = logging.getLogger('flask_app')

@phole_c.route('/dns',methods=['POST'])
def pi_dns():
    data = request.json
    if request.args.get('ip') and request.args.get('dnsname'):
        data = {'ip':request.args['ip'],'dnsname':request.args['dnsname']}
    elif not data or not 'ip' in data or not 'dnsname' in data:
        return 'no parameters or body',404
    shutil.copyfile(f'{pipath}/custom.list',f'{bkpath}/custom.list.old')
    with open(f'{bkpath}/custom.list','a') as newentry:
        newentry.write(f"{data['ip']} {data['dnsname']}")
    return jsonify({'msg':'success!'})
