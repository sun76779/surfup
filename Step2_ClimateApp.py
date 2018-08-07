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

# Getting a list of dates for the last 12 months
today_date = dt.datetime.strptime("2018-08-06", "%Y-%m-%d")

dates = [today_date - dt.timedelta(days=x) for x in range(0, 365)]

# Converting them to a list of strings
str_dates = []
for date in dates:
    new_date = date.strftime("%Y-%m-%d")
    str_dates.append(new_date)


@app.route("/")
def welcome():
    return (
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/yyyy-mm-dd/<br/>"
    f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
    )    


#prep route
@app.route("/api.v1.0/precipitation")
def precipitation():

    # Query precipitation
    prev_year = dt.date.today() - dt.timedelta(days=365)
    results = session.query(Measurement).filter(Measurement.date> prev_year )
    
    prcp_data = []
    for day in results:
        prcp_dict = {}
        prcp_dict[day.date] = day.prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)


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
        station_dict["Station"] = station.station
        station_dict["Name"] = station.name
        all_stations.append(station_dict)

    return jsonify(all_stations)


# temps route using function
@app.route("/api/v1.0/tobs")
def tobs():
    prev_year = dt.date.today() - dt.timedelta(days=365)
    results = session.query(Measurement).filter(Measurement.date> prev_year)

    temp_list = []
    for day in results:
        temp_dict = {}
        temp_dict[day.date] = day.tobs
        temp_list.append(temp_dict)

    return jsonify(temp_list)

#start date route
@app.route("/api/v1.0/calc_temps/<start_date>")

def calc_temps(start='start_date'):
    start_date = dt.strptime('2017-08-06', '%Y-%m-%d').date()
    start_results = session.query(func.max(Measurement.tobs), \
                            func.min(Measurement.tobs),\
                            func.avg(Measurement.tobs)).\
                            filter(Measurement.date >= start_date) 
    
    start_tobs = []
    for tobs in start_results:
        tobs_dict = {}
        tobs_dict["TAVG"] = float(tobs[2])
        tobs_dict["TMAX"] = float(tobs[0])
        tobs_dict["TMIN"] = float(tobs[1])
        
        start_tobs.append(tobs_dict)

    return jsonify(start_tobs)

#start/end date route
@app.route('/api/v1.0/<start_date>/<end_date>/')
def query_dates(start_date, end_date):
    
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    data_list = []
    for result in results:
        row = {}
        row["Start Date"] = start_date
        row["End Date"] = end_date
        row["Avg Temp"] = float(result[0])
        row["High Temp"] = float(result[1])
        row["Low Temp"] = float(result[2])
        data_list.append(row)
    return jsonify(data_list)


if __name__ == '__main__':
    app.run(debug=True)