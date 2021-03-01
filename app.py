import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, distinct

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

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
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        # f"/api/v1.0/<start>"
        # Should start and start/end date not appear here?
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all measurement dates and precipitation measurements
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # List to hold weather data
    weather_data = []

    # For loop to capture data int dictionary, then into the list
    for date, prcp in results:
        weather_dict = {}
        weather_dict['date'] = date
        weather_dict['prcp'] = prcp
        weather_data.append(weather_dict)

    return jsonify(weather_data)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # For loop appending stations to list
    stations = []
    for result in results:
        stations.append(result[0])

    # printing station list
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    one_year_prior = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query all temperature observations for the station with the most readings
    station_results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= one_year_prior).\
    filter(Measurement.station == 'USC00519281').\
    order_by(Measurement.date.desc()).all()

    session.close()

    return jsonify(station_results)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    min_temp = func.min(Measurement.tobs)
    avg_temp = func.avg(Measurement.tobs)
    max_temp = func.max(Measurement.tobs)
    # Query all temperature observations for the station with the most readings
    temp_results = session.query(min_temp, avg_temp, max_temp).\
    filter(Measurement.date >= start).all()

    session.close()

    return jsonify(temp_results)


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    min_temp = func.min(Measurement.tobs)
    avg_temp = func.avg(Measurement.tobs)
    max_temp = func.max(Measurement.tobs)
    # Query all temperature observations for the station with the most readings
    temp_results = session.query(min_temp, avg_temp, max_temp).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()

    session.close()

    return jsonify(temp_results)


if __name__ == '__main__':
    app.run(debug=True)
