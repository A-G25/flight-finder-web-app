from datetime import datetime
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from app.forms import FlightDetailsForm
from app.data_manager import DataManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)


@app.route('/', methods=["GET", "POST"])
def home_page():
    form = FlightDetailsForm()
    return render_template('index.html', form=form)


@app.route('/flight_search', methods=["GET", "POST"])
def flight_search():
    form = FlightDetailsForm(request.args, meta={'csrf': False})
    if form.validate():
        data_manager = DataManager()

        data_manager.set_origin(
            departure_city=request.args.get('departure_city')
        )
        data_manager.set_destinations(
            destination_cities=request.args.get('arrival_city')
        )

        earliest_departure = datetime.strptime(
            request.args.get('earliest_departure'), "%Y-%m-%d"
        )
        latest_departure = datetime.strptime(
            request.args.get('latest_departure'), "%Y-%m-%d"
        )

        if form.return_trip.data:
            data_manager.trip_type = "return"

        data_manager.check_flights(
            from_time=earliest_departure.strftime("%d/%m/%Y"),
            to_time=latest_departure.strftime("%d/%m/%Y"),
            stop_overs=request.args.get('max_stopovers'),
            nights_in_dst_from=request.args.get('min_length'),
            nights_in_dst_to=request.args.get('max_length'),
        )

        return render_template(
            "flight_list.html",
            destinations=data_manager.destinations,
            departure_city=data_manager.origin["city"],
        )
    else:
        return render_template("index.html", form=form)


if __name__ == '__main__':
    app.run()
