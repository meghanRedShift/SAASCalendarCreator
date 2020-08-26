from flask import Flask, request, make_response
import sys

app = Flask(__name__)

#Import relevant libraries
from ics import Calendar, Event
import datetime

#The time (mins and hours) and duration of each period listed on the block schedule
hrs = [15,16,17,17,17,18,18,19,20,20,21,22,22]
mins = [45,00,00,15,30,30,45,30,30,45,00,00,15]
dur = [15,60,15,15,60,15,45,60,15,15,60,15,30]


class cal:
    def __init__(self, courseNames, options):
        self.cal= Calendar()
        self.courseNames = courseNames
        self.options = options

    #creates a 4 day week in calendar using the provided list of course names and week start date
    def create4DayWeek(self):
        if self.options[0]:
            mAdvisory = 'Advisory/Community Flex Time'
        else:
            mAdvisory = ""
        if self.options[1]:
            breaks='Break'
        else:
            breaks=""
        if self.options[2]:
            lunch="Lunch"
        else:
            lunch=""
        if self.options[3]:
            conferencing = 'Conferencing'
        else:
            conferencing = ""
        
        #List of names for each event depending on whether the day is even or odd schedule
        evenNames = [mAdvisory, self.courseNames[0], self.courseNames[0] + " Flex", breaks,
                     self.courseNames[2], self.courseNames[2] + " Flex", lunch, self.courseNames[4], self.courseNames[4] +
                     " Flex", breaks, self.courseNames[6], self.courseNames[6] + " Flex", conferencing]
        oddNames = [mAdvisory, self.courseNames[1], self.courseNames[1] + " Flex", breaks,
                     self.courseNames[3], self.courseNames[3] + " Flex", lunch, self.courseNames[5], self.courseNames[5] +
                     " Flex", breaks, self.courseNames[7], self.courseNames[7] + " Flex", conferencing]
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
                    self.cal.events.add(e)
                    self.cal.events
            
        #Prints calendar file to console
        print(str(self.cal))
        #Saves calendar file to console
        #I just keep writing to the same calendar. Haven't had issues with this but it could possibly cause issues.
        open('my.ics', 'w').writelines(self.cal)

    #creates a 4 day week in calendar using the provided list of course names and week start date
    def create5DayWeek(self):
        if self.options[0]:
            mAdvisory = 'Advisory/Community Flex Time'
        else:
            mAdvisory = ""
        if self.options[1]:
            breaks='Break'
        else:
            breaks=""
        if self.options[2]:
            lunch="Lunch"
        else:
            lunch=""
        if self.options[3]:
            conferencing = 'Conferencing'
        else:
            conferencing = ""
        #List of modified durations for long days on 5 day schedule
        dur5 = [15,60,15,15,60,15,45,60,15,15,105]
        #List of names for each event depending on the day of the week
        mNames = [mAdvisory, self.courseNames[0], self.courseNames[0] + " Flex", breaks,
                     self.courseNames[2], self.courseNames[2] + " Flex", "Lunch", self.courseNames[4], self.courseNames[4] +
                     " Flex", breaks, self.courseNames[6], self.courseNames[6] + " Flex", "Conferencing"]
        tNames = [mAdvisory, self.courseNames[1], self.courseNames[1] + " Flex", breaks,
                     self.courseNames[5], self.courseNames[5] + " Flex", "Lunch", self.courseNames[7], self.courseNames[7] +
                     " Flex", breaks, "Conferencing"]
        wNames = [mAdvisory, self.courseNames[3], self.courseNames[3] + " Flex", breaks,
                     self.courseNames[4], self.courseNames[4] + " Flex", "Lunch", self.courseNames[6], self.courseNames[6] +
                     " Flex", breaks, "Conferencing"]
        thNames = [mAdvisory, self.courseNames[0], self.courseNames[0] + " Flex", breaks,
                     self.courseNames[2], self.courseNames[2] + " Flex", "Lunch", self.courseNames[5], self.courseNames[5] +
                     " Flex", breaks, "Faculty Collaboration"]
        fNames = [mAdvisory, self.courseNames[1], self.courseNames[1] + " Flex", breaks,
                     self.courseNames[3], self.courseNames[3] + " Flex", "Lunch", self.courseNames[7], self.courseNames[7] +
                     " Flex", breaks, "Conferencing"]
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
                    self.cal.events.add(e)
                    self.cal.events
            
        #Prints calendar file to console
        print(str(self.cal))
        #Saves calendar file to console
        #I just keep writing to the same calendar. Haven't had issues with this but it could possibly cause issues.
        open('my.ics', 'w').writelines(self.cal)

    #Runs code for the dates of the first half of the fall trimester
    def fallMidterm1Weeks(blocks):
        create4DayWeek(blocks, 2020, 9, 8)
        create5DayWeek(blocks, 2020, 9, 14)
        create5DayWeek(blocks, 2020, 9, 21)
        create4DayWeek(blocks, 2020, 9,29)
        create4DayWeek(blocks, 2020, 10,5)

    def guidedFallMidterm1Weeks(courses, options):
        create4DayWeek(courses, options, 2020, 9, 8)
        create5DayWeek(courses, options, 2020, 9, 14)
        create5DayWeek(courses, options, 2020, 9, 21)
        create4DayWeek(courses, options, 2020, 9,29)
        create4DayWeek(courses, options, 2020, 10,5)

y= 2020
m=9
d=8
test = cal(["","","","","","","",""], ["mAdvisory", "breaks", "", ""])
test.create5DayWeek()
d=14
test.create5DayWeek()
