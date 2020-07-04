date_primitive = []
time_primitive = ''
time_ist = ''
growthrate = []
newcases = []

def initialize():
    #-------------------------------------------------------------------------------------------------------------
    #First website, gets the cases in India
    #-------------------------------------------------------------------------------------------------------------
    import Base_data
    import re, requests, bs4

    global date_primitive, time_primitive, time_ist, growthrate, newcases

    request = requests.get('https://www.worldometers.info/coronavirus/country/india/')
    request.raise_for_status()

    html = request.text
    soup = bs4.BeautifulSoup(html, features='lxml')
    selection_string = 'body div div div div div span'
    date_select = 'body div div div div[style]'

    #Matches gets the 3 numbers we want - Infections, deaths, and recoveries.
    matches = soup.select(selection_string)

    #Matchdate gets the date when these numbers were updated.
    matchdate = soup.select(date_select)

    #I used a regex to get the actual numbers from their HTML tags
    matchregex = re.compile(r'[0123456789,]+')

    #Initialize the variables which will store our data.
    #data = []
    newinfectnum1 = matchregex.findall(str(matches[0]))[0]
    newinfectnum = newinfectnum1.split(',')[0]+newinfectnum1.split(',')[1]
    newdeaths = matchregex.findall(str(matches[1]))[0]
    newrecoveries = matchregex.findall(str(matches[2]))[0]


    #Gets the date in string form, convert this to a single number to compare with each other.
    date_primitive = matchdate[0].contents[0].split()[2:5]
    date_primitive[1] = date_primitive[1][0:-1]
    date_primitive[2] = date_primitive[2][0:-1]
    time_primitive = matchdate[0].contents[0].split()[5]
    calendar = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
    rev_calendar = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August',9:'September', 10:'October', 11:'November', 12:'December'}

    #convert the primitive date and time to a useful format. I know this try/except block is redundant. Whatever.
    try:
        date = calendar[date_primitive[0]]*100 + int(date_primitive[1]) + int(date_primitive[2])
        time = int(time_primitive.split(':')[0])*100 + int(time_primitive.split(':')[1])
        time_ist = ''
        if int(time_primitive.split(':')[1]) >= 30:
            tempmin = (int(time_primitive.split(':')[1]) + 30)%60
            temphours = int(time_primitive.split(':')[0]) + 6
            if temphours>24:
                temphours -= 24
            time_ist = str(temphours) + ':' + str(tempmin)
        else:
            tempmin = (int(time_primitive.split(':')[1]) + 30)
            temphours = int(time_primitive.split(':')[0]) + 5
            if temphours>24:
                temphours -= 24
            time_ist = str(temphours) + ':' + str(tempmin)
        
    except:
        print('Check the try/except block. Primitive_date and time are not in the correct format.')

    Base_data.infections.append(int(newinfectnum))
    Base_data.deaths.append(int(newdeaths))
    Base_data.recoveries.append(int(newrecoveries))
    Base_data.dates.append(date - 2020)
    Base_data.times.append(time)

    

    #--------------------------------------------------------------------------------------------------------------------
    #WHO Situation report
    #--------------------------------------------------------------------------------------------------------------------

    whorequest = requests.get('https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports')
    whorequest.raise_for_status()

    whohtml = whorequest.text
    whosoup = bs4.BeautifulSoup(whohtml, features='lxml')

    situation_report = 'a[target="_blank"]'

    reports = whosoup.select(situation_report)
    #Check if link has the right contents
    link = 'https://who.int' + reports[5].attrs['href']
    linkdate = str(link[73:75]) + ' ' + rev_calendar[int(link[71:73])] + ' 2020'

    Base_data.wholink.append(link)
    Base_data.whodate.append(linkdate)

    #--------------------------------------------------------------------------------------------------------------------
    #Worldwide Case count
    #--------------------------------------------------------------------------------------------------------------------

    world = requests.get('https://www.worldometers.info/coronavirus/')
    world.raise_for_status()

    worldhtml = world.text
    worldsoup = bs4.BeautifulSoup(worldhtml, features='lxml')

    worldcount = 'body div div div div div div > span'
    total = worldsoup.select(worldcount)

    totalregex = re.compile(r'[0123456789,]+')

    totalcases = totalregex.findall(str(total[0]))[0]
    totaldeaths = totalregex.findall(str(total[1]))[0]
    totalrecoveries = totalregex.findall(str(total[2]))[0]

    Base_data.worldcases.append(totalcases)
    Base_data.worlddeaths.append(totaldeaths)
    Base_data.worldrecoveries.append(totalrecoveries)
    Base_data.growthrates.append(growthrate[-1])
    Base_data.newcases.append(newcases[-1])
    
    Base_data.store()

    print('\nWritten data to file \'virus_data.txt\' in cwd.\n')


if __name__ == '__main__':
    initialize()