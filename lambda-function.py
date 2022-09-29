#Import Necessary Packages

import json

from nacl.signing import VerifyKey #nacl allows us to verify the public key between the app and the request
from nacl.exceptions import BadSignatureError

import boto3 

#Set Public Key and Response Types

PUBLIC_KEY = 'KEY_GO_HERE' # found on Discord Application -> General Information page
PING_PONG = {"type": 1}
RESPONSE_TYPES =  { 
                    "PONG": 1, 
                    "ACK_NO_SOURCE": 2, 
                    "MESSAGE_NO_SOURCE": 3, 
                    "MESSAGE_WITH_SOURCE": 4, 
                    "ACK_WITH_SOURCE": 5
                  }

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
    option = body['data']['options'][0]['value'] #Get the value of the command's argument to used for selecting the instance

    EC2 = boto3.client('ec2') #boto3 client set to the ec2 resource type
    #servername sets the tag information with the information provided by the user
    servername = [{
           'Name': 'tag:serverName',
           'Values': [option]
        }
    ]

    if command == 'aws-start':
        get_instance(EC2, servername, option)
        option_string = (f"Instance {option} is Starting!")
        print(option_string)
        return { 
            "type": RESPONSE_TYPES['MESSAGE_WITH_SOURCE'], 
            "data": {
                "tts": False,
                "content": option_string,
                "embeds": [],
                "allowed_mentions": { "parse": [] }
            }
        }
    elif command == 'aws-status':
        #status = 
        return { 
            "type": RESPONSE_TYPES['MESSAGE_WITH_SOURCE'], 
            "data": {
                "tts": False,
                "content": " is !",
                "embeds": [],
                "allowed_mentions": { "parse": [] }
            }
        }
    elif command == 'aws-stop':
        return { 
            "type": RESPONSE_TYPES['MESSAGE_WITH_SOURCE'], 
            "data": {
                "tts": False,
                "content": " is stopping!",
                "embeds": [],
                "allowed_mentions": { "parse": [] }
            }
        }
    elif command == 'aws-restart':
        return { 
            "type": RESPONSE_TYPES['MESSAGE_WITH_SOURCE'], 
            "data": {
                "tts": False,
                "content": " is restarting!",
                "embeds": [],
                "allowed_mentions": { "parse": [] }
            }
        }

    else:
        return {
            'statusCode': 400,
            'body': ('unhandled command')
    }
    

def get_instance(client, filter, tag):
    instances = client.instances.filter(FILTER=filter)
    for instance in instances:
        if instance.tags != None:
            for tags in instance.tags:
                if tag['Key'] == 'discordBot':
                    return instances


#def start_instance(instance, tag):
    #instances = instance.instances.filter(FILTER=filters)

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

