def aws_start():
    return 'Starting Instance!'

def aws_stop():
    return 'Stopping Instance!'

def aws_restart():
    return 'Starting Instance!'
commands = {
    'aws-start':aws_start(), 'aws-stop':aws_stop(), 'aws-restart':aws_restart()
}

print(commands['aws-start'])