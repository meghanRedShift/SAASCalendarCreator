
#Import relevant libraries
from ics import Calendar, Event
import datetime

#The time (mins and hours) and duration of each period listed on the block schedule
hrs = [15,16,17,17,17,18,18,19,20,20,21,22,22]
mins = [45,00,00,15,30,30,45,30,30,45,00,00,15]
dur = [15,60,15,15,60,15,45,60,15,15,60,15,30]
#List of year, month, and date of holidays on the school calendar
hy = [2020,2020,2020]
hm = [10,11,11]
hd = [12,3,11]
class cal:
    def __init__(self, courseNames, options, y, m, d):
        self.cal= Calendar()
        self.courseNames = courseNames
        self.options = options
        self.y = y
        self.m = m
        self.d = d

        #creates a 4 day week in calendar using the provided list of course names and week start date
    def create4DayWeek(self):
        #Checks if the checkbox for each option has been selected and
        #sets the name for that option accordingly. The name "" will
        #not create an event
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
        oddNames = [mAdvisory, self.courseNames[0], self.courseNames[0] + " Flex", breaks,
                     self.courseNames[2], self.courseNames[2] + " Flex", lunch, self.courseNames[4], self.courseNames[4] +
                     " Flex", breaks, self.courseNames[6], self.courseNames[6] + " Flex", conferencing]
        evenNames = [mAdvisory, self.courseNames[1], self.courseNames[1] + " Flex", breaks,
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
                    beg= datetime.datetime(self.y, self.m, self.d, hrs[x], mins[x])
                    #Adjusts date using z. This is in a separate statement so that the
                    #added day makes the month roll over if necessary
                    beg +=datetime.timedelta(days=z-1)
                    
                    print(beg)
                    #Loops through each holiday date
                    for i in range(len(hy)):
                        #Creates a date object for each holiday date
                        checkHol = datetime.date(hy[i], hm[i], hd[i])
                        holiday = False
                        #Compares the current date to the holiday and skips
                        #to the next day if the current one is a holiday
                        if beg.date() == checkHol:
                            holiday = True
                            print("Holiday")
                            beg+=datetime.timedelta(days=1)
                            print(beg)
                            print("hol")
                            self.d = beg.day
                            self.m = beg.month
                            self.y = beg.year
                            print(beg)
                    #Creates calendar event
                    e=Event(name=names[x], begin=beg, duration={"minutes":dur[x]})
                    #Adds event to calendar
                    self.cal.events.add(e)
                    self.cal.events
                    if holiday == True:
                        beg-=datetime.timedelta(days=1)
                        self.d = beg.day
                        self.m = beg.month
                        self.y = beg.year
                        print(beg)

        
courses = ["1","2","","","","","",""]
options=["", "", "", ""]
createCal = cal(courses, options, 2020, 10, 12)
createCal.create4DayWeek()
