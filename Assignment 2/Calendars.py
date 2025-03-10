from enum import Enum

        
class Visibility(Enum):
    NONE = 0
    PUBLIC = 1
    PRIVATE = 2
            


class Calendar():
    def __init__(self, calendarID, name, visibility, owner):
        self.calendarID = calendarID
        self.name = name
        self.visibility = visibility
        self.owner = owner
        self.users = []
        self.eventsDict = {}

    def AddUser(self, user):
        self.users.append(user)
        user.AddCalendar(self)
        
    def PrintAllUsers(self):
        if(self.owner is not None):
            print("Owner: ")
            self.owner.print()
            print()
        
        for user in self.users:
            print("User: ")
            print(user)
            
    def PrintAllEvents(self):
        for event in self.eventsDict:
            print(self.eventsDict[event])
    
    def AddEvent(self, event):
        self.eventsDict[event.eventID] = event
           
    def DeleteEvent(self, eventID):
        del self.eventsDict[eventID]
        
    def __str__(self):
        return f"Calendar ID: {self.calendarID} | Owner: {self.owner.name} | Visibility {self.visibility.name}"

class User():
    def __init__(self, userID, name, email):
        self.userID = userID
        self.name = name
        self.email = email
        self.calDict = {}
        self.eventInvitations = []
        
         
    def AddCalendar(self, cal):
        self.calDict[cal.calendarID] = cal
        
    def Update(self, event):
        self.eventInvitations.append(event)
        print(f"New Invitation {event.title} for {self.name}")
        
        
    def PrintCalendars(self):
        if(len(self.calDict.keys()) == 0):
            print("No dictionaries to print.")
        else:
            for key in self.calDict.keys():
                print(self.calDict[key])
            
    def RemoveCalendar(self, calID):
        if(calID in self.calDict.keys()):
            del self.calDict[calID]
        else:
            print(f"Error, could not delete {calID}, not a valid calendar.")
        print(f"Removed calendar {calID}")
        
    def UpdateCalendar(self, calID, name=None, visibility=Visibility(0), owner=None):
        if(name is not None):
            self.calDict[calID].name = name
        
        if(visibility is not Visibility.NONE):
            self.calDict[calID].visibility = visibility
            
        if(owner is not None):
            self.calDict[calID].owner = owner
        
    def PrintInvitations(self):
        for event in self.eventInvitations:
            print(event)

    def __str__(self):
        return f"ID: {self.userID} | Name: {self.name} | Email: {self.email}\n"
        
            

        
class App():
    def __init__(self):
        self.users = {}
        
    def AddUser(self, user):
        self.users[user.userID] = user
    
    def PrintUsers(self):
        for user in self.users:
            print(self.users[user])

class ObservableEvent:
    def __init__(self):
        self._observers = []
    
    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, event):
        for observer in self._observers:
            observer.update(event)

class Settings():
    def __init__(self, theme, timezone):
        self.theme = theme
        self.timezone = timezone
        self.instance = self
    
    def GetInstance(self):
        if(self.instance == None):
            self.instance = self
        return self.instance

    def UpdateTimezone(self, timezone):
        self.timezone = timezone

    def UpdateTheme(self, theme):
        self.theme = theme


class Event(ObservableEvent):
    def __init__(self, eventID, title, date, startTime, endTime, timeZone):
        super().__init__()
        self.eventID = eventID
        self.title = title
        self.date = date
        self.startTime = startTime
        self.endTime = endTime
        self.timeZone = timeZone
        
    def ShareEvent(self, user):
        self.add_observer(user)
        self.notify_observers(self)
   
    def __str__(self):
        return f"Event Name: {self.title} | ID: {self.eventID} | From {self.startTime} to {self.endTime}{self.timeZone} | Attendees:"

    
        
def PrintAppOptions():
    print("What would you like to do?")
    print("1. Create user")
    print("2. Login user")
    print("3. View all public calendars")
    print("Q. Quit")
    
def PrintUserLoggedInOptions():
    
    print("What would you like to do?")
    print("1. Add a calendar")
    print("2. Remove a calendar")
    print("3. Update a calendar")
    print("4. View a calendar")
    print("5. View your event invitations")
    print("B. Go Back")
    
