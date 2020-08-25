from flask import Flask, request, make_response

app = Flask(__name__)

#Import relevant libraries
from ics import Calendar, Event
import datetime

#Create calendar
c = Calendar()
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
def fallMidterm1Weeks(blocks):
    create4DayWeek(blocks, 2020, 9, 8)
    create5DayWeek(blocks, 2020, 9, 14)
    create5DayWeek(blocks, 2020, 9, 21)
    create4DayWeek(blocks, 2020, 9,29)
    create4DayWeek(blocks, 2020, 10,5)

def guidedFallMidterm1Weeks(courses):
    create4DayWeek(courses, 2020, 9, 8)
    create5DayWeek(courses, 2020, 9, 14)
    create5DayWeek(courses, 2020, 9, 21)
    create4DayWeek(courses, 2020, 9,29)
    create4DayWeek(courses, 2020, 10,5)

@app.route("/", methods=["GET", "POST"])
def home():
    return '''
        <html>
            <head>
                <style>
                    .col{width:33.33%; float:left; margin-top: 50px; text-align: center;}
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
                        <li><a href="https://support.google.com/calendar/answer/37118?co=GENIE.Platform%3DDesktop&hl=en">Import</a> the calendar that you just created</li>
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
                    <p><input type="checkbox" id="option1" name="option1" value="MorningAdvisory">
                    <label for="option1">Morning Advisory</label></p>
                    <p><input type="checkbox" id="option2" name="option2" value="breaks">
                    <label for="option2">Breaks</label></p>
                    <p><input type="checkbox" id="option3" name="option3" value="Lunch">
                    <label for="option3">Lunch</label></p>
                    <p><input type="checkbox" id="option4" name="option4" value="Conferencing">
                    <label for="option4">Conferencing/Faculty Collaboration</label></p>
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
    guidedFallMidterm1Weeks(courses)
    
    response = make_response(str(c))
    response.headers["Content-Disposition"] = "attachment;filename=my.ics"
    return response

    
if __name__ == "__main__":
    print("running!")
    app.run(debug=True)
    print("done...")
