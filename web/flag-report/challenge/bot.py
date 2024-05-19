from flask import Flask
from selenium import webdriver
from selenium.webdriver import ChromeOptions

URL = "http://0.0.0.0:5000"


def initialize_browser():
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    FLAG = open("./flag").read().strip()
    driver.add_cookie({"name": "FLAG", "value": FLAG})
    return driver


driver = initialize_browser()
app = Flask(__name__)


@app.route("/visit/<int:id>")
def visit(id):
    global driver
    post_url = f"{URL}/post/{id}"
    try:
        driver.get(post_url)
    except Exception as e:
        print(f"Error encountered: {e}. Restarting the browser.")
        driver.quit()
        driver = initialize_browser()
        driver.get(post_url)

    return f"Checked out {post_url}"


if __name__ == "__main__":
    app.run(debug=True)