def PrintCalendarOptions():
    print("What would you like to do?")
    print("1. Add an Event")
    print("2. Remove an Event")
    print("3. Update an Event")
    print("4. Toggle Calendar Visibility")
    print("5. Share Calendar")
    print("B. Go Back")
    
def PrintEventOptions():
    print("What would you like to do?")
    print("1. Share this event.")
    print("2. Edit event")
    print("B. Go Back")
    
def PrintEventEditOptions():
    print("What would you like to edit?")
    print("1. Title")
    print("2. Start Time")
    print("3. End Time")
    print("4. Time Zone")
    print("B. Go Back")
    
    
    

def main():
    print("~~~ Welcome to the Calendars app! ~~~")
    CalendarsApp = App("PST", "Dark-Mode")
    userInput = ""
    currentUser = None
    loggedIn = False
    while(userInput != "Q"):
        PrintAppOptions()
        userInput = input("")
        if(userInput == "1"): #create a new user
            print("Creating a new user!")
            name = input("What is your name?")
            email = input("What is your email?")
            newUser = User(len(CalendarsApp.users)+1, name, email)
            CalendarsApp.AddUser(newUser)
            currentUser = newUser
            print(f"New user created!")
            print(currentUser)
            loggedIn = True
            
        
        elif(userInput == "2"): #login to an existing user
            print("available users: ")
            if(len(CalendarsApp.users) == 0):
                print("There are no available users.")
                pass
                continue
            else:
                CalendarsApp.PrintUsers()
                print(f"Which user would you like to log in, {currentUser.name}? Please enter their ID.")
                userInput = int(input())
                try:
                    currentUser = CalendarsApp.users[userInput]
                    print("Successfully logged in!")
                    loggedIn = True
                except:
                    print("Invalid user")
                    continue
                
        elif(userInput == "3"):
            for user in CalendarsApp.users.keys():
                for cal in CalendarsApp.users[user].calDict.keys():
                    if(CalendarsApp.users[user].calDict[cal].visibility == Visibility(1)):
                        CalendarsApp.users[user].calDict[cal].print()
            continue
                        
                
        
        elif(userInput == "Q"):
            break    
        
        else:
            print("Please enter a valid command")
            continue
        
        #if they get here, that means they are logged in currently
        print(f"Welcome to Calendars {currentUser.name}!")
        currentCalendar = None
        while(loggedIn):
            PrintUserLoggedInOptions()
            userInput = input()
            if(userInput == "1"): #creating a caledar
                print("Creating a new Calendar")
                calName = input("Please name your new Calendar: ")
                print("Visibility:\n1. Public\n2. Private")
                calPrivate = int(input())
                newCal = Calendar(len(currentUser.calDict)+1, calName, Visibility(calPrivate), currentUser)
                currentUser.AddCalendar(newCal)
                currentUser.PrintCalendars()
            elif(userInput == "2"): #removing a calendar
                if(len(currentUser.calDict) == 0):
                    print("There are no calendars!")
                    pass
                else:
                    print("Removing a calendar. Current Calendars:")
                    currentUser.PrintCalendars()
                    print("Please enter the ID of the Calendar you'd like to remove.")
                    userInput = int(input())
                    try:
                        del currentUser.calDict[userInput]
                        print(f"Calendar {userInput} removed!")
                    except:
                        print("Error, invalid Calendar ID")
                        pass
            elif(userInput == "3"): #updating a calendar
                print("Updating a Calendar! Please enter the ID of the Calendar:")
                currentUser.PrintCalendars()
                userInput = int(input())
                try:
                    currentCalendar = currentUser.calDict[userInput]
                except:
                    print("Error. Invalid Calendar ID")
            elif(userInput == "4"): #viewing a calendar
                print("Viewing a Calendar! Please enter the ID of the Calendar:")
                currentUser.PrintCalendars()
                userInput = int(input())
                try:
                    currentCalendar = currentUser.calDict[userInput]
                    if(len(currentCalendar.eventsDict) == 0):
                        print(f"There are no events on calendar {currentCalendar.name}!")
                    else:
                        currentCalendar.PrintAllEvents()
                        currentCalendar = None
                except:
                    print("Error. Invalid Calendar ID")
                    
            elif(userInput == "5"):
                if(len(currentUser.eventInvitations) == 0):
                    print("There are no events to show!")
                else:
                    currentUser.PrintInvitations()
            elif(userInput == "B"):
                loggedIn = False    
            else:
                print("Please enter a valid command")
                continue
            
            currentEvent = None
            while(currentCalendar != None):
                print(f"Viewing Calendar: ")
                print(currentCalendar)
                PrintCalendarOptions()
                userInput = input()
                if(userInput == "1"): #add event
                    print("Adding an event!")
                    eventName = input("Event name: ")
                    eventDate = input("Event date: ")
                    startTime = input("Start time: ")
                    endTime = input("End time: ")
                    timeZone = input("Timezone: ")
                    newEvent = Event(len(currentCalendar.eventsDict)+1, eventName, eventDate, startTime, endTime, timeZone)
                    currentCalendar.AddEvent(newEvent)
                    print(f"Event {eventName} added!")
                elif(userInput == "2"): #remove event
                    if(len(currentCalendar.eventsDict) == 0):
                        print("No events to remove.")
                    else:
                        currentCalendar.PrintAllEvents()
                        print("Please enter the ID of the event you'd like to remove.")
                        userInput = int(input())
                        try:
                            currentCalendar.DeleteEvent(userInput)
                            print(f"Event {userInput} removed!")
                        except:
                            print("Error. Invalid Event ID")
                elif(userInput == "3"): #edit event
                    if(len(currentCalendar.eventsDict) == 0):
                        print("No events to edit.")
                    else:
                        currentCalendar.PrintAllEvents()
                        print("Please enter the ID of the event you'd like to edit.")
                        userInput = int(input())
                        try:
                            currentEvent = currentCalendar.eventsDict[userInput]
                            print(f"Event {userInput} selected.s")
                        except:
                            print("Error. Invalid Event ID")
                elif(userInput == "4"): #toggle visibility
                    print("Visibility:\n1. Public\n2. Private")
                    calPrivate = int(input())
                    currentCalendar.visibility = Visibility(calPrivate)
                    print(f"Visibility changed to {Visibility(calPrivate).name}")
                elif(userInput == "5"): #share calendar
                    if(len(CalendarsApp.users) == 0):
                        print("There are no other users!")
                    else:
                        CalendarsApp.PrintUsers()
                        print("Please enter the ID of the user you'd like to share to.")
                        userInput = int(input())
                        try:
                            currentCalendar.AddUser(CalendarsApp.users[userInput])
                            print(f"Successfully added user {userInput}")
                        except:
                            print("Error: Invalid user ID")
                elif(userInput == "B"): #back
                    currentCalendar = None
                else: 
                    print("Please enter a valid command")
                    continue
                    
                editingEvent = False
                while(currentEvent != None): 
                    PrintEventOptions()
                    userInput = input()
                    if(userInput == "1"): #Share event
                        if(len(CalendarsApp.users) == 0):
                            print("There are no other users!")
                        else:
                            CalendarsApp.PrintUsers()
                            print("Please enter the ID of the user you'd like to share to.")
                            userInput = int(input())
                            try:
                                currentEvent.ShareEvent(CalendarsApp.users[userInput])
                                editingEvent = True
                                print(f"Successfully added user {userInput} to event {currentEvent.title}")
                            except:
                                print("Error: Invalid user ID")
                    elif(userInput == "2"): #edit event
                        editingEvent = True
                        while(editingEvent):
                            PrintEventEditOptions()
                            userInput = input()
                            if(userInput == "1"): #title
                                userInput = input("New title: ")
                                currentEvent.title = userInput
                            elif(userInput == "2"): #start time
                                userInput = input("New start time: ")
                                currentEvent.startTime = userInput
                            elif(userInput == "3"): #end time
                                userInput = input("New end time: ")
                                currentEvent.endTime = userInput
                            elif(userInput == "4"): #timezone
                                userInput = input("New timezone: ")
                                currentEvent.timeZone = userInput
                            elif(userInput == "B"): #go back
                                editingEvent = False
                    elif(userInput == "B"):
                        currentEvent = None
                    else:
                        print('Please enter a valid command')
                        continue
    
main()
    