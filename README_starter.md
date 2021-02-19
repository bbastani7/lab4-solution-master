# Lab 4 - Drone Controller

## Due Date

Feb 8 @ 9 p.m. PST

## Prerequisites
This lab builds on prior work we've done in class and in the labs. It'll really help you to have seen all the related videos before attempting to do this lab. 

1) Video lecture on [HTML](https://www.youtube.com/watch?v=Ht5nE2l4mJI)
2) Video lecture on [Web Serving Fundamentals](https://www.youtube.com/watch?v=5a0R2yiiEeo)
3) Video lecture on [REST](https://www.youtube.com/watch?v=YHZmSlF-rOU)
4) Video lectures on Javascript
    1) [Introduction to Javascript](https://www.youtube.com/watch?v=E0_pEASqB3A&feature=emb_title)
    2) [Interactions](https://www.youtube.com/watch?v=Mwf_qU6zQfo)
    3) [Asynchronous javascript + JSON](https://www.youtube.com/watch?v=eusDs93MlnQ)
5) DB Intro Videos(Pick one of these):
    1) Intro to Database [Video](https://youtu.be/3_GMPJFF1sI)
    2) Advanced Intro to Database [Video](https://youtu.be/GsSagoCByzc)
6) DB Crud Operations [Video](https://youtu.be/FV0hr-cw47A)
7) DB Join Operations [Video](https://youtu.be/-LqlkZ6S7p4)
8) RESTful Databases
    1) [Video 1](https://youtu.be/czJYswiRx-g)
    2) [Video 2](https://youtu.be/U73e3TJxvxM)

## Overview

We will be building a web-based controller for our drone. By the end of this lab, you will build an interface to control your drone. Our database gets an upgrade and we will now be working with SQL databases. We now have three servers: 
1. `web-server`  (a web server in python)
2. `drone-controller`  (more python code to talk to the drone API)
3. `mysql-db`  (a database server you talk to using SQL)

Our `web-server` container is similar to the `frontend` server that you worked with in Lab 3; it provides users with a web-interface they can use to send commands to the database server (and control the drone). The `drone-controller` is where all communication with the drone takes place; it constantly looks for new commands in the database and executes them as they come in. The `mysql-db` database server takes care of storing and retrieving commands that were sent from the `web-server`, to and from a persistent database. The image below provides an overview of the system.

![system](images/ECE140A_Lab4_system.jpg)

Notice that the web server does not directly communicate with the drone controller. Instead, when a user interacts with a webpage you create, it sends RESTFUL requests to the the web server, which in turn communicates with the database.  The drone controller actively looks for a new commands in the database (commands table) that has not yet been executed. As new commands come in, the drone controller executes them one-by-one in the order that they arrived in. For more information on how an event loop works, refer to [here](https://en.wikipedia.org/wiki/Event_loop#:~:text=In%20computer%20science%2C%20the%20event,or%20messages%20in%20a%20program.).

The first thing you will need to do is create a credentials file that allows you to access the mySQL docker container. Create a credentials.env file in the root of this directory and add the following 5 values. You will need to make up the last 3 fields:

```bash
  MYSQL_HOST=mysql-db
  MYSQL_DATABASE=lab4ece140a
  MYSQL_ROOT_PASSWORD= [...]
  MYSQL_USER= [...]
  MYSQL_PASSWORD= [...]
```

We can start the container containing all three servers using: `docker-compose up --build`.
You will see something like this further along in your console output:
![console_output](images/console_output.png)

Now, open up your browser and go to `0.0.0.0:8000`, or if that doesn't work, you might need to use `localhost:8000`. You should see your browser display the text **"Drone Controller"**

## Challenge 1 - Controller Design 

Your first challenge is to design an interface on the `web-server` to interface with the mySQL database. You have the freedom to make it as pretty and interactive as you'd like using CSS and JavaScript. An example of a controller design is shown below:

![controller_example](images/controller_example.png)

The next step is to make RESTful commands to the web-server to print the name of the command that the user selected to the terminal. 

You will notice that a route to send commands from the web-server has been added for you. It looks like this:

```python
    config.add_route('drone_command', '/drone_command/{command}*arg')
    config.add_view(drone_command_route, route_name='drone_command', renderer='json')
```

Notice that this is unlike any of the commands you have seen so far. Unlike static routes, which we have been working with so far, this route allows you to pass parameters and thus dynamically controlling the execution. If we stuck with static routes, we would have to crete a separate route for each type of drone command. Do you see how this can quickly add up to too many routes?

Note that static routes amounts to constructing URL's of the following form:
`http://localhost:8000/drone_command/up/20` -> represents instructing the drone to go 'up' by 20cm
`http://localhost:8000/drone_command/takeoff` -> to instruct the drone to take off.
**Also NOTE that not all commands require arguments. See [Tello SDK Documentation](https://dl-cdn.ryzerobotics.com/downloads/tello/20180910/Tello%20SDK%20Documentation%20EN_1.3.pdf) to view acceptable commands.**
The argument's for linear motion controls (forward, back, up, left etc..) and rotational controls (clockwise, counter-clockwise) will need to be variable via your interface. You can use a slider a dropdown or whatever you like to accomplish this.

As an example: National Weather service's API uses this parameter format in their API to fetch data from a specific location. Feel free to try it out: <https://api.weather.gov/points/{latitude},{longitude>}

Be sure to replace the latitude and lonitude with the location you are looking for. Try [La Jolla](https://api.weather.gov/points/32.8801,-117.234)(32.8801, -117.234) and [New York](https://api.weather.gov/points/40.7128,-74.006)(40.7128,-74.006)

The `drone_command_route` function is responsible for parsing the provided command and translating it to the appropriate syntax that the Tello drone understands. We also check that the sent command is valid.

## Challenge 2 - Database Initiaization
In this step we will build the database to store all drone commands to an SQL database. You will need to create a table named `Commands` with the following schema:

![schema](images/schema.png)

Add your SQl code to the file named `init-db.sql`

In the previous challenge, you have verified that these user button clicks or key presses are successfully communicating with the web server, it's time to complete the system. We need to parse these received commands and store them in the SQL database. 

The `drone_command_route` function is responsible for parsing the provided command and translating it to the appropriate syntax that the Tello drone understands. We have to also check that the sent command is valid. 

Your task is to complete the function named `send_command` to send the given command to the database. 

## Challenge 3 - Updating the database

In this challenge, you will be completing the event loop implementation in `command-dispatcher.py` to read commands from the SQL database, sending the command to the Tello drone and marking the command as completed in the database. 

Note that the Commands table has a key *completed* that indicates whether a given command was executed or not. This will ensure that only the commands that have not yet been executed will be sent to the Tello drone. 


## Deliverables

You will need to have built a web-based controller to interface with the drone. Please record a video* using your phone showing evidence of being able to fly the drone with the controller you just built. Please show at least the following commands in your video: TAKEOFF, LAND, UP, DOWN, FORWARD, BACK, ROTATE CLOCKWISE, ROTATE COUNTERCLOCKWISE. 

*Please limit videos to 3 minutes and upload it to youtube and paste the link to the video below. 

Drone Flight Video: <Insert Video Link Here>
