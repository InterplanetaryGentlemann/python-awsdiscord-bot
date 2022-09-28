#Import Necessary Packages

import json

from nacl.signing import VerifyKey #nacl allows us to verify the public key between the app and the request
from nacl.exceptions import BadSignatureError

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


#Verify the Public Key between the one we copied from the developer page and the one given in the API request

def verify_signature(event):
    raw_body = event.get("rawBody")
    auth_sig = event['params']['header'].get('x-signature-ed25519')
    auth_ts  = event['params']['header'].get('x-signature-timestamp')
    
    message = auth_ts.encode() + raw_body.encode()
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    verify_key.verify(message, bytes.fromhex(auth_sig)) # raises an error if unequal

#Set a function to verify whether the given type is a ping

def ping_pong(body):
    #print(f"Checking Ping")
    if body.get("type") == 1:
        return True
    return False
    
def command_handler(body):
    command = body['data']['name']
    option = body['data']['options'][0]['value']
    
    print(f"{option}")
#RESPONSE_TYPES['MESSAGE_WITH_SOURCE'],
    if command == 'aws-start':
        return { 
            "type": RESPONSE_TYPES['MESSAGE_WITH_SOURCE'], 
            "data": {
                "tts": False,
                "content": "Myles Ween is enormous",
                "embeds": [],
                "allowed_mentions": { "parse": [] }
            }
        }


    else:
        return {
            'statusCode': 400,
            'body': ('unhandled command')
    }
    
def lambda_handler(event, context):
    print(f"event {event}") # debug print, prints the event request
    
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
    
 
