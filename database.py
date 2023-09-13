import datetime

class DataBase:
    
    def __init__(self, filename):
        self.filename = filename
        self.users = None
        self.file = None
        self.allExcercises=None
        self.muscleGroups=None
        self.load()
        

    def load(self):
        self.file = open(self.filename, "r")
        self.users = {}
        self.allExcercises=[]
        self.muscleGroups=[]
        i=0
        for line in self.file:
            excercises=[]
            excercises=line.strip().split(";")
            self.allExcercises.append(excercises)
            i+=1
        self.file.close()

    def getWorkouts(self, muscle,allExcercises):
            
            for i in allExcercises:
                 if i[0] == muscle:
                    return i[1:]
    def getMuscleGroups(self,line):
         
         for i in line:
             self.muscleGroups.append(i[0])
         return self.muscleGroups