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

hy = [2020,2020]
hm = [9, 10]
hd = [28, 12]
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
                    beg= datetime.datetime(self.y, self.m, self.d, hrs[x], mins[x])
                    #Adjusts date using z. This is in a separate statement so that the
                    #added day makes the month roll over if necessary
                    beg +=datetime.timedelta(days=z-1)
                    for i in range(len(hy)):
                        checkHol = datetime.date(hy[i], hm[i], hd[i])
                        if beg.date() == checkHol:
                            beg+=datetime.timedelta(days=1)
                            self.d = beg.day
                            self.m = beg.month
                            self.y = beg.year
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
        beg+=datetime.timedelta(days=3)
        self.d = beg.day
        self.m = beg.month
        self.y = beg.year

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
        open('my.ics', 'w').writelines(self.cal)
        beg+=datetime.timedelta(days=3)
        self.d = beg.day
        self.m = beg.month
        self.y = beg.year


@app.route("/", methods=["GET", "POST"])
def home():
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
                <h1 id="title">SAAS Calendar Creator</h1>
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
                </div>
                <div class="col"><p></p></div>
            </body>
        </html>
'''

@app.route('/getCal')
def getCal():
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

    createCal = cal(courses, options, 2020, 9, 8)
    createCal.create4DayWeek()
    createCal.create5DayWeek()
    createCal.create5DayWeek()
    createCal.create4DayWeek()
    createCal.create4DayWeek()
    
    #guidedFallMidterm1Weeks(courses, options)
    
    response = make_response(str(createCal.cal))
    response.headers["Content-Disposition"] = "attachment;filename=my.ics"
    #return '<br>'.join(str(options))
    return response

    
if __name__ == "__main__":
    print("running!")
    app.run(debug=True)
    print("done...")
