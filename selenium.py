from selenium import webdriver
options = webdriver.EdgeOptions()
options.binary_location = "edgedriver_win64\msedgedriver.exe"
driver = webdriver.Edge(options=options)
driver.get("https://www.google.fr")