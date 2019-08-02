import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_
from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask Setup
app = Flask(__name__)


# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start>/<end></br>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return date and precipitation values as Dictionary"""
   
    # Create session
    session = Session(engine)
    
    # Retrieve the most recent date
    result = session.query(Measurement).order_by(Measurement.date.desc()).limit(1)
    for row in result:
        latest_date = row.date

    # Convert to datetime format
    conv_latest_date = dt.datetime.strptime(latest_date , '%Y-%m-%d')
    
    # Calculate the date 1 year ago from the last data point in the database
    last_12_months = conv_latest_date - dt.timedelta(days=365)

    # Convert datetime to string
    conv_last_12_months = last_12_months.strftime('%Y-%m-%d')
    
    # Query
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date <= latest_date).filter(Measurement.date >= conv_last_12_months).all()

    return jsonify(dict(precipitation))


@app.route("/api/v1.0/stations")
def passengers():
    """Return a JSON list of stations from the dataset"""
    
    # Create session
    session = Session(engine)
    
    # Query
    stations = session.query(Station).count()

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return temperature observations for a year"""
   
    # Create session
    session = Session(engine)
    
    # Retrieve the most recent date
    result = session.query(Measurement).order_by(Measurement.date.desc()).limit(1)
    for row in result:
        latest_date = row.date

    # Convert to datetime format
    conv_latest_date = dt.datetime.strptime(latest_date , '%Y-%m-%d')
    
    # Calculate the date 1 year ago from the last data point in the database
    last_12_months = conv_latest_date - dt.timedelta(days=365)

    # Convert datetime to string
    conv_last_12_months = last_12_months.strftime('%Y-%m-%d')
    
    # Query
    temp_obv = session.query(Measurement.date, Measurement.tobs).\
                filter(and_(Measurement.date <= latest_date, Measurement.date >= conv_last_12_months)).all()


    return jsonify(dict(temp_obv))


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp(start, end=None):
    """Return temperature observations for a date range"""
   
    # Create session
    session = Session(engine)
    
    # Query
    if end is None:
        temp = session.query( func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    else:
        temp = session.query( func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(and_(Measurement.date >= start, Measurement.date <= end)).all()


    return jsonify(temp)




if __name__ == '__main__':
    app.run(debug=True)

