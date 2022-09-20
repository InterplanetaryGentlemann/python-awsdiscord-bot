#Import Discord Interactions Py Library
import interactions

#Import boto3 AWS Library
import boto3
from botocore.exceptions import ClientError

#Set the bot
bot = interactions.Client("MTAyMTMxMzM4MTM5NjkyNjU3NA.GQNCiS.nvGGopw2wILn6RwK04ACnp2AzcoyW0qWBwOQiY")

#Set the EC2 Service
ec2 = boto3.client('ec2')

#Creates a Lambda Handler for the code, Yay!
def lambda_handler(event, context):

    #AWS Vars for getting/setting instances
    #instance_id='' Need some method of getting AWS Instance ID's with a certian tag
    #region='' Need some method of setting the region, would be fine to set manually

    #Temporary Static Vars
    instance_id=''
    region=''

    #Startup Event
    @bot.event
    async def on_ready():
        print("Ready!")


    #Start Command, Starts the specified instance
    @bot.command(
        name="aws-start",
        description="Starts an EC2",
        scope=268602082695577601
    )
    async def aws_start(ctx: interactions.CommandContext):
         await ctx.send("Starting specified instance")
        
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
       

    #Stop Command, Stops the specified instance
    @bot.command(
        name="aws-stop",
        description="Stops an EC2",
        scope=268602082695577601,

    )
    async def aws_stop(ctx: interactions.CommandContext):
        #AWS EC2 Code goes in this function
        await ctx.send("Stopping specified instance")

        #Gets the instance state and checks to ensure it's

        resp = ec2.describe_instance_status(
            InstanceIds=[str(instance_id)],
            IncludeAllInstances=True)

         #print("Response = ",resp)

        instance_status = resp['InstanceStatuses'][0]['InstanceState']['Code']

         #print("Instance status =", instance_status)

        if instance_status == 16:
            #Do the stopping process

    #Status Command, Shows the specified instances status
    @bot.command(
        name="aws-status",
        description="Shows the status of an EC2 Instance",
        scope=268602082695577601,

    )
    async def aws_status(ctx: interactions.CommandContext):
        #AWS EC2 Code goes in this function
        await ctx.send("Instance is ")

    #Start Command, Starts the specified instance
    @bot.command(
        name="aws-restart",
        description="Restarts an EC2",
        scope=268602082695577601
    )
    async def aws_restart(ctx: interactions.CommandContext):
        #AWS EC2 Code goes in this function
        await ctx.send("Restarting specified instance")

    bot.start()