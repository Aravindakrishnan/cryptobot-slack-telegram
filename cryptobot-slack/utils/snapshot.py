from selenium import webdriver
from utils.chart import fullscreen, get_chart_id
from time import sleep  

def snapshot_chart(coinname,chart_time):
        
    driver = webdriver.Chrome(executable_path="E:\chromedriver.exe")
    url = f"https://coinmarketcap.com/currencies/{coinname}/"
    driver.get(url)

    #scroll down for finding chart
    sleep(3)
    driver.execute_script("window.scrollTo(0,680)")
   
    #get_particular_chart
    sleep(2)
    chart_id = get_chart_id(chart_time)
    driver.find_element_by_id(chart_id).click() 

    # fullscreen chart view
    sleep(3)
    driver.find_element_by_xpath(fullscreen()).click()

    #saving the chart   
    sleep(2)
    driver.save_screenshot(".\static\charts\chart.png")
    
    sleep(2)
    driver.close()

