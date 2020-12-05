# PythonProj

## Methodology for calculating pixel position of the data points

I ran into some problems creating a coordinate system because the area I am showing is very small on a global scale, so the
latitude and longitude values for the corners of the map were too close together to create a coordinate system that I could work with.

To get around this, I calculated the width and height of the background map in degrees, and then divided the pixel height and width by the
degree height and width to get the pixels per degree in the x and y directions.

Then, I found the degree position of the center of the map and set that to pixel (0,0), and then as I iterated through the data points I found the difference
between the x and y degree position from center degree position, and then multiplied that difference by the pixel per degree ratio in the x and y directions to find
the pixel position of each data point relative to the center (0,0).

## Methodology for converting dates to readable formats

I used the datetime module in python to read dates and detect if the arrests happened on the desired date or within the desired date range

The datetime module works with dates in a YYYY-MM-DD format, so in order to compare the given dates and the dates in the csv, I converted them to this format
The dates in the csv and the dates the user inputs must be in M/D/YYYY format, so I split each date by the "/" character and then made sure there were 3 ints that
were adequate month, day, and year numbers. I then used the datetime module to compare the dates in the new format using the less than and greater than operators

## Methodology for categorizing arrests by charge and district

The csv file contains the charge code and district in which the arrest took place. Categorizing by district was simple, just storing each arrest in a dictionary 
based on the district for that row. Categorizing by arrest was more difficult, because it meant deciphering the charge codes. If the charge code was not given, I listed 
it as unknown. After some research, I found that if the first number in the charge code was a 1, it was a misdemeanor arrest. If the first number was anything else, it 
was a felony arrest.

## Video Link

https://youtu.be/AxmJIDzjPZE 
