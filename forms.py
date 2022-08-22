from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Email


class SignInForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class FlightSearchForm(FlaskForm):
    fly_from = StringField("Home City", validators=[DataRequired(), Length(max=25)])
    fly_to = StringField("Destination City", validators=[DataRequired(), Length(max=25)])
    min_nights = IntegerField("Min Nights in Destination", validators=[DataRequired()])
    max_nights = IntegerField("Max Nights in Destination", validators=[DataRequired()])
    target_price = IntegerField("Max Target Price", validators=[DataRequired()])
    submit = SubmitField("Submit")



