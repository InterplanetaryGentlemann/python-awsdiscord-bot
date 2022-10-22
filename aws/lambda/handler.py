#This is the main script that gets called by the API gateway and handles
#Whether the input is a valid command or not

#Import other code module
import commands as cmd

#Import Necessary Packages

import os
from dotenv import load_dotenv, find_dotenv

from nacl.signing import VerifyKey #nacl allows us to verify the public key between the app and the request
from nacl.exceptions import BadSignatureError

#Get Public Key from Environment File
load_dotenv(find_dotenv())
PUBLIC_KEY = os.getenv("DISCORD_PUB_KEY") # found on Discord Application -> General Information page

#Set Response type switch cases
PING_PONG = {"type": 1}

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

#This function handles the filtering of the various commands
#It gets the command name from Discord's JSON response and puts it
#through the handler switch-case. Each command string is mapped to
#the related function

def command_handler(body):
    command = body['data']['name'] #Get the name of the command from the json body
    handler = {
        'aws-start':cmd.aws_start(body), 
        'aws-status':cmd.aws_status(body),
        'aws-stop':cmd.aws_stop(body),
        'aws-restart':cmd.aws_restart(body),
        'aws-list':cmd.aws_list()
    }

    return handler[command]

#Main Lambda function, gets called when an event hits the API Gateway 

def lambda_handler(event, context):
    #print(f"event {event}") # debug print, prints the event request
    
    # verify the signature, returns [UNAUTHOORIZED] message should the provided key be invalid
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

