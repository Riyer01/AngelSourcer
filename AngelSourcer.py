#AngelSourcer
#A script that automates reaching out to candidates on AngelList 
#Written for Black SMS
#By Ray Iyer

#coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time


SOURCE_URL = 'https://angel.co/black-sms/source?query=%22React%22&refinementList%5Blocations%5D%5B0%5D=San%20Francisco%20Bay%20Area&refinementList%5Bprimary_role%5D%5B0%5D=Software%20Engineer&refinementList%5Blooking_for%5D%5B0%5D=Full%20Time&refinementList%5Bdev_bootcamp%5D%5B0%5D=false&refinementList%5Btags_skills%5D=&numeric%5Byears_experience_in_primary_role%5D%5Bmin%5D=2&numeric%5Byears_experience_in_primary_role%5D%5Bmax%5D=20&numeric%5Btop_X_user_startup%5D%5Bmin%5D=0&numeric%5Btop_X_user_startup%5D%5Bmax%5D=20'

OUTREACH = ". I hope you are doing well and enjoying your summer! I'm reaching out because we are building out a stellar team at Black SMS (http://blacksms.net). We are backed by the best and work with some pretty awesome people, like the 14th employee at Firebase (acquired by Google) and the first iOS engineer at Hike Messenger, a unicorn startup that developed one of India's most popular messengers with over 100 million active users. You would have the opportunity to be one of the first 3 engineers at a super high-potential startup! If you are interested in joining a team of intentional, intelligent developers, I'd love to chat."

def initializeAngelList():
	print("Loading AngelList source...")
	driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
	#driver = webdriver.Chrome()
	driver.get(SOURCE_URL)
	if driver.title != "Source - AngelList Talent":
		driver.get('https://angel.co/login')
		login(driver)
		driver.get(SOURCE_URL)

	return driver
	

def login(driver):
	print("Logging in...")
	username = raw_input("What is your AngelList email? ")
	password = raw_input("What is your password? ")
	userElem = driver.find_element_by_id('user_email')
	userElem.send_keys(username)
	passElem = driver.find_element_by_id('user_password')
	passElem.send_keys(password)
	submitElem = driver.find_element_by_name('commit')
	submitElem.click()



#Loads all of the profiles to reach out to by continuously scrolling until everything has been loaded
def load_profiles(driver):
    """A method for scrolling the page."""
    print("Waiting for profiles to load...")
    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(8)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def send_messages(driver):
	time.sleep(15)
	introButtons = driver.find_elements_by_css_selector('.icon-only')
	print("Found %s potential candidates..." % len(introButtons))
	print("Sending messages...")

	for button in introButtons:
		button.click()

	textboxes = driver.find_elements_by_tag_name("textarea")
	textboxes.pop() #Bug fix, removes trailing textbox (not an actual candidate profile)
	for i, textbox in enumerate(textboxes):
		#Sneaky trick, get candidates name from textbox placeholder, use to personalize message
		name = textbox.get_attribute('placeholder').split()[4]
		textbox.send_keys("Hey, " + name + OUTREACH)
		if (i + 1) % 10 == 0:
			print("%s candidate messages pasted..." % (i + 1))

	sendButtons = driver.find_elements_by_xpath('//input[@type="submit" and @value="Send and Get Intro"]')
	for sendButton in sendButtons:
		sendButton.click()


def main():
	driver = initializeAngelList()
	load_profiles(driver)
	send_messages(driver)
	
if __name__ == "__main__":
	main()

