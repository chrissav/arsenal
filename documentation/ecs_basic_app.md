---
layout: page
type: doc
title: ECS Basic App
permalink: /aws/ecs/ecs_basic_app/
categories: docker
tags: [docker, ecs, aws, misc]
published: true
---

##### This runbook will be a walkthrough of getting started with AWS ECS.  It'll build an ECS cluster and a basic sample app, similar  to the app in the [docker_compose runbook](https://tech-ops-runbook.2u.com/docker_compose/).  It will cover the following steps:
1. Create the Docker Images
2. Create an EC2 instance to be used with ECS
3. Create a Cluster
4. Create the Task Definition
5. Create Service to Run Task 
6. Test the app
7. Do all of this in one step. Create template to build ECS Cloudformation stack
8. Clean Up

### 1. Create the Docker Images
The Docker Images will need to be created for ECS to use.  We're going to use the image that was created in the [docker_compose runbook](https://tech-ops-runbook.2u.com/docker_compose/), with one minor change because the environment variables will be different in ECS.  In app.py on line 7 change
```
client = MongoClient(os.environ['ALPINE_DB_1_PORT_27017_TCP_ADDR'], 27017)
```
to
```
7 client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
```
Save the file and re-build the image
```
$ docker-compose build
```
Name and tag the image with your_repo_name/app_name:tag
```
$ docker tag -f chrissav/flask_web:latest
```
Push the image to docker hub
```
docker push chrissav/flask_web:latest
```

### 2. Create EC2 Instance to be Used with ECS
- Spin up an instance in EC2 like you would any other.  
There are ecs-optimized images in the Community section of the AMI's.
If you don't use one of these images, you must install docker and the ECS agent on the box before using it with ECS.

### 3. Create a Cluster
- Go to AWS Console --> ECS --> Clusters --> Create Cluster
- Give it a name
- Register the EC2 instance to the cluster (the cli is the easiest way)

### 4. Create the Task Definition
Important Note: I haven't been able to find a way to actually remove Task Definitions once they're created.  This is silly.  If this changes or you find a way, update this runbook.

There are two ways to create a new Task Definition, using the Builder and using a JSON template. To use the builder:
- Go to AWS Console --> ECS --> Task Definitions --> Create New Task Definition
- Give it a name
- Add Container Definition -->
  - Container Name: web
  - Image: chrissav/flask_web:latest
  - Memory: 300
  - CPU Units: 10
  - Essential: yes
  - Port Mappings: 5000 -> 5000 TCP
  - Command: python,-u,app.py
  - Links: db
- Add Another container definition -->
  - Container Name: db
  - Image: mongo:3.0.2
  - Memory: 300
  - CPU Units: 10

If you want to mount a volume, Add a volume with a name and source path (where the directory exists on the EC2 instance), and in the Container Definition add a Mount Point with the name of the volume and the Container Path(where the volume will go in the container).  But you don't need to for this since it's in the image.

### 5. Create Service to Run Task
- Go to the cluster --> Services --> Create
- Pick a task to run, a service name, and number of tasks the service should be running (in this case 1)
- You can choose to add it to an ELB
- Create Service
Now the Service will ensure the task is running x number of times.

### 6. Test the app
- Go to Task Defintions
- Select the new task you just made
- Actions --> Run Task
- Select the cluster you want to run it on
- Run Task
Now you can try accessing the app from the instance by running
```
curl localhost:5000
```
You can use lynx to submit data on the form with
```
lynx localhost:5000
```
Enter the data, and do another curl to see the result.

### 7. Do This All from Cmd Line :)
By using a CloudFormation template, all of this can be created with an AWS CLI command.

Get the ecs-sample.json template from the [CloudFormation repo](https://github.com/2uinc/CloudFormation)

1. Build the Cloudformation stack
{% highlight bash %}
```
$ aws cloudformation create-stack --stack-name ecs-test-stack --template-body file://///Users/csavadel/Desktop/repos/2u/CloudFormation/ecs-sample.json --parameters ParameterKey='EcsAmiId',ParameterValue='ami-4fe4852a' ParameterKey='IamRoleInstanceProfile',ParameterValue='ecsInstanceRole' ParameterKey='KeyName',ParameterValue='docker-sample-dev' --region us-east-1
{
    "StackId": "arn:aws:cloudformation:us-east-1:127579856528:stack/ecs-test-stack/76700600-6210-11e5-b77c-50442ee11cd2"
}
```
{% endhighlight %}
2. Create the Task Defintion
- Create a blank json template.
```
$ aws ecs register-task-definition --generate-cli-skeleton
```
- This template can be used to define one container.  If you want to use more than on you need to use the option --container-definitions instead of --cli-input-json, and the format of the JSON template is a little different.  Fill out what you need, here is an example
{% highlight json %}
```
[
    {
        "name": "web",
        "image": "chrissav/flask_web:latest",
        "cpu": 10,
        "memory": 300,
        "links": [
            "db"
        ],
        "portMappings": [
            {
                "containerPort": 5000,
                "hostPort": 5000
            }
        ],
        "essential": true,
        "entryPoint": [
            ""
        ],
        "command": [
            "python",
            "-u",
            "app.py"
        ],
        "environment": []
    },
    {
        "name": "db",
        "image": "mongo:3.0.2",
        "cpu": 10,
        "memory": 300,
        "links": [],
        "portMappings": [],
        "essential": true,
        "entryPoint": [
            ""
        ],
        "command": [
            ""
        ],
        "environment": []
    }
]
```
{% endhighlight %}

3. Create the Service to run the task

```
$ aws ecs --region us-east-1 create-service --service-name ecs-flask-test --task-definition flask --desired-count 1
```

This Cloudformation Template does a litle more too.  It will put it in an autoscaling group.  And if you delete the running task, it'll get recreated.  If you stop/terminate the instance it's running on, it'll switch to antoher instance in the cluster or create a new instance to run on.  :)

### 8. Clean Up
If you want to remove everything just created, you need to do a few things aside from just deleting the Cloudformation Stack.
To Remove:
1.  Update your service tasks to 0
```
$ aws --region us-west-2 ecs update-service --cluster cluster_name --service service_name --desired-count 0
```
2. delete the service
```
$ aws  --region us-west-2 ecs delete-service --cluster cluster_name --service service_name
```
3. deregister container instances
```
$ aws --region us-west-2 ecs deregister-container-instance --cluster cluster_name --container-instance container_instance_id --force
```
4. delete the cluster
```
$ aws --region us-west-2 ecs delete-cluster --cluster custer_name
```
5. delete the cloudformation stack
