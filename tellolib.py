import socket
import threading
import time
from stats import Stats

"""
TODO
1) Remove deque code
2) Remove commands we are no longer using to make this more readable since all of our commands are interfacing only with the "send_command" call
3) Clean up language syntax
4) TEST!
"""

class Tello:
  def __init__(self, tello_ip: str='192.168.10.1', debug: bool=True):
    # Opening local UDP port on 8889 for Tello communication
    self.local_ip = ''
    self.local_port = 8889
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.socket.bind((self.local_ip, self.local_port))

    # Setting Tello ip and port info
    self.tello_ip = tello_ip
    self.tello_port = 8889
    self.tello_address = (self.tello_ip, self.tello_port)
    self.log = []

    # Intializing response thread
    self.receive_thread = threading.Thread(target=self._receive_thread)
    self.receive_thread.daemon = True
    self.receive_thread.start()

    # easyTello runtime options
    self.MAX_TIME_OUT = 15.0
    self.debug = debug

    # Setting Tello to command mode
    self.send_command('command')


  def send_command(self, command: str, query: bool =False):
    # New log entry created for the outbound command
    self.log.append(Stats(command, len(self.log)))

    # Sending command to Tello
    self.socket.sendto(command.encode('utf-8'), self.tello_address)
    # Displaying conformation message (if 'debug' os True)
    if self.debug is True:
      print('Sending command (tellolib): {}'.format(command))
        
    # Checking whether the command has timed out or not (based on value in 'MAX_TIME_OUT')
    start = time.time()
    while not self.log[-1].got_response():  # Runs while no response has been received in log
      now = time.time()
      difference = now - start
      if difference > self.MAX_TIME_OUT:
        print('Connection timed out! (tellolib)')
        break
    # Prints out Tello response (if 'debug' is True)
    if self.debug is True and query is False:
      print('Response (tellolib): {}'.format(self.log[-1].get_response()))
  

  def _receive_thread(self):
    while True:
      # Checking for Tello response, throws socket error
      try:
        self.response, ip = self.socket.recvfrom(1024)
        self.log[-1].add_response(self.response)
      except socket.error as exc:
        print('Socket error (tellolib): {}'.format(exc))

  def wait(self, delay: float):
    # Displaying wait message (if 'debug' is True)
    if self.debug is True:
      print('Waiting {} seconds... (tellolib)'.format(delay))
    # Log entry for delay added
    self.log.append(Stats('wait', len(self.log)))
    # Delay is activated
    time.sleep(delay)

  def get_log(self):
    return self.log

  def close(self):
    self.socket.close()