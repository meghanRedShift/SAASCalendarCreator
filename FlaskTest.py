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

#List of year, month, and date of holidays on the school calendar
hy = [2020,2020, 2020]
hm = [10, 11,11]
hd = [12, 3, 11]

#Create the class cal
class cal:
    #Initialize the class and its members
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
        
        adjustDay = 1
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
                    #Loops through each holiday date
                    
                    #Adjusts date using z to go through each day of the week.
                    #This is in a separate statement so that the
                    #added day makes the month roll over if necessary
                    beg +=datetime.timedelta(days=z-adjustDay)
                    for i in range(len(hy)):
                        #Creates a date object for each holiday date
                        checkHol = datetime.date(hy[i], hm[i], hd[i])
                        #Compares the current date to the holiday and skips
                        #to the next day if the current one is a holiday
                        if beg.date() == checkHol:
                            adjustDay = 0
                            beg+=datetime.timedelta(days=1)
                    #Creates calendar event
                    print(beg)
                    e=Event(name=names[x], begin=beg, duration={"minutes":dur[x]})
                    #Adds event to calendar
                    self.cal.events.add(e)
                    self.cal.events
            
        #Prints calendar file to console
        print(str(self.cal))
        #Saves calendar file to console
        #I just keep writing to the same calendar. Haven't had issues with this but it could possibly cause issues.
        #This did cause issues. I did all of the class stuff because of them
        open('my.ics', 'w').writelines(self.cal)
        #Adds 3 days to get to the start of the next week
        beg+=datetime.timedelta(days=3)
        self.d = beg.day
        self.m = beg.month
        self.y = beg.year

    #creates a 4 day week in calendar using the provided list of course names and week start date
    def create5DayWeek(self):
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
        if self.options[4]:
            collaboration = 'Collaboration'
        else:
            collaboration = ""
        #List of modified durations for long days on 5 day schedule
        dur5 = [15,60,15,15,60,15,45,60,15,15,105]
        #List of names for each event depending on the day of the week
        mNames = [mAdvisory, self.courseNames[0], self.courseNames[0] + " Flex", breaks,
                     self.courseNames[2], self.courseNames[2] + " Flex", lunch, self.courseNames[4], self.courseNames[4] +
                     " Flex", breaks, self.courseNames[6], self.courseNames[6] + " Flex", conferencing]
        tNames = [mAdvisory, self.courseNames[1], self.courseNames[1] + " Flex", breaks,
                     self.courseNames[5], self.courseNames[5] + " Flex", lunch, self.courseNames[7], self.courseNames[7] +
                     " Flex", breaks, conferencing]
        wNames = [mAdvisory, self.courseNames[3], self.courseNames[3] + " Flex", breaks,
                     self.courseNames[4], self.courseNames[4] + " Flex", lunch, self.courseNames[6], self.courseNames[6] +
                     " Flex", breaks, conferencing]
        thNames = [mAdvisory, self.courseNames[0], self.courseNames[0] + " Flex", breaks,
                     self.courseNames[2], self.courseNames[2] + " Flex", lunch, self.courseNames[5], self.courseNames[5] +
                     " Flex", breaks, collaboration]
        fNames = [mAdvisory, self.courseNames[1], self.courseNames[1] + " Flex", breaks,
                     self.courseNames[3], self.courseNames[3] + " Flex", lunch, self.courseNames[7], self.courseNames[7] +
                     " Flex", breaks, conferencing]
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
                    beg= datetime.datetime(self.y, self.m, self.d, hrs[x], mins[x])
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
        #This did cause issues. I did all of the class stuff because of them
        open('my.ics', 'w').writelines(self.cal)
        #Adds 3 days to get to the start of the next week
        beg+=datetime.timedelta(days=3)
        self.d = beg.day
        self.m = beg.month
        self.y = beg.year

