#Import Necessary Packages

import json

from nacl.signing import VerifyKey #nacl allows us to verify the public key between the app and the request
from nacl.exceptions import BadSignatureError

import boto3 

#Set Public Key and Response Types

PUBLIC_KEY = '7a0537b47a2207c0df3a495e6e9045663d15ccb29da95e68c7a576acb09e4f37' # found on Discord Application -> General Information page
PING_PONG = {"type": 1}
RESPONSE_TYPES =  { 
                    "PONG": 1, 
                    "ACK_NO_SOURCE": 2, 
                    "MESSAGE_NO_SOURCE": 3, 
                    "MESSAGE_WITH_SOURCE": 4, 
                    "ACK_WITH_SOURCE": 5
                  }


EC2 = boto3.resource('ec2') #boto3 client set to the ec2 resource type
#servername sets the tag information with the information provided by the user
#servername = [{
#       'Name': 'tag:Name',
#       'Values': [option]
#    }
#]
botenabled = [{"Name" :"tag:botEnabled", "Values":["True"] }]


#Verify the Public Key between the one we copied from the developer page and the one given in the API request

def verify_signature(event):
    raw_body = event.get("rawBody")
    auth_sig = event['params']['header'].get('x-signature-ed25519')
    auth_ts  = event['params']['header'].get('x-signature-timestamp')
    
    message = auth_ts.encode() + raw_body.encode()
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    verify_key.verify(message, bytes.fromhex(auth_sig)) # raises an error if unequal

#A function to verify whether the message is a ping from Discord

def ping_pong(body):
    if body.get("type") == 1:
        return True
    return False

#This function handles the filtering of the various commands. 
#It gets the name of the run command, calls the related AWS Function 
#and sends a response

def command_handler(body):
    command = body['data']['name'] #Get the name of the command from the json body
    handler = {
        'aws-start':aws_start(body), 'aws-status':aws_status(body),'aws-stop':aws_stop(body),'aws-restart':aws_restart(body),'aws-list':aws_list()
    }

    return handler[command]
    
    
def aws_start(body):
    if 'options' in body['data']:
        option = body['data']['options'][0]['value'] #Get the value of the command's argument to used for selecting the instance
        option_string = (f"Instance {option} is Starting!")
    else:
        option_string = "Not a valid option."
    #start_instance(EC2, botenabled, option)
    
    return { 
        "type": RESPONSE_TYPES['MESSAGE_WITH_SOURCE'], 
        "data": {
            "tts": False,
            "content": option_string,
            "embeds": [],
            "allowed_mentions": { "parse": [] }
        }
    }

def aws_status(body):
    #option = body['data']['options'][0]['value'] #Get the value of the command's argument to used for selecting the instance
    #instance_status(EC2, botenabled, option)
    return { 
        "type": RESPONSE_TYPES['MESSAGE_WITH_SOURCE'], 
        "data": {
            "tts": False,
            "content": " is !",
            "embeds": [],
            "allowed_mentions": { "parse": [] }
        }
    }

def aws_stop(body):
    #option = body['data']['options'][0]['value'] #Get the value of the command's argument to used for selecting the instance
    #stop_instance(EC2, botenabled, option)
    return { 
        "type": RESPONSE_TYPES['MESSAGE_WITH_SOURCE'], 
        "data": {
            "tts": False,
            "content": " is stopping!",
            "embeds": [],
            "allowed_mentions": { "parse": [] }
        }
    }

def aws_restart(body):
    #option = body['data']['options'][0]['value'] #Get the value of the command's argument to used for selecting the instance
    #restart_instance(EC2, botenabled, option)
    return { 
        "type": RESPONSE_TYPES['MESSAGE_WITH_SOURCE'], 
        "data": {
            "tts": False,
            "content": " is restarting!",
            "embeds": [],
            "allowed_mentions": { "parse": [] }
        }
    }

def aws_list():
    #Get instance names
    instances = list_instances(EC2, botenabled)

    #If the list is empty, respond that no instances were found
    if instances == []:
        return { 
            "type": RESPONSE_TYPES['MESSAGE_WITH_SOURCE'], 
            "data": {
                "tts": False,
                "content": "No Instances Available",
                "embeds": [],
                "allowed_mentions": { "parse": [] }
            }
        }
    else:  
        #Format the list so that each entry shows up on a new line  
        list_string = ('\n'.join(map(str, instances)))

        return { 
            "type": RESPONSE_TYPES['MESSAGE_WITH_SOURCE'], 
            "data": {
                "tts": False,
                "content": list_string,
                "embeds": [],
                "allowed_mentions": { "parse": [] }
            }
        }
    
#Function that starts the AWS instance with the given name
def start_instance(client, filter, name):
    instances = client.instances.filter(Filters=filter)
    instance = get_instance(instances, name)

        #Check 1:
            #Return 0
        #Check 2:
            #Return 1
    return


#Function that gets the runtime status of the given instance
def instance_status(client, filter, name):
    instances = client.instances.filter(Filters=filter)

        #Check 1:
            #Return 2
        #Check 2: 
            #Return 3
    return


#Function that stops the AWS instance with the given name
def stop_instance(client, filter, name):
    instances = client.instances.filter(Filters=filter)
    return


#Function that restarts the AWS instance with the given name
def restart_instance(client, filter, name):
    instances = client.instances.filter(Filters=filter)
    return

#Function that returns a list of all the AWS instances the bot can interact with, determined by the AWS tag botEnabled=True
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
    return available_instances

#Function that takes the list of instances from other functions and returns the instance that matches the name
def get_instance(instances, name):
    
    for instance in instances:
        if instance.tags != None:
            for tag in instance.tags:
                if tag['Key'] == 'Name'and tag['Value'] == name:
                    return instance

def lambda_handler(event, context):
    #print(f"event {event}") # debug print, prints the event request
    
    # verify the signature
    try:
        verify_signature(event)
    except Exception as e:
        raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")

    body = event.get('body-json')
    
    if ping_pong(body):
        return PING_PONG
    elif not ping_pong(body):
        return command_handler(body)
    else:
      return {
        'statusCode': 400,
        'body': ('unhandled request type')
      }

