#This module sets up the boto3 client and functions to ingest the 
#data from commands.py and get or set the necessary instance 
#information, then return a status code.

#Import necessary packages
import boto3

#Set the boto3 client to the ec2 resource type
EC2 = boto3.resource('ec2')

#Function that starts the instance of the given name
def start_instance(name):
    #Create a filter so that we only get the instance specified by the user
    filter = [
        {"Name" :"tag:botEnabled", "Values":["True"]},
        {"Name": "tag:Name", "Values": [name] }
        ]
    
    #Try to get the specified instance, if it is invalid, return 404
    try:
        instances = EC2.instances.filter(Filters=filter)
        #This code ensures that we are only starting one instance. If
        #multiple instances share the same name, throw the 403 error
        #Is this really necessary? Can you even name instances the same thing, are there use cases for starting up groups of instances?
        for i, instance in enumerate (instances, start=1):
            if i == 1:
                state = instance.state['Code']
            else:
                print(i)
                state = 403
                
        if state == 80:
            #start instance
            instance.start()
            return state 
        else:
            return state
    except Exception as e:
        print(e)
        return 404

#Function that gets the runtime status of the given instance
def instance_status(name):
    #Create a filter so that we only get the instance specified by the user
    filter = [
        {"Name" :"tag:botEnabled", "Values":["True"]},
        {"Name": "tag:Name", "Values": [name] }
        ]
    #Need a method to check if the instances variable is empty and return state = 404
    try:
        instances = EC2.instances.filter(Filters=filter)
        #Need to check to see if there is one instance or multiple instances and run the correct loop
        for i, instance in enumerate (instances, start=1):
            if i == 1:
                state = instance.state['Code']
            else:
                print(i)
                state = 403
        return state

    except Exception as e:
        print(e)
        return 404

#Function that stops the AWS instance with the given name,
#Function will also reboot instance if the 'restart' flag is set to true.
def stop_instance(name, restart):
    #Create a filter so that we only get the instance specified by the user
    filter = [
        {"Name" :"tag:botEnabled", "Values":["True"]},
        {"Name": "tag:Name", "Values": [name] }
        ]
    try:
        instances = EC2.instances.filter(Filters=filter)
        for i, instance in enumerate (instances, start=1):
            if i == 1:
                state = instance.state['Code']
            else:
                print(i)
                state = 403
                
        if state == 16 and restart == False:
            #stop instance
            instance.stop()
            return state 
        elif state == 16 and restart == True:
            instance.restart()
            return state
        else:
            return state

    except Exception as e:
        print(e)
        return 404

#Function that returns a list of all the AWS instances the bot 
def list_instances():
    #Filter all instances that are tagged to be controlled by the bot
    filter = [
    {"Name" :"tag:botEnabled", "Values":["True"] }
    ]

    instances = EC2.instances.filter(Filters=filter)

    #Declaring a list to store all of the available instances
    available_instances=[]

    #For each instance, add the Name tag to the list
    for instance in instances:
        if instance.tags != None:
            for tag in instance.tags:
                if tag['Key'] == 'Name':
                    name = (f"{tag['Value']}")
                    available_instances.append(name)
    #Return the completed list
    return available_instances