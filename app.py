from flask import Flask, request, render_template_string, abort
import requests
import os

app = Flask(__name__)

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
if not WEBHOOK_URL:
    raise RuntimeError("DISCORD_WEBHOOK_URL not set")

ASSESSMENT_PACKAGES = [
    "Basic Package",
    "Standard Package",
    "Premium Package"
]

GRADE_LEVELS = [
    "Grade 7", "Grade 8", "Grade 9", "Grade 10"
]

TEST_TYPES = [
    "Periodic Test",
    "Summative Test"
]

TOS_FORMATS = [
    "Bloom's Taxonomy format",
    "21st Century Skills format"
]

HTML_FORM = """
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Buyer Info Form</title>
<style>
body { font-family: Arial, sans-serif; padding:1em; max-width:500px; margin:auto; background:#f9f9f9;}
label {font-weight:bold; display:block; margin-top:1em;}
input, select, textarea {width:100%; padding:0.7em; margin-top:0.3em;}
button, input[type=submit] {margin-top:1em;}
#reviewContent {white-space:pre-wrap;background:#eef;padding:1em;}
</style>

<script>
function toggleOptions() {
  const pkg = document.getElementById("package").value;
  document.getElementById("tos-format").style.display = pkg === "Basic Package" ? "none" : "block";
  document.getElementById("days-input").style.display = pkg === "Premium Package" ? "block" : "none";
  document.getElementById("days-dropdown").style.display = pkg === "Standard Package" ? "block" : "none";
  document.getElementById("days-fixed").style.display = pkg === "Basic Package" ? "block" : "none";
}
</script>
</head>

<body>
<h2>Fill-out na, KasaMath!</h2>

<form method="post">
<label>Name</label>
<input name="name" required>

<label>Email</label>
<input type="email" name="email" required>

<label>Grade Level</label>
<select name="grade" required>
  <option value="" disabled selected>Select grade</option>
  {% for g in grades %}
  <option value="{{ g }}">{{ g }}</option>
  {% endfor %}
</select>

<label>Test Type</label>
<select name="test_type" required>
  <option value="" disabled selected>Select test type</option>
  {% for t in test_types %}
  <option value="{{ t }}">{{ t }}</option>
  {% endfor %}
</select>

<label>Assessment Package</label>
<select name="package" id="package" onchange="toggleOptions()" required>
  <option value="" disabled selected>Select package</option>
  {% for p in packages %}
  <option value="{{ p }}">{{ p }}</option>
  {% endfor %}
</select>

<div id="tos-format" style="display:none;">
<label>TOS Format</label>
<select name="tos">
  {% for f in tos_formats %}
  <option value="{{ f }}">{{ f }}</option>
  {% endfor %}
</select>
</div>

<div id="days-fixed" style="display:none;">
<label>Number of Days</label>
<input value="35 days" readonly>
</div>

<div id="days-dropdown" style="display:none;">
<label>Number of Days</label>
<select name="days">
  <option value="35 days">35 days</option>
  <option value="40 days">40 days</option>
</select>
</div>

<div id="days-input" style="display:none;">
<label>Number of Days</label>
<input name="days" placeholder="e.g. 42 days">
</div>

<label>Header Info</label>
<textarea name="order" rows="6" required>
Republic of the Philippines
Department of Education
National Capital Region
SCHOOLS DIVISION OFFICE QUEZON CITY
SAUYO HIGH SCHOOL
Pantabangan St., NIA Village, Sauyo, Quezon City
</textarea>

<input type="submit" value="Submit">
</form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def collect_info():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        grade = request.form.get("grade")
        test_type = request.form.get("test_type")
        package = request.form.get("package")
        tos = request.form.get("tos", "Bloom's Taxonomy format")
        days = request.form.get("days", "35 days")
        order = request.form.get("order", "").strip()

        if grade not in GRADE_LEVELS:
            abort(400)
        if test_type not in TEST_TYPES:
            abort(400)
        if package not in ASSESSMENT_PACKAGES:
            abort(400)
        if tos not in TOS_FORMATS:
            abort(400)
        if len(order) > 2000:
            abort(400)

        message = (
            f"New Buyer Submission\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Grade: {grade}\n"
            f"Test Type: {test_type}\n"
            f"Package: {package}\n"
            f"TOS: {tos}\n"
            f"Days: {days}\n"
            f"Header:\n{order}"
        )

        requests.post(WEBHOOK_URL, json={"content": message})
        return "<h3>Submitted</h3>"

    return render_template_string(
        HTML_FORM,
        grades=GRADE_LEVELS,
        test_types=TEST_TYPES,
        packages=ASSESSMENT_PACKAGES,
        tos_formats=TOS_FORMATS
    )

if __name__ == "__main__":
    app.run()
