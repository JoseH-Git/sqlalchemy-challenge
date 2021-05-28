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
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station 


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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitations"""
    # Query all precipitation dates
    results = session.query(measurement.date,measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_measurment = list(np.ravel(results))

    return jsonify(all_measurment)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitations"""
    # Query all stations
    results = session.query(measurement.station).distinct().all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of tobs"""
    # Query all stations
    #results = session.query(measurement.tobs,measurement.date).all()
    last_date= session.query(measurement.date).order_by(measurement.date.desc()).first()
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    print("Query Date: ", query_date)
    session.close()

    most_active_station = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    most_active_station

    data_query_temp = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').\
                  filter(measurement.date >= query_date).order_by(measurement.date.desc()).all()
    data_query_temp

    # Convert list of tuples into normal list
    most_active = list(np.ravel(most_active_station))
    query_temp = list(np.ravel(data_query_temp))
    #return jsonify(most_active)
    return jsonify(query_temp)

@app.route("/api/v1.0/<date>")
def date():

    """Fetch the Justice League character whose real_name matches
       the path variable supplied by the user, or a 404 if not."""

    canonicalized = measurement.replace(" ", "").lower()
    for date in measurement:
        search_term = date["date"].replace(" ", "").lower()

        if search_term == canonicalized:
            return jsonify(measurement)

    return jsonify({"error": f"Character with real_name {real_name} not found."}), 404



    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitations"""
    # Query all stations
    results = session.query(measurement.date).all()
 
    start_date = [measurement.station, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]


    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
    
    return jsonify(all_stations)


if __name__ == '__main__':
    app.run(debug=True)