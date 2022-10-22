#AWS State Codes:
#0:'pending',
#16:'running',
#32:'shutting-down',
#48:'terminated',
#64:'stopping',
#80:'stopped'

#This module contains all of the code pertaining to the bot's 
#slash commands and the formulation of the responses.

#Import the instancemds.py module, shorten to icmd for calls

import instancecmds as icmd

#Import Necessary Packages

import json

import boto3 

#Case Switch for Discord's response types
RESPONSE_TYPES =  { 
                    "PONG": 1, 
                    "ACK_NO_SOURCE": 2, 
                    "MESSAGE_NO_SOURCE": 3, 
                    "MESSAGE_WITH_SOURCE": 4, 
                    "ACK_WITH_SOURCE": 5
                  }

#boto3 client set to the ec2 resource type
EC2 = boto3.resource('ec2') 

#This is a filter to pass to the boto3 commands. It narrows searches to Instances that have this tag.
botenabled = [
    {"Name" :"tag:botEnabled", "Values":["True"] }
    ]

#This is a simple function that takes the string content provided to it 
#and returns it as a json response for the discord application
def jsonresponse(content):
    return { 
        "type": RESPONSE_TYPES['MESSAGE_WITH_SOURCE'], 
        "data": {
            "tts": False,
            "content": content,
            "embeds": [],
            "allowed_mentions": { "parse": [] }
        } 
    }

#This is the function for the aws-start slash command.
#if all checks are passed, the specified instance should start and 
#the switch case should respond with the "Starting!" message

def aws_start(body):
    if 'options' in body['data']:
        option = body['data']['options'][0]['value'] #Get the value of the command's argument
        response = icmd.start_instance(EC2, option)
        message = {
            
            0:(f"Instance {option} is already Starting! Please be patient!"),
            16:(f"Instance {option} is already Running! If you need to reboot the server run the /aws_restart command!"), 
            32:(f"Instance {option} is currently being Terminated. Please contact the System Admin for more info."), 
            48:(f"Instance {option} has been Terminated. Please contact the System Admin for more info"),
            64:(f"Instance {option} is currently Stopping! Please wait before running this command again."),
            80:(f"Starting the {option} Instance! Enjoy your playtime!"),
            403:(f"Duplicate Instances with the name {option}! Please rename or terminate these Instances!"),
            404:(f"Instance {option} does not exist! Run aws-list to view valid Instance names.")
            
        }
        
        response_string = message[response]

    else:
        response_string = "Not a valid option."
    
    return jsonresponse(response_string)

#The aws-status command sends the option to the instance_status function
#and returns the current state (Starting, Running, Stopped, etc.) of the 
#specified EC2 Instance

def aws_status(body):
    if 'options' in body['data']:
        option = body['data']['options'][0]['value'] #Get the value of the command's argument
        #example reponse string(f"Instance {option} is Starting!")
        response = icmd.instance_status(EC2, option)
        message = {
            
            0:(f"Instance {option} is currently Starting!"),
            16:(f"Instance {option} is currently Running"), 
            32:(f"Instance {option} is currently being Terminated. Please contact the System Admin for more info."), 
            48:(f"Instance {option} has been Terminated. Please contact the System Admin for more info"),
            64:(f"Instance {option} is currently Stopping!"),
            80:(f"Instance {option} is currently Stopped!"),
            403:(f"Duplicate Instances with the name {option}! Please rename or terminate these Instances!"),
            404:(f"Instance {option} does not exist! Run aws-list to view valid Instance names.")

        }
        response_string = message[response]
    else:
        response_string = "Not a valid option."
    
    return jsonresponse(response_string)

#The aws-stop command works the same as the start command,
#just with the checks and endgoal reversed
def aws_stop(body):
    if 'options' in body['data']:
        option = body['data']['options'][0]['value'] #Get the value of the command's argument
        response = icmd.stop_instance(EC2, option, False)
        message = {
            0:(f"Instance {option} is currently Starting! Please wait for the Instance to finish before running this!"),
            16:(f"Stopping the {option} Instance! Thanks for playing!"), 
            32:(f"Instance {option} is currently being Terminated. Please contact the System Admin for more info."), 
            48:(f"Instance {option} has been Terminated. Please contact the System Admin for more info"),
            64:(f"Instance {option} is already Stopping! Please be patient!"),
            80:(f"Instance {option} is already Stopped! Use /aws-start to Start the Instance!"),
            403:(f"Duplicate Instances with the name {option}! Please rename or terminate these Instances!"),
            404:(f"Instance {option} does not exist! Run aws-list to view valid Instance names.")
        }
        response_string = message[response]

    else:
        response_string = "Not a valid option."
    
    return jsonresponse(response_string)

#The restart command uses the stop instance function with the restart flag
#set to true. See instancecmds.py for more info
def aws_restart(body):
    if 'options' in body['data']:
        option = body['data']['options'][0]['value'] #Get the value of the command's argument
        response = icmd.stop_instance(EC2, option, True)
        message = {
            0:(f"Instance {option} is currently Starting! Please wait for the Instance to finish before running this!"),
            16:(f"Restarting the {option} Instance! It'll be back soon!"), 
            32:(f"Instance {option} is currently being Terminated. Please contact the System Admin for more info."), 
            48:(f"Instance {option} has been Terminated. Please contact the System Admin for more info"),
            64:(f"Instance {option} is already Stopping! Please be patient!"),
            80:(f"Instance {option} is already Stopped! Use /aws-start to Start the Instance!"),
            403:(f"Duplicate Instances with the name {option}! Please rename or terminate these Instances!"),
            404:(f"Instance {option} does not exist! Run aws-list to view valid Instance names.")
        }
        response_string = message[response]
    else:
        response_string = "Not a valid option."
    
    return jsonresponse(response_string)

def aws_list():
    #Get instance names
    instances = icmd.list_instances(EC2, botenabled)

    #If the list is empty, respond that no instances were found
    if instances == []:
        response_string = "No Instances Available"
        return jsonresponse(response_string)

    else:  
        #Format the list so that each entry shows up on a new line  
        response_string = ('\n'.join(map(str, instances)))
        return jsonresponse(response_string)
    

