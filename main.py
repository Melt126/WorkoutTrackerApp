import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.widget import Widget
from kivy.uix.button import Button 
from kivy.properties import ObjectProperty


from kivy.uix.popup import Popup
from kivy.uix.label import Label


from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.floatlayout import FloatLayout
#from tkinter import *
from time import strftime
import time
from datetime import datetime, timedelta
from kivy.clock import Clock
from kivy.properties import NumericProperty
from database import DataBase
import read
import src

def createbtn(self, Text,sizeHintx,sizeHinty, posX,posY):
    
    self.btn=Button(text=Text,background_color=(1,1,1,1), size_hint=(sizeHintx, sizeHinty), pos_hint={"x":posX,"y":posY}, on_release= self.release)
    self.add_widget(self.btn)


class MainWindow(Screen):

    def workoutBtn(self):
        read.startWorkout()
        nextPage(self)


def nextPage(self):
    global currentNode
    if currentNode.next:
        currentNode=currentNode.next
        sm.transition.direction="left"
        sm.current=currentNode.data
    else:
        print("No next page available")

def prevPage(self):
    global currentNode
    if currentNode.prev:
        currentNode=currentNode.prev
        sm.transition.direction= "right"
        sm.current=currentNode.data



class MuscleWindow(Screen):
    numProp= NumericProperty(0)
    def add_buttons(self,text):
        self.numProp +=1
        self.new_btn = Button(text=text)
        self.new_btn.bind(on_release=self.release)
        self.ids.button_container.add_widget(self.new_btn)
        
    def remove_buttons(self):
        for btn in self.ids.button_container.children:
            try:
                self.ids.button_container.remove_widget(btn)
            except:
                print("no more buttons")
    def muscleGroup(self,muscleGroup):
        PickWorkout.muscle=muscleGroup
        sm.current="workout"
    
        self.canvas.clear()
    def on_pre_enter(self):
        self.remove_buttons()
        for i in range(len(muscleGroups)):
            self.add_buttons(muscleGroups[i])

    def on_leave(self):
        self.remove_buttons()
        self.remove_buttons() # I can't believe I have to callt his method twice, but here we are
        return super().on_leave()
    
    def release(self, instance):
            sm.transition.direction = "left"
            PickWorkout.muscle=instance.text
            Log.muscle=instance.text
            nextPage(self)

    def back(self):
        prevPage(self)



class PickWorkout(Screen):
    
    group= ObjectProperty(None)
    prev= ObjectProperty(None)
    muscle=""
    button_container=ObjectProperty(None)
    numProp=NumericProperty(0)

    def add_buttons(self,text):
        self.numProp +=1
        self.new_btn = Button(text=text)
        self.new_btn.font_size = 11
        self.new_btn.bind(on_release=self.release)
        self.ids.button_container.add_widget(self.new_btn)

    def remove_buttons(self):
        for btn in self.ids.button_container.children:
            try:
                self.ids.button_container.remove_widget(btn)
            except:
                print("no more buttons")
    def on_pre_enter(self):
        
        self.remove_buttons()




        self.group.text=self.muscle

        layout=BoxLayout(orientation= "vertical")

        HB= BoxLayout(orientation="horizontal")
        VB= BoxLayout(orientation= "vertical")


        workouts=[]
        #self.group.text = self.muscle
        workouts=db.getWorkouts(self.muscle,db.allExcercises)
        self.h=self.height*.9
        yInc=0
        for i in range(len(workouts)):
            self.h=self.h -self.height*.1
            if(i%2==0): 
                posX=.15
                if(i!=0): yInc+=1
            else: posX=.55
            self.add_buttons(workouts[i])

    def on_leave(self):
        self.remove_buttons()
        self.remove_buttons() # I can't believe I have to callt his method twice, but here we are
        return super().on_leave()
    
    def release(self,instance):
        sm.transition.direction="left"
        Log.workout=instance.text
        nextPage(self)

    def back(self):
        prevPage(self)

class TimeInfo(Screen):
    min = ObjectProperty(None)
    sec = ObjectProperty(None)
    def on_pre_enter(self):
        pass
    def toLog(self):
        totalTime=0

        if(self.min.text!=""):
            try:
                minutes= int(self.min.text)
            except:
                return
            if(minutes>=60 or minutes<0):
                return
            totalTime+=60*minutes

        if(self.sec.text!=""):
            try:
                seconds= int(self.sec.text)
            except:
                return
            if(seconds>=60 or seconds<0):
                return
            totalTime+=seconds

        Log.countDown=totalTime
        Log.OGtime=totalTime
        nextPage(self)
    def back(self):
        prevPage(self)


