from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, timedelta
import src
import string
from database import DataBase
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY=os.getenv("API_KEY")    # The ID of spreadsheet.
KEYS=os.getenv("KEYS")
SCOPE=os.getenv("SCOPE")

SAMPLE_SPREADSHEET_ID = API_KEY
SERVICE_ACCOUNT_FILE=KEYS
SCOPES = [SCOPE]

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)




service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
#result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                   #range="sheet2!A1:B24").execute()
#values = result.get('values', [])

#global variables that change depending on which methods are called
global currentCol
global currentRow
global startingRow
global nextCol
global prevMuscle
global prevExcercise

currentCol="A"
currentRow=1
startingRow=currentRow
furthestCol="A"
prevExcercise=""          
prevMuscle=""
#result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    #range="sheet2!A1:B24").execute()

#when start button is pressed
def startWorkout():
        global currentCol
        global currentRow
        global startingRow
        global furthestCol
        global prevMuscle
        global prevExcercise
        print("in start")
        colAndRow=[]
        colAndRow=src.getColRow(False) #get starting col and row
        col=colAndRow[0]
        row=colAndRow[1]
        #check if there is a date in starting cell
        try:
                date = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=f"fromScript!{col}{row}").execute()
                if "values" in date and date["values"]:
                        sheetValue=date["values"][0][0]
                else:
                        sheetValue=None
        except Exception as e:
                print(f"An error occured: {e}")
                sheetValue=None
                                                                                       
        currentDate=src.getDate()

        if(currentDate==sheetValue):                    #if re-entering application the same day
                #find out which col they left on
                currentCol=src.getFurthestCol()
                furthestCol=currentCol
                currentRow=int(src.getStartingRow())    #get starting Row
                #store the last inputted excercise and muslce to prevent out putting uneccesary information
                prevExcercise=getLastExcercise()
                prevMuscle=getLastMuscle()
                #add something to detect previous workout and excercise
                
        else:   #its a new day
                colAndRow=src.getColRow(sheetValue!=None) #If this isn't the first date on sheet, change row according to furthest row in txt
                currentRow=int(colAndRow[1])                  
                startingRow=currentRow
                src.resetFurthestCol()  #reset furthest col

def incremenet_col(current_col):  #incremenet col
        col_number = ord(current_col) - ord('A')
        col_number += 1
        incremented_col = chr(col_number + ord('A'))
        return incremented_col


def logDate(date):      #log current date
        global currentCol
        global currentRow
        global startingRow
        global furthestCol

        request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,            #output to google sheets
                                range=f"fromScript!{currentCol}{currentRow}", valueInputOption="USER_ENTERED", body={"values":date}).execute()
        #currentCol=incremenet_col(currentCol)

def logMuscleGroup(muscle):     #log muscle group 
        global currentCol
        global currentRow
        global startingRow
        global furthestCol
        global prevMuscle

        startingRow=int(src.getStartingRow())
        if (prevMuscle==muscle[0][0]):  #don't output if the prev muscle group is the same as current
                return
        else:
                prevMuscle=muscle       #if new muscle in input
                #update col and row values
                currentCol=incremenet_col(currentCol)
                src.incFurthestCol()    
                currentRow=startingRow
                request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,  #output to google sheets
                                range=f"fromScript!{currentCol}{currentRow}", valueInputOption="USER_ENTERED", body={"values":muscle}).execute()
        

def logWorkout(workout):
        global currentCol
        global currentRow
        global startingRow
        global furthestCol
        global prevExcercise

        startingRow=int(src.getStartingRow())

        if (prevExcercise==workout[0][0]):      #don't output if prev excercise if the same as current
                fixNextRow(src.getFurthestCol())        #find out what row to output to
                return
        #update values
        prevExcercise=workout
        currentRow=startingRow
        currentCol=incremenet_col(currentCol)
        src.incFurthestCol()
        request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,                    #output to google sheets
                                range=f"fromScript!{currentCol}{currentRow}", valueInputOption="USER_ENTERED", body={"values":workout}).execute()
        

def logWeightReps(weightReps):
        global currentRow
        global currentRow
        global startingRow
        global furthestCol

        currentRow+=1 #go down in google sheets
        #should've done all of this in a method for cleanliness
        with open("sheetinfo.txt","r") as file:         
                lines=file.readlines()
        #store furthestRow
        furthestRow=int(lines[3].strip().split(";")[1]) 
        if (currentRow>furthestRow):                    #incrmements furthestrow is need be
                furthestRow=currentRow
                lines[3]=f"furthestRow;{furthestRow}"
                with open("sheetinfo.txt","w") as file:
                        file.writelines(lines)
        request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,                    #output to google sheets
                                range=f"fromScript!{currentCol}{currentRow}", valueInputOption="USER_ENTERED", body={"values": weightReps}).execute()


def getLastExcercise():         #return last input excercise
        row=int(src.getStartingRow())
        col=src.getFurthestCol()
        #reads value in google sheet cells
        try:
                excercise=sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=f"fromScript!{col}{row}").execute()
                if "values" in excercise and excercise["values"]:
                        cellValue=excercise["values"][0][0]
                else: cellValue=None
        except Exception as e:
                print(f"An error occured: {e}")
                cellValue=None
        return cellValue

def getLastMuscle():    #return last mucle group inputted
        db =DataBase("workouts.txt")
        muscleGroups=[]
        muscleGroups=db.getMuscleGroups(db.allExcercises)       #store all musle groups in array
        row=int(src.getStartingRow())
        col=src.getFurthestCol()
        while(col!="A"):        #until it reaches beginning of sheet
                
                try:    #read cell value if it can
                        muscle=sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                range=f"fromScript!{col}{row}").execute()
                        if "values" in muscle and muscle["values"]:
                                cellValue=muscle["values"][0][0]
                        else: cellValue=None
                except Exception as e:
                        print(f"An error occured: {e}")
                        cellValue=None
                if cellValue in muscleGroups:   #return value if it's a muscle
                        return cellValue
                col=src.decCol(col)     #decrement col
        return ""       #return empty string if nothing found

def fixNextRow(col):    #get next Row in given col
        global currentRow
        tempRow=int(src.getStartingRow())+1
        #while a cell isn't empty, move down the sheet
        while True:
                cell=sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=f"fromScript!{col}{tempRow}").execute()
                cellValue= cell.get("values", [])
                if cellValue and cellValue[0]:
                        pass
                else:
                        break
                tempRow+=1
        currentRow=tempRow-1
