from flask import Flask, request, redirect, session
from flask import render_template
import sqlite3, db, config, users, meals

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

db.ensure_meals_schema()

DIETS = [
    {"id": 1, "name": "Keto"},
    {"id": 2, "name": "Vegaani"},
    {"id": 3, "name": "Gluteeniton"},
    {"id": 4, "name": "Korkeaproteiininen"}
]   

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"].strip()
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return "Error: passwords do not match"

    try:
        user_id = users.create_user(username, password1)
    except ValueError as error:
        return f"Error: {error}"

    session["user_id"] = user_id
    session["user_name"] = username
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        user = users.verify_user(username, password)
        if not user:
            return "Error: invalid username or password"

        session["user_id"] = user["id"]
        session["user_name"] = user["username"]
        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_name", None)
    return redirect("/")

@app.route("/profile")
def profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    user = users.get_user_by_id(user_id)
    if not user:
        session.pop("user_id", None)
        session.pop("user_name", None)
        return redirect("/login")

    meal_count = len(meals.get_meals_by_user(user_id))
    total_calories = sum((meal.get("calories") or 0) for meal in meals.get_meals_by_user(user_id))
    total_price = sum((meal.get("price") or 0) for meal in meals.get_meals_by_user(user_id))

    return render_template(
        "profile.html",
        user=user,
        meal_count=meal_count,
        total_calories=total_calories,
        total_price=total_price,
    )


@app.route("/user/<int:user_id>")
def user_meals(user_id):
    user = users.get_user_by_id(user_id)
    if not user:
        return "User not found", 404

    user_meals = meals.get_meals_by_user(user_id)
    return render_template("user_meals.html", user=user, meals=user_meals)


@app.route("/profile/change-password", methods=["POST"])
def change_password():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    user = users.get_user_by_id(user_id)
    if not user:
        return redirect("/login")

    if not users.verify_user(user["username"], current_password):
        return "Error: current password is incorrect"

    if not new_password or new_password != confirm_password:
        return "Error: new passwords do not match"

    users.update_password(user_id, new_password)
    return redirect("/profile")


@app.route("/profile/change-username", methods=["POST"])
def change_username():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    new_username = request.form.get("new_username", "").strip()
    password = request.form.get("password", "")

    user = users.get_user_by_id(user_id)
    if not user:
        return redirect("/login")

    if not users.verify_user(user["username"], password):
        return "Error: password is incorrect"

    if not new_username:
        return "Error: username cannot be empty"

    try:
        users.update_username(user_id, new_username)
    except ValueError as error:
        return f"Error: {error}"

    session["user_name"] = new_username
    return redirect("/profile")


@app.route("/profile/delete-account", methods=["POST"])
def delete_account():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    password = request.form.get("password", "")
    user = users.get_user_by_id(user_id)
    if not user:
        return redirect("/login")

    if not users.verify_user(user["username"], password):
        return "Error: password is incorrect"

    users.delete_user(user_id)
    session.pop("user_id", None)
    session.pop("user_name", None)
    return redirect("/")


@app.route("/")
def index():
    search_query = request.args.get("query", "").strip()
    min_price = request.args.get("min_price", "").strip()
    max_price = request.args.get("max_price", "").strip()
    selected_diets = request.args.getlist("diets")

    try:
        min_price_value = float(min_price) if min_price else None
    except ValueError:
        min_price_value = None

    try:
        max_price_value = float(max_price) if max_price else None
    except ValueError:
        max_price_value = None

    sql = """
        SELECT
            m.id,
            m.user_id,
            m.name,
            m.meal_type,
            m.calories AS total_calories,
            m.protein AS total_protein,
            m.carbs AS total_carbs,
            m.fat AS total_fat,
            m.price,
            u.username,
            m.diet_tags
        FROM meals m
        LEFT JOIN users u ON u.id = m.user_id
    """
    params = []
    conditions = []

    if search_query:
        search_value = f"%{search_query}%"
        conditions.append("(LOWER(m.name) LIKE LOWER(?) OR LOWER(m.meal_type) LIKE LOWER(?) OR CAST(m.price AS TEXT) LIKE ?)")
        params.extend([search_value, search_value, search_value])

    if min_price_value is not None:
        conditions.append("CAST(m.price AS REAL) >= ?")
        params.append(min_price_value)

    if max_price_value is not None:
        conditions.append("CAST(m.price AS REAL) <= ?")
        params.append(max_price_value)

    if selected_diets:
        diet_filters = []
        for diet_id in selected_diets:
            diet_filters.append("(',' || COALESCE(m.diet_tags, '') || ',') LIKE ?")
            params.append(f"%,{diet_id},%")
        conditions.append("(" + " OR ".join(diet_filters) + ")")

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += " ORDER BY m.created_at DESC"

    meal_rows = db.query(sql, params)
    return render_template(
        "index.html",
        meals=meal_rows,
        all_diets=DIETS,
        selected_diets=selected_diets,
        query=search_query,
        min_price=min_price,
        max_price=max_price,
    )