class Log(Screen):
    running=False
    dateLogged=False
    sameWorkout=True
    prevWorkout=""
    prevMuscle=""
    rFest= ObjectProperty(None)
    title = ObjectProperty(None)
    weight = ObjectProperty(None)
    tog = ObjectProperty(None)
    showTime= ObjectProperty(None)
    weightReps= ObjectProperty(None)
    countDown=0
    OGtime=0
    workout=""
    muscle=""
    weight= ObjectProperty(None)
    reps= ObjectProperty(None)

    def on_pre_enter(self):
        m=int(self.countDown/60)
        s=int(self.countDown%60)
        self.title.text=self.workout
        self.showTime.text="{:02d}:{:02d}".format(m,s)

    def start(self):
        cd_time=self.countDown
        m=int(cd_time/60)
        s=int(cd_time%60)
        self.delta=datetime.now() + timedelta(minutes=m,seconds=s+1)
        self.ids.tog.text="Pause"
        if not self.running:
            self.running= True
            Clock.schedule_interval(self.begin, 0.05)

    def reset(self):
         
        m=int(self.OGtime/60)
        s=int(self.OGtime%60)
        self.ids.tog.text= "Start"
        self.ids.showTime.text= "{:02d}:{:02d}".format(m,s)
        self.pause()

    def pause(self):
        if self.running:
            self.running=False
            Clock.unschedule(self.begin)

    def begin(self,cd_start):
        delta=self.delta-datetime.now()
        delta= str(delta)
        self.ids.showTime.text=delta[2:7]
        if delta[2:7] == "00:00":
            self.reset()

    def toggle(self):
        if self.running:
            self.pause()
        else:
            m=int(self.countDown/60)      
            s=int(self.countDown%60)
            startingTime= "{:02d}:{:02d}".format(m,s)
            if(self.ids.showTime.text!=startingTime):      #NOT GETTING INTO IF STATEMENT
                #self.delta=datetime.now() + timedelta(minutes=m,seconds=s+1)
                self.delta=datetime.now() + timedelta(minutes=m,seconds=s)
                self.countDown= int(self.ids.showTime.text[0:1])*60+int(self.ids.showTime.text[3:])
                self.start()
            self.start()
    def back(self):
        prevPage(self)
    def on_leave(self):
        self.reset()

    def loggingWorkout(self):
        if(self.prevWorkout==""):
            read.logWorkout([[self.workout]])
            self.prevWorkout=self.workout
        elif(self.prevWorkout==self.workout):
            pass
        else:
            read.logWorkout([[self.workout]])
            self.prevWorkout=self.workout
            read.currentRow=read.startingRow
        self.workout
    def loggingMuscle(self):
        if(self.prevMuscle==""):
            read.logMuscleGroup([[self.muscle]])
            self.prevMuscle=self.muscle
        elif(self.prevMuscle==self.muscle):
            pass
        else:
            read.logMuscleGroup([[self.muscle]])
            self.prevMuscle=self.muscle
            read.currentRow=read.startingRow
    def logBtn(self):
                        
        w=0
        if(self.ids.weight.text!=""):
            try:
                w= float(self.ids.weight.text)
            except:
                return
        try:
            r= int(self.ids.reps.text)
        except:
            return
        if(w==0):
            stringtoLog=(f"{r}")
        else:
            if (w== int(w)):
                stringtoLog=(f"{int(w)}--{r}")
            else:
                stringtoLog=(f"{w}--{r}")            
        self.ids.weight.text=""
        self.ids.reps.text=""
        print(self.muscle, " ", self.workout)
        print(stringtoLog)
        if(read.currentCol!="A"):
            self.dateLogged=True

        if (self.dateLogged== False):
            date=src.getDate()
            read.logDate([[date]])
            self.dateLogged=True

        self.loggingMuscle()
        self.loggingWorkout()
        read.logWeightReps([[stringtoLog]])

    #now I need to add function that actually logs information

class WindowManager(ScreenManager):
    pass

sm= WindowManager()
db =DataBase("workouts.txt")
kv=Builder.load_file("my.kv")


muscleGroups=["Shoulder","Tricep","Chest", "Back"]
muscleGroups=db.getMuscleGroups(db.allExcercises)
screens= [MainWindow(name="ready"), MuscleWindow(name="muscle"), PickWorkout(name="workout"),TimeInfo(name="timeInfo"), Log(name="log")]

class Node:
    prev=None
    next=None
    def __init__(self, data=None):
        self.data = data


class doublyLinkedWindow:
    def __init__(self):
        self.start_node= None
    def insertToEnd(self,data):
        if self.start_node is None:
            new_node=Node(data)
            self.start_node=new_node
            return
        n = self.start_node
        while n.next is not None:
            n=n.next
        new_node=Node(data)
        n.next = new_node
        new_node.prev=n

linkedScreen = doublyLinkedWindow()
for screen in screens:
    sm.add_widget(screen)
    linkedScreen.insertToEnd(screen.name)
    
currentNode=linkedScreen.start_node
sm.current=currentNode.data


class MyMainApp(MDApp):
    def build(self):
        global currentNode
        self.theme_cls.theme_style="Dark"
        return sm
    
if __name__== "__main__":
    MyMainApp().run()