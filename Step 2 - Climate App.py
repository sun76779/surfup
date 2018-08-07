import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


@app.route("/")
def welcome():
    return (
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/<start_date><br/>"
    f"/api/v1.0/<start>/<end><br/>"
    )    

'''
#prep route
@app.route("/api/v1.0/precipitation")
def prep():
    prev_year = dt.date.today() - dt.timedelta(days=500)
    past_year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > prev_year)
    
    return jsonify(past_year)
'''

#station route
@app.route("/api/v1.0/stations")
def stations():

    #Query all stations
    stations = session.query(Station).all()
    #create a dictionary for each station's info and append to list
    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for station in stations:
        station_dict = {}
        station_dict["station_id"] = station[0]
        station_dict["name"] = station[1]
        station_dict["latitude"] = station[2]
        station_dict["longitude"] = station[3]
        station_dict["elevation"] = station[4]

        all_stations.append(station_dict)

    return jsonify(all_stations)


# temps route using function
@app.route("/api/v1.0/tobs")
def tobs():
    prev_year = dt.date.today() - dt.timedelta(days=500)
    past_year_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > prev_year)
    
    return jsonify(past_year_tobs)
    
#start date route
@app.route("/api/v1.0/<start_date>/")
def start_temp(start):
    #prev_year = dt.date.today() - dt.timedelta(days=500)
    temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurements.date >= start).first()
    #create dictionary from result
    start_temp = {"minimum temperuture": temps[0], "maximum temperature": temps[1], "average temperature": temps[2]}
    return jsonify(start_temp)

#start/end date route
@app.route("/api/v1.0/<start>/<end>/")
def temp_range(start, end):
    #query
    temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).first()
    #create dictionary from result
    start_n_end = {"TMIN": temps[0], "TMAX": temps[1], "TAVG": temps[2]}
    return jsonify(start_n_end)

if __name__ == '__main__':
    app.run(debug=True)