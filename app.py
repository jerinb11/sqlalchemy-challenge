import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Flask Setup
############################
# KEEP __name__ same
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/startend<br/>"
    )

@app.route("/api/v1.0/precipitation")
def preciptiation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation from last year"""
    # Query all precipitation
    # session.query(key, value)
    results = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date > '2016-08-23').\
    order_by(measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_results= list(np.ravel(results))

    return jsonify(all_results)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations from last year"""
    # Query all stations
    results = session.query(measurement.station, func.count(measurement.id)).group_by(measurement.station).\
    order_by(func.count(measurement.id).desc()).all()

    session.close()

    # Convert list of tuples into normal list
    all_results= list(np.ravel(results))

    return jsonify(all_results)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    tobs_highest = session.query(measurement.station).group_by(measurement.station).\
    order_by(func.count(measurement.tobs).desc()).first()
    tobs_highest = tobs_highest[0]
    # Query 
    # session.query(key, value)
    results = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date > '2016-08-23' ).\
    filter(measurement.station == tobs_highest).\
    order_by(measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_results= list(np.ravel(results))

    return jsonify(all_results)


@app.route("/api/v1.0/start")
def start():
  # Create our session (link) from Python to the DB
    session = Session(engine)

  # session.query(key, value)
    results = session.query(measurement.station).group_by(measurement.station).\
    order_by(func.count(measurement.id).desc()).first()

    session.close()

 # Convert list of tuples into normal list
    all_results= list(np.ravel(results))

    return jsonify(all_results)


@app.route("/api/v1.0/startend")
def startend():
   # Create our session (link) from Python to the DB
    session = Session(engine)

    active_station = session.query(measurement.station).group_by(measurement.station).\
    order_by(func.count(measurement.id).desc()).first()
    active_station = active_station[0]

    # session.query(key, value)
    results = session.query(measurement.station, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).group_by(measurement.station).\
    filter(measurement.station == active_station).all()

    session.close()

# Convert list of tuples into normal list
    all_results= list(np.ravel(results))

    return jsonify(all_results)


if __name__ == '__main__':
    app.run(debug=True)