# Näytetään itse lomake (GET-pyyntö)
@app.route("/form")
def form():
    return render_template("form.html")

# Vastaanotetaan lomakkeen tiedot (POST-pyyntö) ja näytetään tulos
@app.route("/result", methods=["POST"])
def result():
    # Luetaan lomakkeen kenttä "message" name-attribuutin perusteella
    user_message = request.form["message"]
    
    # Välitetään viesti Jinja2-muuttujana result.html-sivupohjalle
    return render_template("result.html", message=user_message)


@app.route("/meal")
def show_form():
    return render_template("meal.html", diets=DIETS)


@app.route("/meal/<int:meal_id>")
def meal_detail(meal_id):
    meal = meals.get_meal_by_id(meal_id)
    if not meal:
        return "Meal not found", 404
    return render_template("meal_detail.html", meal=meal, diets=DIETS)


@app.route("/meal/<int:meal_id>/edit", methods=["GET", "POST"])
def edit_meal(meal_id):
    meal = meals.get_meal_by_id(meal_id)
    if not meal:
        return "Meal not found", 404

    if session.get("user_id") != meal["user_id"]:
        return "Unauthorized", 403

    if request.method == "POST":
        meals.update_meal(
            meal_id,
            name=request.form["name"],
            meal_type=request.form["meal_type"],
            calories=request.form.get("calories", 0),
            protein=request.form.get("protein", 0),
            carbs=request.form.get("carbs", 0),
            fat=request.form.get("fat", 0),
            price=request.form.get("price", 0),
        )
        return redirect("/")

    return render_template("edit_meal.html", meal=meal, diets=DIETS)


@app.route("/meal/<int:meal_id>/delete", methods=["POST"])
def delete_meal(meal_id):
    meal = meals.get_meal_by_id(meal_id)
    if not meal:
        return "Meal not found", 404

    if session.get("user_id") != meal["user_id"]:
        return "Unauthorized", 403

    meals.delete_meal(meal_id)
    return redirect("/")


# 2. POST-reitti: Otetaan lomakkeen tiedot vastaan
@app.route("/add_meal", methods=["POST"])
def add_meal():
    user_id = session.get("user_id")
    if not user_id:
        return "Error: You must be logged in to add a meal"

    name = request.form["name"]
    meal_type = request.form["meal_type"]
    calories = request.form.get("calories", 0)
    protein = request.form.get("protein", 0)
    carbs = request.form.get("carbs", 0)
    fat = request.form.get("fat", 0)
    price = request.form.get("price", 0)
    selected_diets = request.form.getlist("diets")
    diet_tags = ",".join(selected_diets)

    try:
        meal_id = meals.create_meal(
            user_id=user_id,
            name=name,
            meal_type=meal_type,
            calories=calories,
            protein=protein,
            carbs=carbs,
            fat=fat,
            price=price,
            diet_tags=diet_tags,
        )
    except ValueError as error:
        return f"Error: {error}"

    print(f"Lisätty ateria: {name} ({meal_type})")
    print(f"Makrot: {calories} kcal, {protein}g proteiinia, {carbs}g hiilihydraatteja, {fat}g rasvaa")
    print(f"Valitut luokittelu-ID:t: {selected_diets}")
    print(f"Tallennettu aterian id: {meal_id}")

    return redirect("/")

@app.route("/sqltest")
# ESIMERKKI: Aterioiden haku tietokannasta (GET)
def sqltest():
    db.execute("INSERT INTO visits (visited_at) VALUES (datetime('now'))")
    result = db.query("SELECT COUNT(*) FROM visits")
    count = result[0][0]
    return "Sivua on ladattu " + str(count) + " kertaa"



if __name__ == "__main__":
    app.run(debug=True)




