from flask import Flask, render_template, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pickle
import pandas as pd
import os

app = Flask(__name__)

# Function to get a headless Selenium driver
import undetected_chromedriver as uc

def get_driver():
    chrome_options = uc.ChromeOptions()
    chrome_options.headless = True
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=chrome_options)  # Use undetected chromedriver
    return driver



# Function to log in and save cookies
def login_and_save_cookies(email, password):
    driver = get_driver()
    driver.get("https://login.live.com/")
    time.sleep(3)
    
    driver.find_element("name", "loginfmt").send_keys(email)
    driver.find_element("name", "loginfmt").send_keys("\n")
    time.sleep(3)
    
    driver.find_element("name", "passwd").send_keys(password)
    driver.find_element("name", "passwd").send_keys("\n")
    time.sleep(5)
    
    try:
        driver.find_element("id", "idSIButton9").click()
        time.sleep(3)
    except:
        pass
    
    with open("cookies.pkl", "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    
    driver.quit()

# Function to perform Bing search
def bing_search(queries):
    driver = get_driver()
    driver.get("https://www.bing.com/")
    time.sleep(2)
    
    if os.path.exists("cookies.pkl"):
        with open("cookies.pkl", "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
    
    results_list = []
    
    for query in queries:
        driver.get("https://www.bing.com/news/")
        time.sleep(2)
        
        search_box = driver.find_element("name", "q")
        search_box.send_keys(query)
        search_box.send_keys("\n")
        time.sleep(3)
        
        results = driver.find_elements("css selector", "a.title")[:5]
        
        for result in results:
            results_list.append({"query": query, "title": result.text, "url": result.get_attribute("href")})
    
    driver.quit()
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
        queries = []
        if "file" in request.files:
            file = request.files["file"]
            queries = pd.read_csv(file).iloc[:, 0].tolist()
        else:
            queries = request.form["queries"].split("\n")
        
        results = bing_search(queries)
        return render_template("results.html", results=results)
    
    return render_template("search.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)
