import os
from stage import StageWriter
from color import Color
from account import Account,Command
from paramiko import SSHClient,AutoAddPolicy,Channel
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from helper import BANNER,froze





def get_server_files() -> 'list[str]':
    files = os.listdir("context")
    serverFiles = list()

    for serverFile in files:
        if(serverFile.endswith(".server.str") and serverFile.count(".")==2):
            serverFiles.append(serverFile)


    return serverFiles


def get_commands(account:'Account') -> 'list[Command]':
    load_dotenv(find_dotenv())

    git_name = os.environ.get("GIT_USERNAME")
    git_pwd = os.environ.get("GIT_ACCESS_KEY")

    commands = [
                Command('sudo git -c credential.helper=\'!f() { echo "password='+git_pwd+'"; echo "username='+git_name+'";}; f\' pull origin '+account.branch),
                Command('sudo ./build_deploy.sh',75)] #Example commands

    return commands


def get_results(commands:'list[Command]',channel:'Channel') -> 'None':
    for command in commands:
        channel.send(str(command))
        while not channel.recv_ready(): #Wait for the server to read and respond
            froze()
        froze() #wait enough for writing to (hopefully) be finished
        output = channel.recv(9999) #read in
        print(output.decode('utf-8'))
        if(command.duration > 5):
            start = datetime.utcnow()
            try:
                while((datetime.utcnow() - start).seconds <= command.duration*3):
                    froze()
                    output = channel.recv(9999) #read in
                    print(output.decode('utf-8'))
            except KeyboardInterrupt:
                break

def main() -> 'None':
    BANNER()

    stageWriter = StageWriter(3)
    stageWriter.next(f"{Color.B_GREEN}Server selection stage{Color.OFF}")

    ##########################################################################

    serverFiles = get_server_files()

    option = 0
    for f in serverFiles:
        print("["+str(option)+"]: "+f)
        option+=1

    option = int(input("Please select server: "))
    ##########################################################################
    stageWriter.next(f"{Color.B_GREEN}Connection stage{Color.OFF}")
    file = open("context/"+serverFiles[option],'r')
    account = Account.of(file.read())
    file.close()


    try:
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(hostname=account.ip,
                    username=account.user,
                    password=account.pwd,
                    allow_agent=False)

        channel = ssh.invoke_shell()
        print('Connection success')
    except:
        print('Unsuccessfull connection')
        exit(1)

    ##########################################################################
    stageWriter.next(f"{Color.B_GREEN}Deployment stage{Color.OFF}")

    commands = get_commands(account)

    get_results(commands,channel)


    ssh.close()

    print('Bye')
    BANNER()


if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Bye')
        BANNER()