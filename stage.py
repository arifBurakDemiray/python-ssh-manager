class StageWriter:

    def __init__(self, max:'int') -> 'StageWriter':
        self.max = max
        self.current = 1

    def next(self,message: 'str') -> None:
        if(self.current>self.max):
            print("Please update your max stage size")
            return

        print("-----------------------------------------------------------")
        print("["+str(self.current)+"/"+str(self.max)+"] - "+message)        
        print("-----------------------------------------------------------")
        self.current+=1
