
import turtle
import datechecker
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

    arrest_data = open("BPD_Arrests_copy.csv", "r")

    if date2 == "":
            
        for line in arrest_data.readlines()[1:]:
            lst = line.split(",")

            arrest_date = datechecker.dateConverter(lst[4])

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
                                
                    elif charge[2] != "0":
                        t.color("red")
                        felony["Felony"] += 1
                                
                    else:
                        t.color("blue")
                        felony["Misdemeanor"] += 1

                    t.setpos(x_coord, y_coord)
                    t.stamp()

                if lst[11] not in districts:
                    districts[lst[11]] = 0

                districts[lst[11]] += 1
    else:
        
        for line in arrest_data.readlines()[1:]:
            lst = line.split(",")

            arrest_date = datechecker.dateConverter(lst[4])

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
                                        
                    elif charge[2] != "0":
                        t.color("red")
                        felony["Felony"] += 1
                                        
                    else:
                        t.color("blue")
                        felony["Misdemeanor"] += 1

                    t.setpos(x_coord, y_coord)
                    t.stamp()

                if lst[11] not in districts:
                    districts[lst[11]] = 0

                districts[lst[11]] += 1

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
    
    print("Baltimore Arrest Database Visualizer")
    print("Enter a beginning date in M/D/YYYY format to see Baltimore arrest data")
    print("The date must be between 1/1/2014 and 9/30/2020")
    date1 = input()

    if datechecker.validDate(date1) is False:
        print("Please restart and enter a valid beginning date")
    else:
        print("Enter the end date in M/D/YYYY format")
        print("The date must be after the beginning date and between 1/1/2014 and 9/30/2020")
        print("If you want to see the first date only, enter nothing")
        date2 = input()
            
        if datechecker.validDate(date1) is True and date2 == "":
            newdate1 = datechecker.dateConverter(date1)

            bmore_arrests(newdate1, date2)
        
        elif datechecker.validDate(date2) is False:
            print("Please restart and enter a valid end date")
        
        else:
            
            newdate1 = datechecker.dateConverter(date1)
            newdate2 = datechecker.dateConverter(date2)

            if datechecker.checkBetween(date1, date2) is False:
                print("The beginning date must be before the end date, please restart and enter valid dates")
            
            else:
                bmore_arrests(newdate1, newdate2)


main()

