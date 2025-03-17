from flask import Flask, render_template, request, jsonify
from projects_code.norm_mut_logic import run_norm_mut_test

application = Flask(__name__)

def render_page(template):
    """Helper function to serve full page or just the content for AJAX requests"""
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render_template(template)  # Only return content for AJAX
    return render_template("base.html", content=render_template(template))  # Return full page

@application.route('/')
def home():
    return render_page("index.html")

@application.route('/projects')
def projects():
    return render_page("projects.html")

@application.route('/about')
def about():
    return render_page("about.html")

@application.route('/contact')
def contact():
    return render_page("contact.html")

@application.route('/norm-mut-test', methods=["GET", "POST"])
def norm_mut_test():
    if request.method == "POST":
        test_cases = request.json.get("test_cases", [])  # Get JSON test cases
        results = run_norm_mut_test(test_cases)  # Calls the function from norm_mut_logic.py
        return jsonify(results)  # Return results as JSON
    
    return render_page("norm-mut-test.html")

@application.route('/task-manager')
def task_manager():
    return render_page("task-manager.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8080)
