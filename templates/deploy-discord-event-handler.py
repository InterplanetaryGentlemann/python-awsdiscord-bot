import boto3
import botocore
import logging
from zipfile import ZipFile
import os
from os.path import basename
import sys
import json
import time
import yaml

def main():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    param_file = './config.json'
    if os.path.isfile(param_file):
        json_data=open(param_file).read()
    else:
        print ("Parameters file: " + param_file + " is invalid!")
        print (" ")
        sys.exit(3)

    print ("Parameters file: " + param_file)
    parameters_data = json.loads(json_data)
    region = parameters_data["REGION"]
    unique_prefix = parameters_data["UNIQUE_PREFIX"]
    s3_bucket = f'{unique_prefix}-discord-event-handler-source'
    print ("Connecting to region: " + region)
    cfn_client = boto3.client('cloudformation', region)
    generate_discord_lambda_source(s3_bucket,region)
    create_discord_lambda_stack(unique_prefix,region,s3_bucket,cfn_client)

def generate_discord_lambda_source(s3_bucket,region):
    try:
        with ZipFile('discord_event_handler.zip', 'w') as zipObj:
            # Iterate over all the files in directory
            for folderName, subfolders, filenames in os.walk('../src'):
                for filename in filenames:
           #create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)
           # Add file to zip
                    zipObj.write(filePath, basename(filePath))
        s3_client = boto3.client('s3', region_name=region)
        location = {'LocationConstraint': region}
        s3_client.create_bucket(
            Bucket=s3_bucket,
            CreateBucketConfiguration=location,
            ACL='private')
        s3_client.upload_file(file_name="../src/discord_event_handler.zip", bucket=s3_bucket, object_name="discord_event_handler.zip")
    except botocore.exceptions.ClientError as e:
        logging.error(e)
        return False
    return True

def create_discord_lambda_stack(unique_prefix,region,s3_bucket,cfn_client):
    cfn_stack_name = f'{unique_prefix}-discord-event-handler-stack'
    template_file_location = 'discord-event-handler-cft.yaml'
    print ("You are deploying stack: " + cfn_stack_name)
    #-- Check if this stack name already exists
    stack_list = cfn_client.describe_stacks()["Stacks"]
    stack_exists = False
    for stack_cf in stack_list:
        if cfn_stack_name == stack_cf["StackName"]:
            print ("Stack " + cfn_stack_name + " already exists.")
            stack_exists = True
    #-- If the stack already exists then delete it first
    if stack_exists:
        user_response = input ("Do you want to delete the stack? (y/n)")
        confirm_values = ['y','yes','Y','YES']
        if user_response == any(confirm_values):
            print ("Calling Delete Stack API for " + cfn_stack_name)
            cfn_client.delete_stack(StackName=cfn_stack_name)
            #-- Check the status of the stack deletion
            check_status(cfn_client, cfn_stack_name)
    print (" ")
    print ("Calling CREATE_STACK method to create: " + cfn_stack_name)
    status_cur = ""
    # read entire file as yaml
    with open(template_file_location, 'r') as content_file:
        content = yaml.load(content_file)
    # convert yaml to json string
    content = json.dumps(content)
    print("Creating {}".format(cfn_stack_name))
    result = cfn_client.create_stack(
        StackName=cfn_stack_name,
        TemplateBody=content,
        Parameters=[{ # set as necessary. Ex: 
            'ParameterKey': 'UniquePrefix',
            'ParameterValue': unique_prefix,
            'ParameterKey': 'Region',
            'ParameterValue': region,
            'ParameterKey': 'S3BucketName',
            'ParameterValue': s3_bucket
        }]
    )
    print ("Output from API call: ")
    print (result)
    print (" ")
    #-- Check the status of the stack creation
    status_cur = check_status( cfn_client, cfn_stack_name )
    if status_cur == "CREATE_COMPLETE":
        print ("Stack " + cfn_stack_name + " created successfully.")
    else:
        print ("Failed to create stack " + cfn_stack_name)
        sys.exit(1)

def check_status( cfn_client, cfn_stack_name ):
    stacks = cfn_client.describe_stacks(StackName=cfn_stack_name)["Stacks"]
    stack_val = stacks[0]
    status_cur = stack_val["StackStatus"]
    print ("Current status of stack " + stack_val["StackName"] + ": " + status_cur)
    for ln_loop in range(1, 9999):
        if "IN_PROGRESS" in status_cur:
            print ("\rWaiting for status update(" + str(ln_loop) + ")...",)
            time.sleep(5) # pause 5 seconds
            try:
                stacks = cfn_client.describe_stacks(StackName=cfn_stack_name)["Stacks"]
            except:
                print (" ")
                print ("Stack " + stack_val["StackName"] + " no longer exists")
                status_cur = "STACK_DELETED"
                break
            stack_val = stacks[0]
            if stack_val["StackStatus"] != status_cur:
                status_cur = stack_val["StackStatus"]
                print (" ")
                print ("Updated status of stack " + stack_val["StackName"] + ": " + status_cur)
        else:
            break
    return status_cur 

if __name__ == "__main__":
    main()
 