#This module contains all of the functions thattake the information
#given by the discord bot

#Function that starts the instance of the given name

def start_instance(client, name):
    #Create a filter so that we only get the instance specified by the user
    filter = [
        {"Name" :"tag:botEnabled", "Values":["True"]},
        {"Name": "tag:Name", "Values": [name] }
        ]
    #Need a method to check if the instances variable is empty and return state = 404
    try:
        instances = client.instances.filter(Filters=filter)
        #Need to check to see if there is one instance or multiple instances and run the correct loop
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
def instance_status(client, name):
    #Create a filter so that we only get the instance specified by the user
    filter = [
        {"Name" :"tag:botEnabled", "Values":["True"]},
        {"Name": "tag:Name", "Values": [name] }
        ]
    #Need a method to check if the instances variable is empty and return state = 404
    try:
        instances = client.instances.filter(Filters=filter)
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
def stop_instance(client, name, restart):
    #Create a filter so that we only get the instance specified by the user
    filter = [
        {"Name" :"tag:botEnabled", "Values":["True"]},
        {"Name": "tag:Name", "Values": [name] }
        ]
    #Need a method to check if the instances variable is empty and return state = 404
    try:
        instances = client.instances.filter(Filters=filter)
        #Need to check to see if there is one instance or multiple instances and run the correct loop
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
def list_instances(client, filter):
    instances = client.instances.filter(Filters=filter)

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