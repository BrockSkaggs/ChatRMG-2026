import os
from waitress import serve


from app import flask_server

http_port=os.environ.get('HTTP_PLATFORM_PORT')
serve(flask_server, host='127.0.0.1', port=http_port)

"""
if __name__ == '__main__':
    print('starting waitress...')
    # dash_app.run(port=http_port, host='0.0.0.0')
    serve(flask_server, host='0.0.0.0', port=http_port, _quiet=False)
    # serve(flask_server, host='0.0.0.0', port=http_port, threads=8)
    # serve(server, host='0.0.0.0', port=http_port, threads=8) #Dummy apps works as expected
"""