#Import Discord Interactions Py Library
import interactions

#Import boto3 AWS Library
import boto3
from botocore.exceptions import ClientError

#Import the OS and DotEnv libraries to safely load tokens
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TOKEN=os.getenv("DISCORD_TOKEN")
GUILD=os.getenv("GUILD_TOKEN")

#Set the bot
bot = interactions.Client(token=TOKEN)

#Creates a Lambda Handler for the code, Yay!
def lambda_handler(event, context):

    #AWS Vars for getting/setting instances
    #instance_id='' Need some method of getting AWS Instance ID's with a certian tag
    #region='' Need some method of setting the region, would be fine to set manually
    #ec2 = boto3.client('ec2')

    #Startup Event
    @bot.event
    async def on_ready():
        print("Ready!")


    #Start Command, Starts the specified instance
    @bot.command(
        name="aws-start",
        description="Starts an EC2",
        scope=GUILD
    )
    async def aws_start(ctx: interactions.CommandContext):
         await ctx.send("Starting specified instance")
       

    #Stop Command, Stops the specified instance
    @bot.command(
        name="aws-stop",
        description="Stops an EC2",
        scope=GUILD

    )
    async def aws_stop(ctx: interactions.CommandContext):
         await ctx.send("Stopping specified instance")

        # #Gets the instance state and checks to ensure it's

        # resp = ec2.describe_instance_status(
        #     InstanceIds=[str(instance_id)],
        #     IncludeAllInstances=True)

        #  #print("Response = ",resp)

        # instance_status = resp['InstanceStatuses'][0]['InstanceState']['Code']

        #  #print("Instance status =", instance_status)

    #Status Command, Shows the specified instances status
    @bot.command(
        name="aws-status",
        description="Shows the status of an EC2 Instance",
        scope=GUILD

    )
    async def aws_status(ctx: interactions.CommandContext):
        #AWS EC2 Code goes in this function
        await ctx.send("Instance is ")

    #Start Command, Starts the specified instance
    @bot.command(
        name="aws-restart",
        description="Restarts an EC2",
        scope=GUILD
    )
    async def aws_restart(ctx: interactions.CommandContext):
        #AWS EC2 Code goes in this function
        await ctx.send("Restarting specified instance")

    bot.start()