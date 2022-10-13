from flight_search import FlightSearch
from datetime import datetime, timedelta
from flask import render_template, redirect, request, flash
from markupsafe import Markup
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from forms import SignInForm, FlightSearchForm
from common import db, app, User, FlightData


# Initializes Bootstrap and the Flask Login Manager
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)


# Initialized the Flask user manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Get today's date and the end date (6 months from today) formatted
today = datetime.today().date().strftime("%d/%m/%Y")
search_end_date = (datetime.today() + timedelta(days=180)).strftime("%d/%m/%Y")

def get_year():
    return datetime.now().year


# Returns the home route
@app.route("/")
def home():
    return render_template("index.html")


# Returns the login route. Upon form submission, performs several verification checks and logs the user in if successful
@app.route("/login", methods=["POST", "GET"])
def login():
    form = SignInForm()
    if form.validate_on_submit():
        entered_email = form.email.data
        entered_password = form.password.data
        user = User.query.filter_by(email=entered_email).first()
        if user:
            if check_password_hash(user.password, entered_password):
                login_user(user)
                return redirect('/account/home')
            else:
                flash("The password is incorrect")
                return redirect("/login")
        else:
            flash("This email does not exist")
            return redirect("/login")
    return render_template("login.html", form=form)


# Returns the register route. Makes sure the User is in the DB and performs several other verification checks.
@app.route('/register', methods=["GET", "POST"])
def register():
    form = SignInForm()
    if form.validate_on_submit():
        entered_email = form.email.data
        user = User.query.filter_by(email=entered_email).first()
        if user:
            flash("This email already exists")
            return redirect("/login")
        else:
            new_user = User(
                email=entered_email,
                password=generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect('account/home')
    return render_template("register.html", form=form)


# Returns the Account Home main page. Requires login
@app.route("/account/home", methods=["GET", "POST"])
@login_required
def account_home():
    return render_template("account/home.html")


# Returns the Search page. Performs some checks to make sure the data entered is correect and alerts the user otherwise
# Requires login
@app.route("/account/search", methods=["GET", "POST"])
@login_required
def search():
    form = FlightSearchForm()
    if form.validate_on_submit():
        flights_engine = FlightSearch()
        from_city = form.fly_from.data
        to_city = form.fly_to.data
        min_nights = form.min_nights.data
        max_nights = form.max_nights.data
        try:
            from_iata_code = flights_engine.get_IATA(from_city)
        except IndexError:
            flash("Sorry, there are no flights from that location!")
            return redirect("/account/search")
        try:
            to_iata_code = flights_engine.get_IATA(to_city)
            results = flights_engine.get_flights(
                from_code=from_iata_code,
                to_code=to_iata_code,
                today=today,
                future_date=search_end_date,
                nights_min=min_nights,
                nights_max=max_nights)
            if results == []:
                flash("Sorry, there are no flights betweem those locations!")
                return redirect("/account/search")
        except IndexError:
            flash("Sorry, there are no flights to that location!")
            return redirect("/account/search")

        # Here, we check that the price of the cheapest price is lower than our target and add it to the user account
        if results[0]["price"] <= form.target_price.data:
            flight = results[0]
            new_flight = FlightData(
                to_city=flight["cityTo"],
                from_city=flight["cityFrom"],
                to_iata_code=flight["flyTo"],
                from_iata_code=flight["flyFrom"],
                from_date=flight["route"][0]['local_departure'].split("T")[0],
                to_date=flight["route"][-1]['local_arrival'].split("T")[0],
                price=flight["price"],
                url=flight["deep_link"],
                user_id=current_user.id
            )
            db.session.add(new_flight)
            db.session.commit()
            return redirect("/account/home")
        else:
            flash("Sorry, there are no flights that cheap! Try raising your price")
            return redirect("/account/search")
    return render_template("account/search.html", form=form)


# This route is used to delete a saved flight
@app.route("/delete-entry<int:flight_id>")
@login_required
def delete_entry(flight_id):
    flight_to_delete = FlightData.query.filter_by(id=flight_id).first()
    db.session.delete(flight_to_delete)
    db.session.commit()
    flash("Entry Deleted")
    return redirect("/account/home")


# Logout the current user
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

# Enables lazy loading
if __name__ == "__main__":
    app.run(debug=True, port=5001)
