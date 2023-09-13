from datetime import datetime, timedelta
import string
#def startWorkout():
    #date=datetime.now().date()
    #return date.strftime("%m/%d/%Y")

def getDate():
    date=datetime.now().date()  
    return date.strftime("%m/%d/%Y")       #return date in month/day/year format

def getColRow(inc):  #return values for col and row
    with open("sheetinfo.txt","r") as file:
        lines=file.readlines()
    starting_col = lines[0].strip().split(";")[1]
    starting_row = lines[1].strip().split(";")[1]
    furthest_row = int(lines[3].strip().split(";")[1])
    #if true, increment row
    if (inc==True):                 
        lines[1] = f"startingRow;{furthest_row+1}\n"
        lines[3] = f"furthestRow;{furthest_row+1}"
        with open("sheetinfo.txt","w") as file:
            file.writelines(lines)
    #return new values

        values=[starting_col,furthest_row+1]
        return values
    values=[starting_col,starting_row]
    return values

def getStartingRow():   #return startinRow from txt file
    with open("sheetinfo.txt", "r") as file:
        lines=file.readlines()
    startingRow=lines[1].strip().split(";")[1]
    return startingRow

def getFurthestCol():   #return furthest col from txt file
    with open("sheetinfo.txt", "r") as file:
        lines=file.readlines()
    furthestCol=lines[2].strip().split(";")[1]
    return furthestCol


def incFurthestCol():   #incremenet furthest col in file 
    with open("sheetinfo.txt", "r") as file:
        lines=file.readlines()
    furthestCol=lines[2].strip().split(";")[1]
    #column_index = string.ascii_uppercase.index(furthestCol)
    #column_index += 1  
    #furthestCol = string.ascii_uppercase[column_index]
    asc_val= ord(furthestCol)
    asc_val+=1
    furthestCol= chr(asc_val)
    lines[2] = f"furthestCol;{furthestCol}\n"
    with open("sheetinfo.txt","w") as file:
        file.writelines(lines)

def resetFurthestCol():     #set furthset col in file to A
    with open("sheetinfo.txt", "r") as file:
        lines=file.readlines()

    lines[2]="furthestCol;A\n"
    with open("sheetinfo.txt", "w") as file:
        file.writelines(lines)

#used for going left in google sheet
def decCol(char):       #decremenet a char
    asc_val= ord(char)
    asc_val-=1
    char= chr(asc_val)
    return char