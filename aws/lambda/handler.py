#This is the main script that gets called by the API gateway and handles
#the resulting json request

#Import Commands Module
import commands as cmd

#Import Necessary Packages

import os
from dotenv import load_dotenv, find_dotenv

from nacl.signing import VerifyKey #nacl allows us to verify the public key between the app and the request
from nacl.exceptions import BadSignatureError

#Get Public Key from Environment File - Needs to be set by bot admin
load_dotenv(find_dotenv())
PUBLIC_KEY = os.getenv("DISCORD_PUB_KEY") # found on Discord Application -> General Information page
TEXT_CHANNEL = os.getenv("TEXT_CHANNEL") # The ID of the Discord Channel you wan to use the bot in

#Set Response type for discord's Ping request
PING_PONG = {"type": 1}

#Verify the Public Key between the one we copied from the developer 
#page and the one given in the API request headers

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
    if TEXT_CHANNEL == body['channel_id']:
        command = body['data']['name'] #Get the name of the command from the json body
        handler = {
            'aws-start':cmd.aws_start(body), 
            'aws-status':cmd.aws_status(body),
            'aws-stop':cmd.aws_stop(body),
            'aws-restart':cmd.aws_restart(body),
            'aws-list':cmd.aws_list()
        }

        return handler[command]
    else:
        return { 
        "type": 4, 
        "data": {
            "tts": False,
            "content": "Bot is not authorized for use in this channel",
            "embeds": [],
            "allowed_mentions": { "parse": [] }
        } 
    }

#Main Lambda function, gets called when an event hits the API Gateway
def lambda_handler(event, context):
    #print(f"event {event}") # debug print, prints the event request
    
    # verify the signature, returns [UNAUTHOORIZED] message should the provided key be invalid
    try:
        verify_signature(event)
    except Exception as e:
        raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")

    #Get the json request from the event
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

