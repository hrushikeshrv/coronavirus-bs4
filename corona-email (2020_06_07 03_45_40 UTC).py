import bs4
import requests
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_data():

    count_page = requests.get('https://www.worldometers.info/coronavirus/country/india/')
    count_page_bs4 = bs4.BeautifulSoup(count_page.text, features='lxml')

    cases = count_page_bs4.select("div[class='maincounter-number'] span")
    cases = list(cases)

    infections_str = str(cases[0]).split('>')[1].split('<')[0]
    infections = int(''.join(infections_str.split(',')))

    deaths_str = str(cases[1]).split('>')[1].split('<')[0]
    deaths = int(''.join(deaths_str.split(',')))

    recoveries_str = str(cases[2]).split('>')[1].split('<')[0]
    recoveries = int(''.join(recoveries_str.split(',')))

    update_time_selection = count_page_bs4.select('body > div > div > div.col-md-8 > div > div')
    update_time = str(update_time_selection[1]).split('>')[1].split('<')[0]

    prev_data = count_page_bs4.select('script[type=\'text/javascript\']')
    prev_data_tag = prev_data[7]
    previous_data_regex = re.compile(r'data:\s\S+')
    previous_data = previous_data_regex.findall(prev_data_tag.text)[0].split()[1].split('[')[1].split(']')[0].split(',')
    previous_data = [int(x) for x in previous_data]
    yesterdays_infections = int(previous_data[-2])
    #Previous data contains the list of total cases every day starting Feb.
    
    daily_cases_tag = prev_data[8]
    daily_new_cases = previous_data_regex.findall(daily_cases_tag.text)[0].split()[1].split('[')[1].split(']')[0].split(',')
    newcases_today = int(daily_new_cases[-1])
    #Daily_new_cases containes a list of new cases everyday since Feb.

    active_cases_tag = prev_data[9]
    previous_active_cases = previous_data_regex.findall(active_cases_tag.text)[0].split()[1].split('[')[1].split(']')[0].split(',')
    active_cases_today = previous_active_cases[-1]
    #previous_active_cases contains a list of active cases every day since Feb.

    death_and_recovery_rate_tag = prev_data[13]
    previous_rates = previous_data_regex.findall(death_and_recovery_rate_tag.text)[0].split()[1].split('[')[1].split(']')[0].split(',')
    death_rate_yesterday = previous_rates[-1][0:5] + '%'

    return infections, deaths, recoveries, update_time, yesterdays_infections, newcases_today, active_cases_today, death_rate_yesterday

infections, deaths, recoveries, update_time, yesterdays_infections, newcases_today, active_cases_today, death_rate_yesterday = get_data()

def prepare_email():

    recipients = ['hrushikeshvaidya2002@gmail.com']

    #This is the body of the email. Use HTML& inline CSS to style.
    message_body = f"""

    """

    for a in recipients:
	    #Setting up the email content
	    message = MIMEMultipart('Alternative')
	    message['Subject'] = f'({infections}, {deaths}, {recoveries})'
	    message['To'] = a
	    message['From'] = 'COVID-19 Update'
	    
	    custom_body = MIMEText(message_body, 'HTML')
	    message.attach(custom_body)
	    
	    
	    #Authenticating with the server
	    address = 'hrushikeshspython@gmail.com'
	    password = 'ewidbsnfhbshtpox'
	    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
	    s.ehlo()
	    s.starttls()
	    s.login(address, password)

	    #Send the email!
	    s.send_message(message)
	    print(f'Email sent to {a}')

	    s.quit()
