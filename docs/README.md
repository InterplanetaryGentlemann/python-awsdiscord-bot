## TO-DO
* Flesh out readme
* Create wiki to walk users through bot setup
* Finish Boto3 functions in lambda_function
* split into two versions? One Minecraft specific and one as an empty template?
* CloudFormation Templates

## AWS Instance Bot
This is a project started out of a desire to host multiplayer game servers for friends. I have a small discord server where we chat and do various game nights, but certain games are better or just flat out require that you host a private server for playing with friends.

Currently, I host these servers in the AWS Cloud. However, these servers do not have huge player bases and access to them is infrequent at best. I do not need these servers to be on 24/7, nor do I want to pay for them to be that available.

The easy solution with the cloud is to just pay for what you use, shut the server down while nobody plays, and only pay for when people are playing. The problem here is that I am not always available to start the servers up when other people want to play. Not everyone I play with is tech savvy enough to want to learn/use AWS and I don't neccessarily want to start making a bunch of IAM users for people to mess with my AWS environment.

## What it does
The Solution for me was to create this Discord Bot to run on our server. This bot runs serverless as lambda function called via an API Gateway, allowing the bot to only run when a command is called in the Discord Server.

Currently, this bot is designed to:
* Get a list of availabe EC2 Instances based on tags
* Get the current state of a specified instance
* Start, Restart, or Stop a specified instance

Breakdown of commands:
*/aws-list
** Generates a list of all the instances the bot can currently see
*/aws-status -instance ''
** Gets the current state of the instance specified in the 'instance' parameter
*/aws-start -instance ''
** Starts the instance specified in the instance option
*/aws-stop -instance ''
** Stops the instanc especified in the instance option
*/aws-restart -instance ''
** Restarts the instance specified in the instance option