#This is where we get into flask stuff. I only have a basic working knowledge of this stuff
#This says that when we just have the base address, run this function
@app.route("/", methods=["GET", "POST"])
def home():
    #This is the HTML for the web page that you see
    return '''
        <html>
            <head>
                <style>
                    .col{width:33.33%; float:left; margin-top: 10px; text-align: center;}
                    #title{border: 5px solid red;}
                    #instructions {text-align: left;}
                </style>
            </head>
            <body>
                <div class="col"><p></p></div>
                <div class="col">
                <h1 id="title">Calendar Creator for SAAS</h1>
                <div id="instructions">
                    <h3>Instructions</h3>
                    <p>Enter the names of your classes here. If you do not have a class for a certain block just leave the box blank. Once you press submit:</p>
                    <ul>
                        <li>A calendar file will download.</li>
                        <li>Create a <a href="https://support.google.com/calendar/answer/37095?hl=en">new calendar</a> in Google Drive</li>
                        <li><a href="https://support.google.com/calendar/answer/37118?co=GENIE.Platform%3DDesktop&hl=en">Import</a> the calendar that you just downloaded into the calendar that you just created!</li>
                    </ul>
                    <p><u>Currently, this generates a file for the first half trimester of the year only</u></p>
                </div>
                <form action="/getCal">
                    <p><b>Class Names:</b></p>
                    <p>Block 1: <input name="block1"/></p>
                    <p>Block 2: <input name="block2"/></p>
                    <p>Block 3: <input name="block3"/></p>
                    <p>Block 4: <input name="block4"/></p>
                    <p>Block 5: <input name="block5"/></p>
                    <p>Block 6: <input name="block6"/></p>
                    <p>Block 7: <input name="block7"/></p>
                    <p>Block 8: <input name="block8"/></p>
                    <p><b>Check to include:</b></p>
                    <p><input type="checkbox" id="mAdvisory" name="mAdvisory" value="mAdvisory">
                    <label for="mAdvisory">Morning Advisory</label></p>
                    <p><input type="checkbox" id="breaks" name="breaks" value="breaks">
                    <label for="breaks">Breaks</label></p>
                    <p><input type="checkbox" id="lunch" name="lunch" value="Lunch">
                    <label for="lunch">Lunch</label></p>
                    <p><input type="checkbox" id="conferencing" name="conferencing" value="conferencing">
                    <label for="conferencing">Conferencing</label></p>
                    <p><input type="checkbox" id="collaboration" name="collaboration" value="collaboration">
                    <label for="collaboration">Faculty Collaboration</label></p>
                    <p><input type = "submit" value="Submit"/></p>
                </form>
                <p>Want to learn more about how this was made? Check out the <a href="https://github.com/meghanRedShift/SAASCalendarCreator">GitHub</a>!</p>
                </div>
                <div class="col"><p></p></div>
            </body>
        </html>
'''

@app.route('/getCal')
def getCal():
    #Get each block name from the form
    block1 = request.args['block1']
    block2 = request.args['block2']
    block3 = request.args['block3']
    block4 = request.args['block4']
    block5 = request.args['block5']
    block6 = request.args['block6']
    block7 = request.args['block7']
    block8 = request.args['block8']
    courses = [block1, block2, block3, block4, block5, block6, block7, block8]
    #Creates a boolean list that says whether or not each box has been checked
    mAdvisory = 'mAdvisory' in request.args
    breaks = 'breaks' in request.args
    lunch = 'lunch' in request.args
    conferencing = 'conferencing' in request.args
    collaboration = 'collaboration' in request.args
    options=[mAdvisory,breaks,lunch,conferencing,collaboration]

    #Create a calendar for each relevant week
    createCal = cal(courses, options, 2020, 10, 12)
    createCal.create4DayWeek()
    createCal.create5DayWeek()
    createCal.create5DayWeek()
    createCal.create4DayWeek()
    createCal.create4DayWeek()
    createCal.create5DayWeek()
    
    #guidedFallMidterm1Weeks(courses, options)

    #Downloads the file
    response = make_response(str(createCal.cal))
    response.headers["Content-Disposition"] = "attachment;filename=my.ics"
    #return '<br>'.join(str(options))
    return response

#Runs the flask
if __name__ == "__main__":
    print("running!")
