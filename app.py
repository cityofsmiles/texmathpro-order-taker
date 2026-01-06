from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://canary.discord.com/api/webhooks/1437299022716207115/swf5n0l7mEd1_AoroaTVX6qbufQwSl2Wfi_LxyBoJbvD3yhn2bD3Hc2SSvM2JLDtSHxK"

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
    body {
      font-family: Arial, sans-serif;
      padding: 1em;
      max-width: 500px;
      margin: auto;
      background: #f9f9f9;
    }
    h2 {
      text-align: center;
    }
    label {
      font-weight: bold;
      display: block;
      margin-top: 1em;
    }
    input, select, textarea {
      width: 100%;
      padding: 0.7em;
      margin-top: 0.3em;
      border: 1px solid #ccc;
      border-radius: 5px;
      box-sizing: border-box;
    }
    input[type=submit], button {
      background-color: #4CAF50;
      color: white;
      border: none;
      margin-top: 1em;
      padding: 0.7em;
      cursor: pointer;
      width: 100%;
      border-radius: 5px;
    }
    input[type=submit]:hover, button:hover {
      background-color: #45a049;
    }
    #reviewContent {
      white-space: pre-wrap;
      background: #eef;
      padding: 1em;
      border-radius: 5px;
    }
  </style>
  <script>
    function toggleOptions() {
      const pkg = document.getElementById("package").value;
      document.getElementById("tos-fixed").style.display = pkg === "Basic Package" ? "block" : "none";
      document.getElementById("tos-format").style.display = pkg !== "Basic Package" ? "block" : "none";
      document.getElementById("days-fixed").style.display = pkg === "Basic Package" ? "block" : "none";
      document.getElementById("days-dropdown").style.display = pkg === "Standard Package" ? "block" : "none";
      document.getElementById("days-input").style.display = pkg === "Premium Package" ? "block" : "none";
    }

    function showReview() {
      const form = document.getElementById("orderForm");
      const review = document.getElementById("reviewSection");
      const content = document.getElementById("reviewContent");

      const name = form.name.value;
      const email = form.email.value;
      const grade = form.grade.value;
      const testType = form.test_type.value;
      const package = form.package.value;
      const order = form.order.value;

      let tos = "N/A";
      let days = "N/A";

      if (package === "Basic Package") {
        tos = "Bloom's Taxonomy format";
        days = "35 days";
      } else {
        const tosSelect = document.querySelector('#tos-format select');
        if (tosSelect) {
          tos = tosSelect.options[tosSelect.selectedIndex].value;
        }

        if (package === "Standard Package") {
          const daysDropdown = document.querySelector('#days-dropdown select');
          if (daysDropdown) {
            days = daysDropdown.options[daysDropdown.selectedIndex].value;
          }
        } else if (package === "Premium Package") {
          const daysInput = document.querySelector('#days-input input');
          if (daysInput) {
            days = daysInput.value;
          }
        }
      }

      // Sync hidden fields for submission
      document.getElementById("tos_final").value = tos;
      document.getElementById("days_final").value = days;

      content.textContent =
        `🛍️ New Buyer Submission\n` +
        `Name: ${name}\n` +
        `Email: ${email}\n` +
        `Grade Level: ${grade}\n` +
        `Test Type: ${testType}\n` +
        `Assessment Package: ${package}\n` +
        `TOS Format: ${tos}\n` +
        `Number of Days: ${days}\n` +
        `Order Notes:\n${order}`;

      form.style.display = "none";
      review.style.display = "block";
      return false;
    }

    function submitForm() {
      document.getElementById("orderForm").submit();
    }

    function editForm() {
      document.getElementById("orderForm").style.display = "block";
      document.getElementById("reviewSection").style.display = "none";
    }
  </script>
