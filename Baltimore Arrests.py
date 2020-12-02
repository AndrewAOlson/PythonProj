
import turtle
import datetime

#Dimensions of the background picture

PIC_WIDTH = 700
PIC_HEIGHT = 757

#Coords
#Upper Left : 39.377749, -76.726121
#Upper Right: 39.377749, -76.512116
#Lower Left : 39.196489, -76.726121
#Lower Right: 39.196489, -76.512116

#Height and width of the map in degrees

MAP_WIDTH = -76.526121 + 76.726121
MAP_HEIGHT = 39.377749 - 39.196489

#Ratio of pixels on the screen to degrees on the map in the X and Y directions

PIXELS_PER_DEGREE_X = PIC_WIDTH / MAP_WIDTH
PIXELS_PER_DEGREE_Y = PIC_HEIGHT / MAP_HEIGHT

#The center of the map expressed in degrees

CENTER_X = (-76.726121 + -76.512116) / 2
CENTER_Y = (39.377749 + 39.196489) / 2

#CENTER: 39.287119, 76.6191185


#Setup function

def bmore_setup():
    
    #Set the size of the turtle window to the size of the background image

    import tkinter
    turtle.setup(PIC_WIDTH, PIC_HEIGHT)

    #Create and title the window

    wn = turtle.Screen()
    wn.title("Baltimore Arrests")

    #Set the background image to the map of Baltimore

    canvas = wn.getcanvas()   
    bmore_map = tkinter.PhotoImage(file = "bmore_map.png")

    #Put the map in the center of the turtle window

    canvas.create_image(-PIC_WIDTH/2, -PIC_HEIGHT/2, anchor=tkinter.NW, image = bmore_map)

    t = turtle.Turtle()

    return (t, wn, bmore_map)



#Functions to check the dates

def validDate(date):
    result = True
    
    #Return error if the date does not contain slashes
    
    if "/" not in date:
        return False
    else:        
        lst = date.split("/")

        #Return error if the list is not exactly 3 items when split by the slashes

        if len(lst) != 3:
            return False
    
    #Pull the month, day, and year from the list

    month = lst[0]
    day = lst[1]
    year = lst[2]

    #Return error if the month, day, or year are not ints

    if testInt(month) is False or testInt(day) is False or testInt(year) is False:
        result = False

    else:
        #Make month, day, year into ints
        month = int(month)
        day = int(day)
        year = int(year)

        #Test the year to see if it is valid
        if year not in range(2014, 2021):
            result = False

        else:

            #Test the month to see if it is valid 
            if year == 2020:
                if month not in range(1,10):
                    result = False
            elif year in range(2014, 2020) and month not in range(1,13):
                result = False
            else:

                #Determine whether or not the year is a leap year
                if year % 400 == 0:
                    leapYear = True
                elif year % 100 == 0:
                    leapYear = False
                elif year % 4 == 0:
                    leapYear = True
                else:
                    leapYear = False

                #Test the day to see if it is within 1 and 31
                if day not in range(1,32):
                    result = False

                #If the month only has 30 days, determine if the day is between 1 and 30 
                elif month in [4,6,9,11] and day > 30:
                    result = False

                #If the month is February and it's a leap year, test to see if the day is between 1 and 29
                elif month == 2 and leapYear == True and day not in range(1, 30):
                    result = False

                #If the month is February and it's not a leap year, test to see if the day is between 1 and 28
                elif month == 2 and leapYear == False and day not in range(1, 29):
                    result = False

                else:
                    result = True

    return result

def dateConverter(date):

    #Split the date by /, and return it in a form that the datetime module can use

    lst = date.split("/")

    month = int(lst[0])
    day = int(lst[1])
    year = int(lst[2])

    newdate = datetime.date(year, month, day)
    return newdate

def checkBetween(date1, date2):
    
    #Check to see if date1 comes before date2
    
    if date1 < date2:
        return True
    else:
        return False

def testInt(x):
    
    #Check if a number is an integer, use to verify the dates
    
    try:
        int(x)
        return True
    except ValueError:
        return False


#Function to show the arrests

