from flask import Flask, render_template, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pickle
import pandas as pd

app = Flask(__name__)

driver = None  # Global driver instance to keep session active

# Function to log in and save cookies
def login_and_save_cookies(email, password):
    global driver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get("https://login.live.com/")
    time.sleep(3)

    driver.find_element(By.NAME, "loginfmt").send_keys(email + Keys.RETURN)
    time.sleep(3)
    driver.find_element(By.NAME, "passwd").send_keys(password + Keys.RETURN)
    time.sleep(5)

    try:
        driver.find_element(By.ID, "idSIButton9").click()
        time.sleep(3)
    except:
        pass

    with open("cookies.pkl", "wb") as f:
        pickle.dump(driver.get_cookies(), f)

# Function to perform Bing search
def bing_search(queries):
    global driver
    if not driver:
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.bing.com/")
        time.sleep(2)

        with open("cookies.pkl", "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)

    driver.get("https://www.bing.com/news/")
    time.sleep(2)

    results_list = []

    for query in queries:
        driver.get("https://www.bing.com/news/")
        time.sleep(2)

        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query + Keys.RETURN)
        time.sleep(3)

        results = driver.find_elements(By.CSS_SELECTOR, "a.title")[:5]

        for result in results:
            results_list.append({"query": query, "title": result.text, "url": result.get_attribute("href")})

    return results_list

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        login_and_save_cookies(email, password)
        return redirect(url_for("search"))
    return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            queries = pd.read_csv(file).iloc[:, 0].tolist()
        else:
            queries = request.form["queries"].split("\n")

        results = bing_search(queries)
        return render_template("results.html", results=results)

    return render_template("search.html")

if __name__ == "__main__":
    app.run(debug=True)
