# Import the dependencies.
import sqlalchemy
from flask import Flask, jsonify, render_template, request
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from pathlib import Path
import pandas as pd
import datetime as dt

#################################################
# Database Setup
#################################################
# Create a reference to the file. 
database_path = Path("Resources/hawaii.sqlite")

# Create Engine
engine = create_engine(f"sqlite:///{database_path}")
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine, reflect = True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Run the application 
if __name__ == "__main__":
    app.run(port=8000, debug=True)

#################################################
# Flask Routes
#################################################
@app.route("/")
def Home():
    return render_template("home.html")

# calculate the date 1 year ago from the last date in database
last_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).limit(1).scalar()
last_date = dt.date.fromisoformat(last_date_str)
year_ago_date = last_date - dt.timedelta(days=365.24)


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results from your precipitation analysis 
    (i.e. retrieve only the last 12 months of data) to a dictionary 
    using date as the key and prcp as the value."""
    session = Session(engine)
    
    prcp_results = (
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date >= year_ago_date)
        .order_by(Measurement.date)
        .all()
    )
    session.close()
    
    # Return the JSON representation of your dictionary.
    all_prcp = []
    for date, prcp in prcp_results:
        if prcp != None:
            precip_dict = {}
            precip_dict[date] = prcp
            all_prcp.append(precip_dict)
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    session = Session(engine)
    
    # Query for stations.
    stations = session.query(Station.station, Station.name).all()
   
    # Return the JSON representation of your dictionary.
    all_stations = []
    for station, name in stations:
        if name != None:
            stations_dict = {}
            stations_dict[station] = name
            all_stations.append(stations_dict)
    session.close()
    return jsonify(all_stations) 

@app.route("/api/v1.0/tobs")
def tobs():
    """Query the dates and temperature observations of the most-active station for the previous year of data."""
    session = Session(engine) 
    
    highest_active_stations = session.query(Measurement.station, func.count(Measurement.id)).\
    filter(Measurement.station == Station.station).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.id).desc()).\
    all()
    
    temperature = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > year_ago_date).\
    filter(Measurement.station == highest_active_stations[0][0]).\
    order_by(Measurement.date).\
    all()
    
    # Return the JSON representation of your dictionary.
    all_temp = []
    for date, tobs in temperature:
        if tobs != None:
            temp_dict = {}
            temp_dict[date] = tobs
            all_temp.append(temp_dict)
    session.close()
    return jsonify(all_temp)  

def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVG and TMAX
    """
    session = Session(engine)

    return (
        session.query(
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs),
        )
        .filter(Measurement.date >= start_date)
        .filter(Measurement.date <= end_date)
        .all()
    )
    
@app.route("/api/v1.0/<start>")
def start(start):
    
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range"""
    session = Session(engine) 
    
    temps = calc_temps(start, last_date)

    # Create a list to store the temperature records
    temp_list = []
    date_dict = {"Start Date": start, "End Date": last_date}
    temp_list.append(date_dict)
    temp_list.append(
        {"Observation": "Minimum Temperature", "Temperature(F)": temps[0][0]}
    )
    temp_list.append(
        {"Observation": "Average Temperature", "Temperature(F)": temps[0][1]}
    )
    temp_list.append(
        {"Observation": "Maximum Temperature", "Temperature(F)": temps[0][2]}
    )
    session.close()
    return jsonify(temp_list)

    """calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date"""
    
    """calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive"""
    
    # Create a dictionary from the row data and append to a list of min, avg, and max temperature
    
    
@app.route("/api/v1.0/start-end", methods = ['GET'])
def start_end():
    session = Session(engine) 
    
    """Returns the JSON list of the minimum, average and the maximum temperatures for a given start date and end date(YYYY-MM-DD)"""
    start = request.args.get("Start Date")
    end = request.args.get("End Date")

    temps = calc_temps(start, end)
    # Create a list to store the temperature records
    temp_list = []
    date_dict = {"Start Date":start, "End Date":end}
    temp_list.append(date_dict)
    temp_list.append(
        {"Observation": "Minimum Temperature", "Temperature(F)": temps[0][0]}
    )
    temp_list.append(
        {"Observation": "Average Temperature", "Temperature(F)": temps[0][1]}
    )
    temp_list.append(
        {"Observation": "Maximum Temperature", "Temperature(F)": temps[0][2]}
    )
    session.close()
    return jsonify(temp_list)