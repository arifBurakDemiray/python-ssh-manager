# python-ssh-manager
Ssh manager via paramiko. Sends commands and waits for the results

To send commands with this tool please use one liner versions of the commands 

like sudo git -c credential.helper='!f() { echo "password=GIT_PWD"; echo "username=GIT_NAME";}; f' pull origin
