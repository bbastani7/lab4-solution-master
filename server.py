# Pyramid Imports
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.response import Response

# Import MySQL Connector Driver
import mysql.connector as mysql

# Load the DB credentials
import os
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

# Valid commands from web UI controller
valid_commands = ['takeoff','land','up','down','left','right','back','forward','cw','ccw']


""" Helper Functions """

# A Function to Queue Commands to the MySQL Database
def send_command(command):
  db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
  cursor = db.cursor()
  query = "insert into Commands (message, completed) values (%s, %s)"
  values = (command, "0")
  cursor.execute(query, values)
  db.commit()
  db.close()


""" Routes """

# TEST ROUTE TEST ROUTE TEST ROUTE TEST ROUTE TEST ROUTE
def test(req):
  send_command("test")
  return Response("Command sent (server): 'test'")

# VIEW: Web Controller Route
def web_ui_route(req):
  return render_to_response('templates/web_ui.html', [], request=req)

# REST: Drone Command Route
def drone_command_route(req):
  command = req.matchdict.get('command')
  arg = req.matchdict.get('arg')

  if command not in valid_commands:
    return {'Response (server):':'Invalid command received'}

  # Combine argument with command
  command = command if not arg else command + " " + arg[0]

  print('Sending command: ', command)
  send_command(command)
  return {'Response (server):':'Command sent!'}


""" Main Entrypoint """

if __name__ == '__main__':
  with Configurator() as config:
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')

    # TEST ROUTE TEST ROUTE TEST ROUTE TEST ROUTE TEST ROUTE
    config.add_route('test', '/test')
    config.add_view(test, route_name='test')

    config.add_route('web_ui', '/')
    config.add_view(web_ui_route, route_name='web_ui')

    config.add_route('drone_command', '/drone_command/{command}*arg')
    config.add_view(drone_command_route, route_name='drone_command', renderer='json')

    config.add_static_view(name='/', path='./public', cache_max_age=3600)

    app = config.make_wsgi_app()

  server = make_server('0.0.0.0', 1234, app)
  print('Web server started on: http://0.0.0.0:8000 OR http://localhost:8000')
  server.serve_forever()