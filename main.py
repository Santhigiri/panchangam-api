from datetime import datetime
import re
from flask import Flask, jsonify, request

from panchangam.astronomical_calculations import get_panchangam
from panchangam.constants import DEFAULT_TIMEZONE, Coordinates
from panchangam.get_monthly_panchangam import get_monthly_panchangam

app = Flask(__name__)


@app.route('/panchangam', methods=['GET'])
def panchangam():
    date_str= request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    time_str = request.args.get('time', '00:00:00')
    latitude= request.args.get('latitude', Coordinates.SG_LATITUDE)
    longitude = request.args.get('longitude', Coordinates.SG_LONGITUDE)
    timezone = request.args.get('timezone', 'Asia/Kolkata')

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        time = datetime.strptime(time_str, "%H:%M:%S").time()
        localdt = datetime.combine(date, time)
    except ValueError:
        return jsonify({'error': 'Invalid Date format. Use YYYY-MM-DD'}), 400


    return get_panchangam(
        localdt=localdt,
        latitude_degrees=float(latitude),
        longitude_degrees=float(longitude),
        timezone=timezone
    )

@app.route('/panchangam/monthly', methods=['GET'])
def panchangam_monthly():
    year: int = int(request.args.get('year', datetime.now().year)) 
    month: int = int(request.args.get('month', datetime.now().month)) 
    latitude= float(request.args.get('latitude', Coordinates.SG_LATITUDE))
    longitude = float(request.args.get('longitude', Coordinates.SG_LONGITUDE))
    timezone = request.args.get('timezone', DEFAULT_TIMEZONE)
    return get_monthly_panchangam(
        year=year,
        month=month,
        latitude_degrees=latitude,
        longitude_degrees=longitude,
        timezone=timezone
    )



if __name__ == "__main__": 
    app.run(debug=True, port=8000)
