#Import relevant libraries
from ics import Calendar, Event
import datetime

#Create calendar
c = Calendar()

#The time (mins and hours) and duration of each period listed on the block schedule
hrs = [15,16,17,17,17,18,18,19,20,20,21,22,22]
mins = [45,00,00,15,30,30,45,30,30,45,00,00,15]
dur = [15,60,15,15,60,15,45,60,15,15,60,15,30]

#creates a 4 day week in calendar using the provided list of course names and week start date
def create4DayWeek(courseNames, y, m, d):
    #List of names for each event depending on whether the day is even or odd schedule
    evenNames = ["Advisory/Community Flex Time", courseNames[0], courseNames[0] + " Flex", "Break",
                 courseNames[2], courseNames[2] + " Flex", "Lunch", courseNames[4], courseNames[4] +
                 " Flex", "Break", courseNames[6], courseNames[6] + " Flex", "Conferencing"]
    oddNames = ["Advisory/Community Flex Time", courseNames[1], courseNames[1] + " Flex", "Break",
                 courseNames[3], courseNames[3] + " Flex", "Lunch", courseNames[5], courseNames[5] +
                 " Flex", "Break", courseNames[7], courseNames[7] + " Flex", "Conferencing"]
    #The outer loop makes this run for each day of the week
    for z in range(1,5):
        #Chooses which set of names to use based on whether it is an even or odd day of the schedule
        if (z%2==0):
            names = evenNames
        else:
            names = oddNames
        #The inner loop makes this run for each class in the day
        for x in range(len(hrs)):
            #if statement make it so events are only created for named courses
            if (names[x] != "" and names[x] != " Flex"):
                #creates datetime for a class
                beg= datetime.datetime(y, m, d, hrs[x], mins[x])
                #Adjusts date using z. This is in a separate statement so that the
                #added day makes the month roll over if necessary
                beg +=datetime.timedelta(days=z-1)
                #Creates calendar event
                e=Event(name=names[x], begin=beg, duration={"minutes":dur[x]})
                #Adds event to calendar
                c.events.add(e)
                c.events
        
    #Prints calendar file to console
    print(str(c))
    #Saves calendar file to console
    #I just keep writing to the same calendar. Haven't had issues with this but it could possibly cause issues.
    open('my.ics', 'w').writelines(c)

#creates a 4 day week in calendar using the provided list of course names and week start date
def create5DayWeek(courseNames, y, m, d):
    #List of modified durations for long days on 5 day schedule
    dur5 = [15,60,15,15,60,15,45,60,15,15,105]
    #List of names for each event depending on the day of the week
    mNames = ["Advisory/Community Flex Time", courseNames[0], courseNames[0] + " Flex", "Break",
                 courseNames[2], courseNames[2] + " Flex", "Lunch", courseNames[4], courseNames[4] +
                 " Flex", "Break", courseNames[6], courseNames[6] + " Flex", "Conferencing"]
    tNames = ["Advisory/Community Flex Time", courseNames[1], courseNames[1] + " Flex", "Break",
                 courseNames[5], courseNames[5] + " Flex", "Lunch", courseNames[7], courseNames[7] +
                 " Flex", "Break", "Conferencing"]
    wNames = ["Advisory/Community Flex Time", courseNames[3], courseNames[3] + " Flex", "Break",
                 courseNames[4], courseNames[4] + " Flex", "Lunch", courseNames[6], courseNames[6] +
                 " Flex", "Break", "Conferencing"]
    thNames = ["Advisory/Community Flex Time", courseNames[0], courseNames[0] + " Flex", "Break",
                 courseNames[2], courseNames[2] + " Flex", "Lunch", courseNames[5], courseNames[5] +
                 " Flex", "Break", "Faculty Collaboration"]
    fNames = ["Advisory/Community Flex Time", courseNames[1], courseNames[1] + " Flex", "Break",
                 courseNames[3], courseNames[3] + " Flex", "Lunch", courseNames[7], courseNames[7] +
                 " Flex", "Break", "Conferencing"]
    #The outer loop makes this run for each day of the week
    for z in range(1,6):
        #Chooses which set of names and durations to use based the day of the week
        if (z==1):
            names = mNames
            duration = dur
        elif (z==2):
            names = tNames
            duration = dur5
        elif (z==3):
            names = wNames
            duration = dur5
        elif (z==4):
            names = thNames
            duration = dur5
        else:
            names = fNames
            duration = dur5
        #The inner loop makes this run for each class in the day
        for x in range(len(names)):
            #if statement make it so events are only created for named courses
            if (names[x] != "" and names[x] != " Flex"):
                #creates datetime for a class
                beg= datetime.datetime(y, m, d, hrs[x], mins[x])
                #Adjusts date using z. This is in a separate statement so that the
                #added day makes the month roll over if necessary
                beg +=datetime.timedelta(days = z-1)
                #Creates calendar event
                e=Event(name=names[x], begin=beg, duration={"minutes":duration[x]})
                #Adds event to calendar
                c.events.add(e)
                c.events
        
    #Prints calendar file to console
    print(str(c))
    #Saves calendar file to console
    #I just keep writing to the same calendar. Haven't had issues with this but it could possibly cause issues.
    open('my.ics', 'w').writelines(c)

#Runs code for the dates of the first half of the fall trimester
def fallMidterm1Weeks():
    create4DayWeek(["Block 1","Block 2","Block 3","Block 4", "Block 5", "Block 6", "Block 7", "Block 8"], 2020, 9, 8)
    create5DayWeek(["Block 1","Block 2","Block 3","Block 4", "Block 5", "Block 6", "Block 7", "Block 8"], 2020, 9, 14)
    create5DayWeek(["Block 1","Block 2","Block 3","Block 4", "Block 5", "Block 6", "Block 7", "Block 8"], 2020, 9, 21)
    create4DayWeek(["Block 1","Block 2","Block 3","Block 4", "Block 5", "Block 6", "Block 7", "Block 8"], 2020, 9,29)
    create4DayWeek(["Block 1","Block 2","Block 3","Block 4", "Block 5", "Block 6", "Block 7", "Block 8"], 2020, 10,5)

def guidedFallMidterm1Weeks():
    courses = []
    print("Please enter the name of each of your courses as you are prompted. If you do not have a course for a given block please press enter without typing anything.")
    for x in range(1,9):
        name = input("Please enter the name of the course you have for Block " + str(x) + ":")
        courses.append(name)
    create4DayWeek(courses, 2020, 9, 8)
    create5DayWeek(courses, 2020, 9, 14)
    create5DayWeek(courses, 2020, 9, 21)
    create4DayWeek(courses, 2020, 9,29)
    create4DayWeek(courses, 2020, 10,5)

guidedFallMidterm1Weeks()
