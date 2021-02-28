from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, SelectField, ValidationError
from wtforms.validators import DataRequired, Optional
from wtforms.fields.html5 import DateField
from datetime import datetime


# Custom validators
class NotLessThan(object):
    """
    Verifies that the value entered in a field is not smaller than the value
    entered in another field.
    """
    def __init__(self, fieldname):
        self.fieldname = fieldname

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(
                field.gettext("Invalid field name '%s'.") % self.fieldname
            )

        if int(field.data) < int(other.data):
            message = f"{field.label.text} should be longer than " \
                      f"{form[self.fieldname].label.text}"
            raise ValidationError(message)


class NotInThePast(object):
    """
    Verifies that the value entered in a datetime field is not in the past.
    """
    def __call__(self, form, field):
        if field.data < datetime.now().date():
            raise ValidationError('Flight time cannot be in the past')


class DateAfter(object):
    """
    Verifies that the value entered in a datetime field is later than the
    datetime entered in another field. If no other field is provided then it
    compares against the current date.
    """
    def __init__(self, fieldname=''):
        self.fieldname = fieldname

    def __call__(self, form, field):
        try:
            other_field = form[self.fieldname]
        except KeyError:
            other_field_time = datetime.now().date()
            err_message = "Flight time cannot be in the past"
        else:
            other_field_time = other_field.data
            err_message = f"{field.label.text} should be " \
                          f"after '{form[self.fieldname].label.text}'"
        if field.data < other_field_time:
            raise ValidationError(err_message)


# Flight details form for 'index.html'
class FlightDetailsForm(FlaskForm):
    departure_city = StringField("Departure City", validators=[DataRequired()])
    arrival_city = StringField("Arrival City", validators=[DataRequired()])
    return_trip = BooleanField("Return?")
    earliest_departure = DateField(
        "Earliest Departure Date",
        validators=[DataRequired(), NotInThePast()]
    )
    latest_departure = DateField(
        "Latest Departure Date",
        validators=[DataRequired(), NotInThePast(), DateAfter('earliest_departure')]
    )
    min_length = SelectField(
        "Min Trip Length",
        choices=[('1', '1 day')] + [(str(x), str(x) + ' days') for x in range(2, 31)],
        validators=[Optional()]
    )
    max_length = SelectField(
        "Max Trip Length",
        choices=[('1', '1 day')] + [(str(x), str(x) + ' days') for x in range(2, 31)],
        validators=[Optional(), NotLessThan('min_length')]
    )
    max_stopovers = SelectField(
        "Maximum Number of Stopovers",
        choices=[('0', '0 (direct flights only)')] + [(str(x), str(x)) for x in range(1, 4)]
    )
    submit = SubmitField("Search Flights")
