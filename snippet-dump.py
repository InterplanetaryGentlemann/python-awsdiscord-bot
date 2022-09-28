        #Gets the instance state and checks to ensure it's

         resp = ec2.describe_instance_status(
            InstanceIds=[str(instance_id)],
            IncludeAllInstances=True)

         #print("Response = ",resp)

         instance_status = resp['InstanceStatuses'][0]['InstanceState']['Code']

         #print("Instance status =", instance_status)

         if instance_status == 80:
            #Try a dry run first to test permissions
            try:
                 ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
            except ClientError as e:
                 if 'DryRunOperation' not in str(e):
                     raise

            # Dry run succeeded, run start_instances without dryrun
            try:
                 response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
                 print(response)
            except ClientError as e:
                 print(e)

#Example Script
import boto3
import time

# Defining boto3 the connection
ec2 = boto3.resource('ec2')

def timeInRange(startRange, endRange, currentRange):
    if startRange <= endRange:
        return startRange <= currentRange <= endRange
    else:
        return startRange <= currentRange or currentRange <= endRange

def lambda_handler(event, context):
    
    currentTime = time.strftime("%H:%M")

    filters = [{
            'Name': 'tag:autoSchedulerEnabled',
            'Values': ['True']
        }
    ]

    instances = ec2.instances.filter(Filters=filters)

    stopInstancesList = []
    startInstancesList = []

    for instance in instances:
            
        for tag in instance.tags:

            if tag['Key'] == 'autoStopSchedule':

                stopTime = tag['Value']
                pass

            if tag['Key'] == 'autoStartSchedule':

                startTime = tag['Value']
                pass

            pass

        instanceState = instance.state['Name']

        if timeInRange(startRange=startTime, endRange=stopTime, currentRange=currentTime):

            if (instanceState == "running") or (instanceState == "pending"):
                print("[", currentTime, "]", "Instance", instance.id, "already running, it won't be added to START list")
            else:
                startInstancesList.append(instance.id)
                print("[", currentTime, "]", "Instance", instance.id, "has been added to START list")
                
                pass

        elif timeInRange(startRange=startTime, endRange=stopTime, currentRange=currentTime) == False:

            if (instanceState == "stopped") or (instanceState == "stopping"):
                print("[", currentTime, "]", "Instance", instance.id, "already stopped, it won't be added to STOP list")
            else:
                stopInstancesList.append(instance.id)
                print("[", currentTime, "]", "Instance", instance.id, "has been added to STOP list")
                
                pass

        pass

    if len(stopInstancesList) > 0:
        stop = ec2.instances.filter(InstanceIds=stopInstancesList).stop()
        print(stop)
    else:
        print("[", currentTime, "]", "No instances to stop in the list")

    if len(startInstancesList) > 0:
        start = ec2.instances.filter(InstanceIds=startInstancesList).start()
        print(start)
    else:
        print("[", currentTime, "]", "No instances to start in the list")