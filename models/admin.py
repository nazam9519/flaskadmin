from flask import Blueprint
from flask import jsonify
from flask import request
import os
import subprocess 
import signal

admin_c = Blueprint('admin',__name__)

@admin_c.route('/restart',methods=['GET','POST'])
def restart():
    r_type = request.args.get('type')
    if r_type == 'app':
        subprocess.Popen(['sudo','/opt/rest/admin/restart_app.pl',f'{os.getpid()}'])
        return jsonify({'msg':f'restarting app: {os.getpid()} please wait 30 seconds...'})
    elif r_type == 'server':
        output = subprocess.Popen(['/home/nazam/Documents/restart.pl','&'])
        return jsonify({'msg':'restarting server'})
    elif r_type == 'test':
        return jsonify({'msg':'tested!'})
    else:
        return jsonify({'msg':f"unknown admin arg: {r_type}"})
        
@admin_c.route('/shutdown',methods=['GET','POST'])
def shutdown():
    subprocess.Popen(['/opt/rest/admin/stop_app.py',f"{os.getpid()}"])
    #exit
    return jsonify({'msg':'stopping app, please login to the controller to restart'})
