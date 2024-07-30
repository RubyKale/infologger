import logging
from flask import Flask, request, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)

def my_logger_setup():
    mylogger = logging.getLogger('my_logger')
    mylogger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')  # Simple formatter
    handler.setFormatter(formatter)
    mylogger.addHandler(handler)# local variable mylogger
    return(mylogger)

def log_request_as_json(request, status_code):
    log_data = {
        "ip_address": request.remote_addr,
        "user_id": "-",  # Placeholder, customize as needed
        "username": "-",  # Placeholder, customize as needed
        "timestamp": datetime.utcnow().strftime('%d/%b/%Y:%H:%M:%S +0000'),
        # The request object in Flask is a global object that contains all the information about the current HTTP request.
        "request_method": request.method,
        "request_url": request.path,
        "protocol": request.environ.get('SERVER_PROTOCOL'),
        "status_code": status_code,
        "response_size_bytes": "-"  # Placeholder, update if needed
    }
    json_log = json.dumps(log_data, indent=4)
    mylogger = my_logger_setup() #local variable
    mylogger.info(json_log)


# def get_git_commit_sha():
#     try:
#         sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')
#     except Exception as e:
#         sha = "N/A"
#     return sha

def get_git_commit_sha():
    try:
        with open('commit_sha.txt', 'r') as f:
            commit_sha = f.read().strip()
    except FileNotFoundError:
        commit_sha = 'N/A'
    return commit_sha


@app.route('/info', methods=['GET', 'POST'])
def get_info():
    # Build response data
    infoResult = {
        'serviceName': "RubyKInfoLog",
        'version': "1.0.0",
        'git_commit_sha': get_git_commit_sha(),
        'environment': {
            'service_port': os.getenv('SERVICE_PORT'),
            #or 'service_port': request.environ.get('SERVER_PORT'), << this is the variables for the request object
            'log_level':os.getenv('LOG_LEVEL') # this is from export command that i used.
        }
    }
    print(request.environ.get('SERVER_PORT'))
    # The request object in Flask is a global object that contains all the information about the current HTTP request.
    log_request_as_json(request, 200)
    return jsonify(infoResult)

if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    log.disabled = True
    service_port = os.getenv('SERVICE_PORT', '8080') # if no port is specified in the enviroment then by default it shal take 8080
    #print("serviceportis" + service_port)
    myport = int(service_port)
    #Effect: By default, Flask listens only on localhost (127.0.0.1), which means the app is only accessible from the machine it’s running on. Setting host to 0.0.0.0 makes the app accessible from any device that can reach the server, not just the local machine.
    app.run(host="0.0.0.0",debug=True, port=myport)
