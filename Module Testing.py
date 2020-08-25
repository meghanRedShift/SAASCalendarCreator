from flask import Flask, request, make_response

app = Flask(__name__)

#Import relevant libraries
from ics import Calendar, Event
import datetime

#Create calendar
c = Calendar()
options=[]
'''
class cal:
  def __init__(self, calendar):
    self.calendar = calendar

c = cal(Calendar())
'''
#The time (mins and hours) and duration of each period listed on the block schedule
hrs = [15,16,17,17,17,18,18,19,20,20,21,22,22]
mins = [45,00,00,15,30,30,45,30,30,45,00,00,15]
dur = [15,60,15,15,60,15,45,60,15,15,60,15,30]
#creates a 4 day week in calendar using the provided list of course names and week start date
def create4DayWeek(courseNames, options, y, m, d,):
    if 'mAdvisory' in options:
        mAdvisory = 'Advisory/Community Flex Time'
    else:
        mAdvisory = ""
    if 'breaks' in options:
        breaks='Break'
    else:
        breaks=""
    if 'lunch' in options:
        lunch="Lunch"
    else:
        lunch=""
    if 'conferencing' in options:
        conferencing = 'Conferencing'
        print("found conferencing")
    else:
        conferencing = ""
    
    #List of names for each event depending on whether the day is even or odd schedule
    evenNames = [mAdvisory, courseNames[0], courseNames[0] + " Flex", breaks,
                 courseNames[2], courseNames[2] + " Flex", lunch, courseNames[4], courseNames[4] +
                 " Flex", breaks, courseNames[6], courseNames[6] + " Flex", conferencing]
    oddNames = [mAdvisory, courseNames[1], courseNames[1] + " Flex", breaks,
                 courseNames[3], courseNames[3] + " Flex", lunch, courseNames[5], courseNames[5] +
                 " Flex", breaks, courseNames[7], courseNames[7] + " Flex", conferencing]
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

create4DayWeek(["","", "", "", "","","",""], ["mAdvisory","breaks"], 2019, 9, 8,)
