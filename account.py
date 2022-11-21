class Account:

    def __init__(self) -> 'Account':
        self.ip = ""
        self.pwd = ""
        self.user = ""
        self.db_pwd = ""
        self.branch = ""

    @staticmethod
    def of(fileBody: 'str') -> 'Account':
        parsedBody = fileBody.splitlines()
        response = Account()
        response.user = parsedBody[0]
        response.ip = parsedBody[1]
        response.pwd = parsedBody[2]
        response.db_pwd = parsedBody[3]
        response.branch = parsedBody[4]

        return response

    def __str__(self) -> 'str':
        return self.user+"@"+self.ip

class Command:

    def __init__(self,command:'str',duration:'float'=1.0) -> 'Command':
        self.command = command
        self.duration = duration

    def __str__(self) -> 'str':
        return self.command+"\n"

    @staticmethod
    def toArray(fileBody: 'str') -> 'list[Command]':
        commands = list()
        
        for command in fileBody.splitlines():
            props = command.split(':')
            commandBody = props[1].split(',')
            req = False
            
            if(props[0] == 'M1'):
                req = True

            response = Command(commandBody[0],req,commandBody[1])

            commands.append(response)


        return commands