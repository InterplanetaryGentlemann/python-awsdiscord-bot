#Import Discord Interactions Py Library
import interactions

#Import the OS and DotEnv libraries to safely load tokens
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TOKEN=os.getenv("DISCORD_TOKEN")
GUILD=os.getenv("GUILD_TOKEN")

#Set the bot
bot = interactions.Client(token=TOKEN)


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