</head>
<body>
  <h2>Fill-out na, KasaMath!</h2>
  <form id="orderForm" method="post" onsubmit="return showReview()">
    <label>Name:</label>
    <input type="text" name="name" required>

    <label>Email:</label>
    <input type="email" name="email" required>

    <label>Grade Level:</label>
    <select name="grade" required>
      {% for grade in grades %}
        <option value="{{ grade }}">{{ grade }}</option>
      {% endfor %}
    </select>

    <label>Test Type:</label>
    <select name="test_type" required>
      {% for test_type in test_types %}
        <option value="{{ test_type }}">{{ test_type }}</option>
      {% endfor %}
    </select>

    <label>Select Assessment Package:</label>
    <select name="package" id="package" onchange="toggleOptions()" required>
      {% for item in packages %}
        <option value="{{ item }}">{{ item }}</option>
      {% endfor %}
    </select>

    <div id="tos-fixed" style="display:none;">
      <label>TOS Format:</label>
      <input type="text" name="tos" value="Bloom's Taxonomy format" readonly>
    </div>

    <div id="tos-format" style="display:none;">
      <label>TOS Format:</label>
      <select name="tos">
        {% for format in tos_formats %}
          <option value="{{ format }}">{{ format }}</option>
        {% endfor %}
      </select>
    </div>

    <div id="days-fixed" style="display:none;">
      <label>Number of Days:</label>
      <input type="text" name="days" value="35 days" readonly>
    </div>

    <div id="days-dropdown" style="display:none;">
      <label>Number of Days:</label>
      <select name="days">
        <option value="35 days">35 days</option>
        <option value="40 days">40 days</option>
      </select>
    </div>

    <div id="days-input" style="display:none;">
      <label>Number of Days:</label>
      <input type="text" name="days" placeholder="e.g. 42 days">
    </div>

    <label>Palitan po ang Infos para sa Header:</label>
    <textarea name="order" rows="6" required>
Republic of the Philippines
Department of Education
National Capital Region
SCHOOLS DIVISION OFFICE QUEZON CITY
SAUYO HIGH SCHOOL
Pantabangan St., NIA Village, Sauyo, Quezon City
    </textarea>

    <!-- Hidden fields to sync review values -->
    <input type="hidden" name="tos_final" id="tos_final">
    <input type="hidden" name="days_final" id="days_final">

    <input type="submit" value="Review Before Submit">
  </form>

  <div id="reviewSection" style="display:none;">
    <h3>📋 Review Your Submission</h3>
    <div id="reviewContent"></div>
    <button onclick="submitForm()">✅ Confirm and Submit</button>
    <button onclick="editForm()">✏️ Edit</button>
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def collect_info():
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        grade = request.form.get("grade", "")
        test_type = request.form.get("test_type", "")
        package = request.form.get("package", "")
        order = request.form.get("order", "").strip()
        tos = request.form.get("tos_final", "N/A")
        days = request.form.get("days_final", "N/A")

    
        message = (
            f"🛍️ **New Buyer Submission**\n"
            f"**Name:** {name}\n"
            f"**Email:** {email}\n"
            f"**Grade Level:** {grade}\n"
            f"**Test Type:** {test_type}\n"
            f"**Assessment Package:** {package}\n"
            f"**TOS Format:** {tos}\n"
            f"**Number of Days:** {days}\n"
            f"**Header:** {order}"
        )

        response = requests.post(WEBHOOK_URL, json={"content": message})
        return f"<h3>✅ Submitted!</h3><p>Discord responded with status: {response.status_code}</p><p>Paki-screenshot na lang po ng payment at isend sa akin. Isesend ko sa e-mail ang files after payment. Thank you po sa pagsuporta sa TeXMathPro!</p>"

    return render_template_string(
        HTML_FORM,
        packages=ASSESSMENT_PACKAGES,
        grades=GRADE_LEVELS,
        test_types=TEST_TYPES,
        tos_formats=TOS_FORMATS
    )

if __name__ == "__main__":
    app.run(debug=True)
