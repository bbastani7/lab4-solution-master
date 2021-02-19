# Time keeping
import time

# Import MySQL Connector Driver
import mysql.connector as mysql

# Import tello
from tellolib import Tello

# Load the DB credentials
import os
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

# At most, send a command every COMMAND_DELAY seconds
COMMAND_DELAY = 1

heart_beat_freq = 10

""" Main Entrypoint """
if __name__ == "__main__":

  # Wait until the database is ready to establish a connection, checking it every second
  while(True):
    try:
      db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
      cursor = db.cursor()
      break
    except:
      time.sleep(1)

  # Create Tello connection
  drone = Tello()

  # Enter into the main event loop
  before = time.time()
  time_last_command_sent = time.time()
  while(True):
    now = time.time()
    if(now - before > COMMAND_DELAY):
      before = now

      # Get the most recent command
      cursor.execute("select * from Commands where completed=0 limit 1;")
      response = cursor.fetchone()
      db.commit()

      # Check if there was a command in the queue
      if response is not None:

        time_last_command_sent = now
        print("DEBUG: Command received (dispatcher): ", response)

        ########################################
        # INSERT DRONE CONTROL COMMANDS HERE
        ########################################
        drone.send_command(response[1])

        # Mark the command as completed
        cursor.execute("update Commands set completed=1 where id=%s" % response[0])
        db.commit()

      # Else, if time since last command > 10s, query battery to keep connection
      else:
        print("DEBUG: No commands in database queue (dispatcher)")
        if(now - time_last_command_sent > heart_beat_freq):
          print("DEBUG: Query battery level to keep connection (dispatcher)")
          drone.send_command("battery?")
          time_last_command_sent = now