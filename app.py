# Import Modules
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt 
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
print(Base.classes.keys())

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Climate API!<hr/>"
        f"Listed below are the available routes:<br/>"
        f"Precipitation Data for 8/23/16 - 8/23/17: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Observed Temperatures for USC00519281: /api/v1.0/tobs<br/>"
        f"Temperature ranges: /api/v1.0/start_date or /api/v1.0/start_date/end_date<br/>"
        f"**start_date/end_date is in the format yyyy-mm-dd"

    )


# Create precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return precipitation data"""
    # Query measurement data
    prcp_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()

    session.close()   

    # Convert results to a dictionary
    precipitation_dict = []
    for date, prcp in pcrp_results:
        precipitation_dict.append({date: prcp})

    # Return JSON representation of dictionary
    return jsonify(precipitation_dict)


# Create stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all stations
    stations_list = session.query(Station.station, Station.name).all()

    session.close()

    # Convert results to a dictionary
    stations_dict = []
    for station, name in stations_list:
        stations_dict.append({station: name})

    # Return the results
    return jsonify(stations_dict)


# Create observed temperatures route
@app.route("/api/v1.0/tobs")
def most_active_station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most active station for the last year of data
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').all()

    # Convert results to a dictionary
    tobs_results_dict = []
    for date, tobs in tobs_results:
        tobs_results_dict.append({date: tobs})

    # Return the results
    return jsonify(tobs_results_dict)


# Create temp data route with start date only
@app.route("/api/v1.0/<start>")
def temp_obs(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    temps = {}
    temps['TMIN'] = temp_results[0][0]
    temps['TAVG'] = temp_results[0][1]
    temps['TMAX'] = temp_results[0][2]

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    return jsonify(temps)


# Create temp data route with date range
@app.route("/api/v1.0/<start>")
def temp_obs(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    temps = {}
    temps['TMIN'] = temp_results[0][0]
    temps['TAVG'] = temp_results[0][1]
    temps['TMAX'] = temp_results[0][2]

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)