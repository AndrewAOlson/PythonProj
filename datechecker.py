import datetime

def validDate(date):
    result = True
    
    if "/" not in date:
        return False
    else:        
        lst = date.split("/")

    #Test the month, day, and year to see if int
    month = lst[0]
    day = lst[1]
    year = lst[2]

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

    lst = date.split("/")

    month = int(lst[0])
    day = int(lst[1])
    year = int(lst[2])

    newdate = datetime.date(year, month, day)
    return newdate

def checkBetween(date1, date2):
    if date1 < date2:
        return True
    else:
        return False

def testInt(x):
    try:
        int(x)
        return True
    except ValueError:
        return False


