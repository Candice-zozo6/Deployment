import csv
from flask import Flask, render_template, request

app = Flask(__name__)

def load_animals():
    ###
    # Reading the data from a CSV file
    ###
    animals = []
    with open("animals.csv", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            animals.append(row)
    return animals

def filter_animals(animals):
    animal_type = request.args.get("type", "")
    sex = request.args.get("sex", "")
    outcome = request.args.get("outcome", "")
    health = request.args.get("health", "")
    reason = request.args.get("reason", "")
    max_days = request.args.get("max_days", "")
    filtered = []
    for animal in animals:
        if animal_type and animal["type"] != animal_type:
            continue
        if sex and animal["sex"] != sex:
            continue
        if outcome and animal["outcome"] != outcome:
            continue
        if health and animal["health"] != health:
            continue
        if reason and animal["reason"] != reason:
            continue
        if max_days.isdigit():
            # animals still in the shelter have no number of days
            if animal["days"] == "" or int(animal["days"]) > int(max_days):
                continue
        filtered.append(animal)
    return filtered

@app.get("/")
def index():
    animals = load_animals()
    filtered = filter_animals(animals)
    max_days = request.args.get("max_days", "")
    error = ""
    if max_days and not max_days.isdigit():
        error = "Please enter a whole number of days."
    return render_template("index.html",
                           animals=filtered[:50],
                           types=sorted({animal["type"] for animal in animals}),
                           sexes=sorted({animal["sex"] for animal in animals}),
                           outcomes=sorted({animal["outcome"] for animal in animals}),
                           healths=sorted({animal["health"] for animal in animals}),
                           reasons=sorted({animal["reason"] for animal in animals}),
                           selected_type=request.args.get("type", ""),
                           selected_sex=request.args.get("sex", ""),
                           selected_outcome=request.args.get("outcome", ""),
                           selected_health=request.args.get("health", ""),
                           selected_reason=request.args.get("reason", ""),
                           max_days=max_days,
                           matching=len(filtered),
                           total=len(animals),
                           error=error)

if __name__ == "__main__":
    app.run()
    