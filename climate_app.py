import numpy as np
import datetime as dt
import sqlalchemy
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)
session = Session(engine)

@app.route("/")
def welcome():
    """Available Routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():    
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_year = query_date - dt.timedelta(days=365)

    past_temp = session.query(measurement.date, measurement.prcp).filter(
        measurement.date <= last_year).all()
    p_list = []
    for x, y in past_temp:
        p_dict = {}
        p_dict["date"] = x
        p_dict["prcp"] = y       
        p_list.append(p_dict) 

    return jsonify(p_list)

@app.route("/api/v1.0/station")
def stations():
    station_nm = session.query(station.station,station.name).all()
    s_list = []
    for x, y in station_nm:
        s_dict = {}
        s_dict["station"] = x
        s_dict["name"] = y       
        s_list.append(s_dict) 
    
    return jsonify(s_list) 

@app.route("/api/v1.0/tobs")
def temp():
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    temp_result = session.query(measurement.tobs).filter(measurement.date >= query_date).filter(measurement.station == 'USC00519281').all()

    output = list(np.ravel(temp_result))   
    return jsonify(output)


@app.route("/api/v1.0/<start>")
def startdate(start):
    session = Session(engine)
    temp_start = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()

    return jsonify(temp_start)
  
@app.route("/api/v1.0/<start>/<end>")
def start(start, end):
    session = Session(engine)
    startend = (session.query(func.min(measurement.tobs), func.max(measurement.tobs),func.avg(measurement.tobs))).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()

    return jsonify(startend)

if __name__ == '__main__':
    app.run(debug=True)