def bmore_arrests(date1, date2):

    #Run the setup function

    (t, wn, bmore_map) = bmore_setup()

    #Prepare the turtle to stamp locations on the map

    t.speed(0)
    t.up()
    t.ht()

    #Create dictionary to store district locations and felony/misdemeanor arrests

    districts = {}
    felony = {"Felony":0,"Misdemeanor":0,"Unknown":0}

    #show data points

    arrest_data = open("BPD_Arrests.csv", "r")

    if date2 == "":
            
        #If only showing for one day, test if dates in the csv are equal to given date 

        for line in arrest_data.readlines()[1:]:
            lst = line.split(",")

            arrest_date = dateConverter(lst[4])

            if arrest_date == date1:

                if lst[14] != "" and lst[15] != "":    
                    lat = float(lst[14])
                    lon = float(lst[15])

                    #Calculate the pixel position of the arrest using the degree position relative to
                    #the center of the window and multiplying by the pixel to degree ratio

                    x_coord = (lat - CENTER_X) * PIXELS_PER_DEGREE_X
                    y_coord = (lon - CENTER_Y) * PIXELS_PER_DEGREE_Y

                    charge = str(lst[9])

                    #Set the color of the turtle to match whether the arrest is for a felony, misdemeanor, or unknown

                    if charge == "":
                        t.color("gray")
                        felony["Unknown"] += 1
                                
                    elif charge[0] != "1":
                        t.color("red")
                        felony["Felony"] += 1
                                
                    else:
                        t.color("blue")
                        felony["Misdemeanor"] += 1

                    #Move the turtle and stamp on the location of each arrest

                    t.setpos(x_coord, y_coord)
                    t.stamp()

                #Count the number of arrests in each district

                if lst[11] != "":
                    if lst[11] not in districts:
                        districts[lst[11]] = 0

                    districts[lst[11]] += 1
    else:

        #If showing arrests for a range of dates, test if dates in csv fall in the given date range

        for line in arrest_data.readlines()[1:]:
            lst = line.split(",")

            arrest_date = dateConverter(lst[4])

            if arrest_date >= date1 and arrest_date <= date2:

                if lst[14] != "" and lst[15] != "":
                    lat = float(lst[14])
                    lon = float(lst[15])

                    #Calculate the pixel position of the arrest using the degree position relative to
                    #the center of the window and multiplying by the pixel to degree ratio

                    x_coord = (lat - CENTER_X) * PIXELS_PER_DEGREE_X
                    y_coord = (lon - CENTER_Y) * PIXELS_PER_DEGREE_Y

                    charge = str(lst[9])

                    #Set the color of the turtle to match whether the arrest is for a felony, misdemeanor, or unknown

                    if charge == "":
                        t.color("gray")
                        felony["Unknown"] += 1
                                        
                    elif charge[0] != "1":
                        t.color("red")
                        felony["Felony"] += 1
                                        
                    else:
                        t.color("blue")
                        felony["Misdemeanor"] += 1

                    t.setpos(x_coord, y_coord)
                    t.stamp()

                #Count the number of arrests in each district
                if lst[11] != "":
                    if lst[11] not in districts:
                        districts[lst[11]] = 0

                    districts[lst[11]] += 1

    #After the turtle has finished stamping, show the felony/misdemeanor and district numbers

    print("")
    print("Arrests by Police District:")
    for i in districts:
        print(i + ": " + str(districts[i]))

    print("")
    print("Felony/Misdemeanor Arrests:")
    for i in felony:
        print(i + ": " + str(felony[i]))

    print("")


    wn.exitonclick()

def main():

    #Ask for beginning date, return error if invalid
    
    print("Baltimore Arrest Database Visualizer")
    print("Enter a beginning date in M/D/YYYY format to see Baltimore arrest data")
    print("The date must be between 1/1/2014 and 9/30/2020")
    date1 = input()

    if validDate(date1) is False:
        print("Please restart and enter a valid beginning date")
    else:

        #If beginning date is valid, ask for end date

        print("Enter the end date in M/D/YYYY format")
        print("The date must be after the beginning date and between 1/1/2014 and 9/30/2020")
        print("If you want to see the first date only, enter nothing")
        date2 = input()
        
        #If end date is blank, show arrests for just the beginning date

        if validDate(date1) is True and date2 == "":
            newdate1 = dateConverter(date1)

            bmore_arrests(newdate1, date2)

        #If end date is not blank, test if valid
        
        elif validDate(date2) is False:
            print("Please restart and enter a valid end date")
        
        else:
            
            #If end date is valid, convert and test if end date comes after beginning date

            newdate1 = dateConverter(date1)
            newdate2 = dateConverter(date2)

            if checkBetween(date1, date2) is False:
                print("The beginning date must be before the end date, please restart and enter valid dates")
            
            else:

                #If everything is valid, show arrests for the date range given

                bmore_arrests(newdate1, newdate2)


main()

