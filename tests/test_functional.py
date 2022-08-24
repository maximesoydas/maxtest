from urllib import response
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from flask_testing import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_purchase_1_place():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('http://127.0.0.1:5000/')
    element = driver.find_element(By.NAME,'email')
    element.send_keys('admin@irontemple.com')
    element.send_keys(Keys.ENTER)
    element = driver.find_element(By.CSS_SELECTOR,'body > h2')
    assert 'Welcome' in element.text
    element = driver.find_element(By.NAME,'club_points')
    club_points = str(element.text).replace('Points available: ',"")
    element = driver.find_element(By.NAME,'Winter Fitness_points')
    comp_points = str(element.text).replace('Number of Places: ',"")
    element = driver.find_element(By.NAME,'Winter Fitness_places')
    element.click()
    element = driver.find_element(By.NAME,'places')
    element.send_keys('1')
    element = driver.find_element(By.CSS_SELECTOR,'body > form > button')
    element.click()
    element = driver.find_element(By.CSS_SELECTOR,'body > ul:nth-child(3) > li')
    assert 'Great' in element.text
    element = driver.find_element(By.NAME,'club_points')
    refreshed_club_points = str(element.text).replace('Points available: ',"")
    element = driver.find_element(By.NAME,'Winter Fitness_points')
    refreshed_comp_points = str(element.text).replace('Number of Places: ',"")
    assert int(refreshed_club_points) == int(club_points) - 1
    assert int(refreshed_comp_points) == int(comp_points) - 1
    driver.close()
    
def test_login_purchase_13_places():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('http://127.0.0.1:5000/')
    element = driver.find_element(By.NAME,'email')
    element.send_keys('admin@irontemple.com')
    element.send_keys(Keys.ENTER)
    element = driver.find_element(By.CSS_SELECTOR,'body > h2')
    assert 'Welcome' in element.text
    element = driver.find_element(By.NAME,'club_points')
    club_points = element.text.replace('Points available: ','')
    element = driver.find_element(By.NAME,'Winter Fitness_points')
    comp_points = element.text.replace('Number of Places:','')
    element = driver.find_element(By.NAME,'Winter Fitness_places')
    element.click()
    element = driver.find_element(By.NAME,'places')
    element.send_keys('13')
    element = driver.find_element(By.CSS_SELECTOR,'body > form > button')
    element.click()
    element = driver.find_element(By.CSS_SELECTOR,'body > ul:nth-child(3) > li')
    assert 'You cannot request more than 12 places for a competition' in element.text
    element = driver.find_element(By.NAME,'club_points')
    refreshed_club_points = element.text.replace('Points available: ','')
    element = driver.find_element(By.NAME,'Winter Fitness_points')
    refreshed_comp_points = element.text.replace('Number of Places:','')
    assert refreshed_club_points == club_points
    assert refreshed_comp_points == comp_points
    driver.close()

def test_login_purchase_1_place_0_club_points():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('http://127.0.0.1:5000/')
    element = driver.find_element(By.NAME,'email')
    element.send_keys('points@gain.com')
    element.send_keys(Keys.ENTER)
    element = driver.find_element(By.CSS_SELECTOR,'body > h2')
    assert 'Welcome' in element.text
    element = driver.find_element(By.NAME,'club_points')
    club_points = str(element.text).replace('Points available: ',"")
    element = driver.find_element(By.NAME,'Winter Fitness_points')
    comp_points = str(element.text).replace('Number of Places: ',"")
    element = driver.find_element(By.NAME,'Winter Fitness_places')
    element.click()
    element = driver.find_element(By.NAME,'places')
    element.send_keys('1')
    element = driver.find_element(By.CSS_SELECTOR,'body > form > button')
    element.click()
    element = driver.find_element(By.CSS_SELECTOR,'body > ul:nth-child(3) > li')
    assert 'You do not have enough club points' in element.text
    element = driver.find_element(By.NAME,'club_points')
    refreshed_club_points = str(element.text).replace('Points available: ',"")
    element = driver.find_element(By.NAME,'Winter Fitness_points')
    refreshed_comp_points = str(element.text).replace('Number of Places: ',"")
    assert refreshed_club_points == club_points
    assert refreshed_comp_points == comp_points
    driver.close()
    
def test_logout():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('http://127.0.0.1:5000/')
    element = driver.find_element(By.NAME,'email')
    element.send_keys('admin@irontemple.com')
    element.send_keys(Keys.ENTER)
    element = driver.find_element(By.CSS_SELECTOR,'body > h2')
    assert 'Welcome' in element.text
    element = driver.find_element(By.NAME,'_logout')
    element.click()
    assert driver.current_url == 'http://127.0.0.1:5000/'
    driver.close()
  