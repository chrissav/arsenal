---
layout: page
type: doc
title: Docker Compose
permalink: /docker_compose/
categories: docker
tags: [docker, image, container, docker-compose, it-ops, how-to]
published: true
---

##### This runbook will be a walkthrough of getting started with docker-compose.  We'll build 1 container with Flask and 1 container with Mongo DB and link them.  Docker-compose is an easy way to build images and run containers that are linked to each other.  The following topics will be covered:
1. Using a Vagrant Environment
2. Install docker-compose
3. File setup
4. Running everything

### 1. Using a Vagrant Environment
This runbook is written using a vagrant environment with `Vagrant 1.6.3` running an `ubuntu/trusty64 distro`.  You can download and install vagrant [here](https://www.vagrantup.com/).  There are alot of resources on the vagrant website to [get started](https://docs.vagrantup.com/v2/getting-started/index.html) and using vagrant with the [command line](https://docs.vagrantup.com/v2/cli/index.html).

If you don't want to use Vagrant, any virtual machine will do (but Vagrant is better).  Or you can check out [boot2docker](http://boot2docker.io/), made by Docker to use docker easily on OS X.  It's really just a tiny VM, so don't get excited.

Use a [Vagrantfile](https://docs.vagrantup.com/v2/vagrantfile/index.html) with the contents:
```
  1 VAGRANTFILE_API_VERSION = "2"¬
  2 ¬
  3 Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|¬
  4   config.vm.box = "ubuntu/trusty64"¬
  5 ¬
  6   config.vm.network "forwarded_port", guest: 80, host: 8080¬
  7   config.vm.network "forwarded_port", guest: 5000, host: 5000¬
  8 end¬
```
Forwarding port 5000 will be important to view the Flask website in your local browser.

### 2. Install [docker-compose](https://docs.docker.com/compose/install/)
```
pip install -U docker-compose
chmod +x /usr/local/bin/docker-compose
```

Test it's installed correctly
```
docker-compose --version
```

### 3. File setup

Make a directory, I'm using 'alpine', with 4 files: 

```
alpine:
  - app.py  //will run a basic Flask app
  - docker-compose.yml //the magic that links the containers and other cool stuff
  - Dockerfile
  - requirements.txt
```

If you're not familiar with flask you can check out [Installing Flask](http://flask.pocoo.org/docs/0.10/installation/) and [Quick Start to Flask](http://flask.pocoo.org/docs/0.10/quickstart/), but you don't need to.

The contents of app.py with explanations:
```
1 import os
2 from flask import Flask, redirect, url_for, request, render_template
3 from pymongo import MongoClient
4 
5 app = Flask(__name__) # create a basic Flask app
6 
7 client = MongoClient(os.environ['ALPINE_DB_1_PORT_27017_TCP_ADDR'], 27017) # creates a mongo db client that connects to the db by IP address and port number.  'ALPINE_DB_1_PORT_27017_TCP_ADDR' is an environment variable of the container IP.
8 db = client.alpinedb # create the db
9
10 @app.route('/') #Route the url to the root direcory
11 def alpine():
12
13   _items = db.alpinedb.find()
14   items = [item for item in _items] # loop through all items in the db
15
16   return render_template('alpine.html', items=items) # render the template with items from the db
17
18 @app.route('/new', methods=['POST']) # Post function to add new items to the database via an html form
19 def new():
20   # create a form with 2 fields
21   item_doc = {
22     'name': request.form['name'],
23     'description': request.form['description']
24   }
25   db.alpinedb.insert_one(item_doc) # insert into db
26
27   return redirect(url_for('alpine')) # redirect back to root dir to refresh the page with new values
28
29 if __name__ == "__main__":
30   app.run(host='0.0.0.0', debug=True) # open app to all Ip addresses
 ```

The contents of the [Dockerfile](https://docs.docker.com/reference/builder/)
```
FROM alpine:edge
ADD . /alpine
WORKDIR /alpine
RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
&& pip install -r requirements.txt \
&& rm -rf install /var/cache/apk/*
```
Docker always looks to the Dockerfile when building the image.  The image we're using is Alpine:edge, the latest version of Alpine.  [Alpine](https://hub.docker.com/_/alpine/) is a super light weight linux distro at only 5 MB.  There are a few extra steps to take with apk to install python and such.. but still much better than the python:2.7 distro which is about 230 MB.

The contents of requirements.txt:
```
flask
pymongo
```

The contents of docker-compose.yml:
```
web:
  build: .
  command: python -u app.py
  ports:
    - "5000:5000"
  volumes:
    - .:/alpine
  links:
    - db
db:
  image: mongo:3.0.2
```
This is the coolest part of the setup.  "web" and "db" are the names of two different containers.  The "build" option passes a `.` to tell it to build the docker image from this directory.  So it'll look for a Dockerfile in the directory it is in.  The "command" option will run the command `python -u app.py` in the container as soon as it's up and running.  The option "ports" tells it to forward port 5000 to 5000.  The "volumes" option will mount a volume from the local vm to the container.  In this case it's mounting the current directory `.` to the directory `/alpine`.  The "links" option tells this container to link to another container (that's all you have to do to connect them!!).  The "image" option under db will provide that container with the mongo:3.0.2 image from the Docker Hub.  

Lastly, because we're being difficult and setting an html template to be rendered, we need to add the template.
Make a directory called `templates` with the file alpine.html and the contents:
```
<!doctype html>
<form action="/new" method="POST">
  <input type="text" name="name"></input>
  <input type="text" name="description"></input>
  <input type="submit"></input>
</form>


{% for item in items %}
  <h1> {{ item.name }} </h1>
  <p> {{ item.description }} </p>
{% endfor %}
```

Directory should look like this now:
```
compose_app:
  - app.py  //will run a basic Flask app
  - docker-compose.yml //the magic that links the containers and other cool stuff
  - Dockerfile
  - requirements.txt
  - templates/
    - alpine.html
```

### 4. Running Everything

```
docker-compose up
```

It will start executing the commands in the Dockerfile then docker-compose.yml.  When it's done setting up, it'll show a network log and run until you hit ctrl+c.  Go to localhost:5000 in your browser (locally, on your mac).  Try entering info in the fields and hitting submit.  It'll get added the db.

NOTE:  If you get a DNS error while the image is building, try updating your VM's dns server to 8.8.8.8, if it's not already.  
ANOTHER NOTE:  If you make any changes to the docker-compose setup after running `docker-compose up`, you will need to run `docker-compose build` to rebuild the images, and then `docker-compose up` again.
