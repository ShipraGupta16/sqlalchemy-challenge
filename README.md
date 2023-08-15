# sqlalchemy-challenge - Surfs Up!

### Objective:

This repository is to perform climate analysis on Honolulu, Hawaii. The climate analysis is done using SQLAlchemy and Python which is in climate_analysis.ipynb file, and flask web application is built in app.py file and the SQLAlchemy file was provided in hawaii.sqlite. 

In order to run the flask application, use this command: flask run --port 8000

Technologies used: Python(Numpy, Pandas, Matplotlib), SQLAlchemy (ORM), FLASK

### Part 1: Analyze and Explore the Climate Data

1. Used the SQLAlchemy create_engine() function to connect to hawaii.sqlite database.
2. Used the SQLAlchemy automap_base() function to reflect tables into classes and  save references to the classes named station and measurement.
3. Linked Python to the database by creating a SQLAlchemy session.

### Precipitation Analysis

1. Found the most recent date in the dataset.
2. Using that date, obtained the previous 12 months of precipitation data by querying the previous 12 months of data.
3. Selected only the "date" and "prcp" values.
4. Loaded the query results into a Pandas DataFrame. Explicitly set the column names.
5. Sorted the DataFrame values by "date".
6. Plot the results by using the DataFrame plot method.
7. Used Pandas to print the summary statistics for the precipitation data.


### Station Analysis

1. Designed a query to calculate the total number of stations in the dataset.
2. Designed a query to find the most-active stations (that is, the stations that have the most rows). To do so, complete the following steps:
    - List the stations and observation counts in descending order.
    - which station id has the greatest number of observations?
3. Designed a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
4. Designed a query to get the previous 12 months of temperature observation (TOBS) data. To do so, completed the following steps:
    - Filtered by the station that has the greatest number of observations.
    - Performed a query on the previous 12 months of TOBS data for that station.
    - Plot the results as a histogram with bins = 12

### Part 2: Design Your Climate App
Designed a Flask API based on the queries that were developed above.
Used FLASK to create the following routes.
Used Flask jsonify to convert your API data into a valid JSON response object.

These are the following routes defined:
1. / <br>
   This is for the homepage.

2. /api/v1.0/precipitation <br>
   Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.

   Return the JSON representation of your dictionary.

3. /api/v1.0/stations <br>
   Return a JSON list of stations from the dataset.

4. /api/v1.0/tobs <br>
   Query the dates and temperature observations of the most-active station for the previous year of data.

   Return a JSON list of temperature observations for the previous year.

5. /api/v1.0/<start> and /api/v1.0/<start>/<end>
   Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

   For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

   For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.