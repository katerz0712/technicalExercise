# Import Modules 
import time, os, csv, requests, string
from selenium import webdriver
from bs4 import BeautifulSoup

chromeDriverPath = 'C:/users/m3ac-tuckerk/chromedriver.exe'
driver = webdriver.Chrome(chromeDriverPath)

def navigateMailChimp():
    driver.get('https://mailchimp.com/');
    time.sleep(3)

def acceptCookie():
    acceptCookie = driver.find_element_by_class_name("optanon-alert-box-close")
    acceptCookie.click()
    time.sleep(3)

def navigateAboutMailChimp():
    aboutLink = driver.find_element_by_class_name("site-footer") and driver.find_element_by_link_text('About MailChimp')
    aboutLink.click()
    time.sleep(3)

def soup():
    about = requests.get('https://mailchimp.com/about/')
    soup = BeautifulSoup(about.text, 'html.parser')

    # Take out the link for current job postings
    careerLink = soup.find(class_='btn ghost on_dark')
    careerLink.decompose()

    # Find all of the leadership team entries in the HTML - place in list
    leadershipTeam = soup.find(class_='row pb3 center')
    leaderList = leadershipTeam.find_all('a')

    # Create CSV File and open for writing
    file = open('mailChimpLeadershipTeam.csv', 'w', encoding='utf-8')
    csvWriter = csv.writer(file)
    csvWriter.writerow(['Name', 'Position', 'Description'])

    # Loop through the list and write the data to the CSV
    for entry in leaderList:
        name = entry.get('data-title')
        position = entry.get('data-position')
        description = entry.get('data-description')
        newDescription = description.replace('â', '\u0027')
        print(newDescription)
        csvWriter.writerow([name, position, newDescription])

    file.close()    
    

def main():
    navigateMailChimp()
    acceptCookie()
    URL = navigateAboutMailChimp()
    soup()
    driver.quit()  
    

main()
