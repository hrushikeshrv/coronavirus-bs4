import get_data
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#get_data.initialize()

case = []
data = open('virus_data.txt')
for line in data:
	case.append(line)

data.close()

#Remove repetitions if you wanna plot the data.
def remove_repeats():
	a = 0
	while a < len(case)-1:
		if case[a].split()[3] == case[a+1].split()[3]:
			case.pop(a)

		a += 1

def prepare_email():
	newinfections = case[-1].split()[0]
	newdeaths = case[-1].split()[1]
	newrecoveries = case[-1].split()[2]
	updatedate = case[-1].split()[3]
	updatetime = case[-1].split()[4]
	reportlink = case[-1].split()[5]
	reportdate = case[-1].split()[6:9]
	previnfections = case[-2].split()[0]
	prevdeaths = case[-2].split()[1]
	prevrecoveries = case[-2].split()[2]
	deltacasesindia = int(newinfections) - int(previnfections)
	deltadeathsindia = int(newdeaths) - int(prevdeaths)
	deltarecoveriesindia = int(newrecoveries) - int(prevrecoveries)
	growthrate = int(newinfections)/int(previnfections)
	r0 = '2.0 to 2.5'
	worldinfections = case[-1].split()[9]
	worlddeaths = case[-1].split()[10]
	worldrecoveries = case[-1].split()[11]
	get_data.growthrate.append(str(round(growthrate, 4)))
	get_data.newcases.append(str(deltacasesindia))

	get_data.initialize()


def sendemail():	
	#Redefine all the variables cuz we initialize() after we define them.
	case.clear()

	data1 = open('virus_data.txt')
	for line in data1:
		case.append(line)

	data1.close()

	newinfections = case[-1].split()[0]
	newdeaths = case[-1].split()[1]
	newrecoveries = case[-1].split()[2]
	updatedate = case[-1].split()[3]
	updatetime = case[-1].split()[4]
	reportlink = case[-1].split()[5]
	reportdate = case[-1].split()[6:9]
	previnfections = case[-2].split()[0]
	prevdeaths = case[-2].split()[1]
	prevrecoveries = case[-2].split()[2]
	deltacasesindia = int(newinfections) - int(previnfections)
	deltadeathsindia = int(newdeaths) - int(prevdeaths)
	deltarecoveriesindia = int(newrecoveries) - int(prevrecoveries)
	growthrate = int(newinfections)/int(previnfections)
	r0 = '2.0 to 2.5'
	worldinfections = case[-1].split()[9]
	worlddeaths = case[-1].split()[10]
	worldrecoveries = case[-1].split()[11]
	
	deltagrowthrate = float(case[-1].split()[12]) - float(case[-2].split()[12])
	deltadeltacases = int(case[-1].split()[0]) - 2*int(case[-2].split()[0]) + int(case[-3].split()[0])

	msgstring = '<HTML><BODY><P>' + '_'*35 + f'</P><P>Throughout the world, <STRONG>{worldinfections}</STRONG> people have been infected.<br><STRONG>{worlddeaths}</STRONG> people have died.<br><STRONG>{worldrecoveries}</STRONG> people have succesfully recovered from the virus.</P><P><STRONG>{newinfections}</STRONG> people in India have been infected with COVID-19.<br><STRONG>{newdeaths}</STRONG> people have died, while <STRONG>{newrecoveries}</STRONG> people have recovered from the infection.</P><P>There are <STRONG>{deltacasesindia}</STRONG> new cases in India today.<br>There were <STRONG>{deltadeathsindia}</STRONG> deaths in India yesterday, and <STRONG>{deltarecoveriesindia}</STRONG> people recovered.</P><P>According to these numbers, the growth rate of the virus is {round(growthrate,4)}. One infected person infects, on average, {round(growthrate,4)} healthy people. Without any control measures, the growth rate would have been between {r0}</P><P>The change in the growth rate since yesterday has been <STRONG>{round(deltagrowthrate, 4)}</STRONG>. The change in the number of new cases (i.e. (new cases yesterday) - (new cases today))is <br>deltanewcases = <STRONG>{deltadeltacases}</STRONG>. <br>A negative value of deltanewcases over a sustained period of time means that the exponential growth of the virus has started to slow down, and that we will stabilize at around twice the number of infections that we had when deltanewcases first became negative.</P><P>The mortality rate according to today\'s numbers is {round(int(newdeaths)/int(newinfections)*100,3)}%</P><P><FONT face="monospace" color="rgb(128,128,128)">Last updated on {get_data.date_primitive[0]} {get_data.date_primitive[1]} {get_data.date_primitive[2]} \nat GMT {get_data.time_primitive} (IST {get_data.time_ist})</FONT></P><P><br>\n\nRead the detailed report by the World Health Organization here (last updated on {reportdate[0]} {reportdate[1]} {reportdate[2]})- \n</P><P><A href="{reportlink}">who.int/default/coronavirus/situation_update</A>\n</P>' + '_'*35 + f'<br><P FONT="Times New Roman">Automated email delivery by hrushikeshvaidya2002@gmail.com<br>Data from <A href="https://worldometers.info/coronavirus/country/india/">worldometers.info/coronavirus/india</A> and <A href="{reportlink}">WHO Situation Updates</A></P></BODY></HTML>'

	htmlmessage = f"""
		<HTML>
<HEAD>
	<TITLE>COVID-19 Update</TITLE>
</HEAD>
<BODY>
	<H1 align="center">--- Global Infections ---
	</H1>
	<P align="center"><STRONG>
		Total infections 	= 	{worldinfections}<br>
		Deaths 				=	{worlddeaths}<br>
		Recoveries 			=	{worldrecoveries}<br>
	</STRONG></P>
	<P align="center">
		_____________________________________________________________
	</P>
	<H1 align="center">--- India ---
	</H1>
	<P align="center"><STRONG>
		Total infections 	= 	{newinfections}<br>
		Deaths 				= 	{newdeaths}<br>
		Recoveries 			= 	{newrecoveries}<br>
	</STRONG></P> 
	<P>
		According to these numbers, the growth rate is {round(growthrate,4)}.<br>
		One infected person infects, on average, {round(growthrate,4)} healthy people. Without any control measures, this growth rate would have been betweeen 2.0 to 2.5.<br><br>

		The change in growth rate since yesterday is {round(deltagrowthrate, 4)}.<br><br>

		There are {deltacasesindia} new cases in India today.<br>
		There were {deltadeathsindia} deaths yesterday.<br>
		The mortality rate according to today's numbers is {round(int(newdeaths)/int(newinfections)*100,3)}%<br><br>

		The change in number of new cases today as compared to yesterday is<br><br>

		New_cases_today - New_cases_yesterday<br><br>

		delta(newcases)		=	 {deltadeltacases}<br><br>

		A negative value of delta(newcases) over a sustained period of time means that the exponential spread of the virus is slowing down.
	</P>

	<P>
		<FONT face="monospace" color="rgb(128,128,128)">
			Last updated on {get_data.date_primitive[0]} {get_data.date_primitive[1]} {get_data.date_primitive[2]} at GMT {get_data.time_primitive} (IST {get_data.time_ist})
		</FONT>
	</P>
	<P>
		Read the detailed report by the World Health Organization here (last updated on {reportdate[0]} {reportdate[1]} {reportdate[2]})<br>
		<A href="{reportlink}">who.int/default/coronavirus/situation_update</A><br>
	</P>

	<P align="center">
		_____________________________________________________________
	</P>
	<P align="center">
		Automated email delivery by hrushikeshvaidya2002@gmail.com<br>
		Data from <A href="https://worldometers.info/coronavirus/country/india/">worldometers.info/coronavirus/india</A> and <A href="{reportlink}">WHO Situation Updates</A>
	</P>
</BODY>
</HTML>


	"""


	newhtmlmessage = f"""

		<!--src for world map image - https://static.vecteezy.com/system/resources/previews/000/142/990/original/vector-world-map.jpg -->

<HTML>
<HEAD>
	<TITLE>COVID-19 Update</TITLE>
</HEAD>
<BODY bgcolor="D9EEEC">
	<H1 align="center">• Global Infections •
	</H1>
	<P align="center"><A href="https://www.worldometers.info/coronavirus/"><img align="top" src="https://static.vecteezy.com/system/resources/previews/000/142/990/original/vector-world-map.jpg" height="40" width="66" vspace="10"></A></P>
	<TABLE align="center" frame="void" border="1" cellpadding="10" width="500">
		
		<tr bgcolor="AEA4A2"><td><FONT face="garamond"><STRONG>Total Infections</STRONG></FONT></td><td align="center">{worldinfections}</td></tr>
		<tr><td><FONT face="garamond"><STRONG>Deaths</STRONG></FONT></td><td align="center">{worlddeaths}</td></tr>
		<tr bgcolor="AEA4A2"><td><FONT face="garamond"><STRONG>Recoveries</STRONG></FONT></td><td align="center">{worldrecoveries}</td></tr>
	
	</TABLE><br><br>
	<hr align="center" width="50%" size="4" noshade="1"><br>
	<H1 align="center">• India •
	</H1>
	<P align="center"><A href="https://www.worldometers.info/coronavirus/country/india/"><img align="top" src="https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Flag_of_India.svg/1200px-Flag_of_India.svg.png" height="40" width="66" vspace="10"></A></P>
	<TABLE align="center" frame="void" border="1" cellpadding="10" width="500">
		
		<tr bgcolor="AEA4A2"><td><FONT face="garamond"><STRONG>Total Infections</STRONG></FONT></td><td align="center">{newinfections}</td></tr>
		<tr><td><FONT face="garamond"><STRONG>Deaths</STRONG></FONT></td><td align="center">{newdeaths}</td></tr>
		<tr bgcolor="AEA4A2"><td><FONT face="garamond"><STRONG>Recoveries</STRONG></FONT></td><td align="center">{newrecoveries}</td></tr>
		<tr><td><FONT face="garamond"><STRONG>New Cases Today</STRONG></FONT></td><td align="center">{deltacasesindia}</td></tr>
	
	</TABLE><br><br> 

	<hr align="center" width="50%" size="4" noshade="1">
	<P align="center"><FONT color="B4B4B4">Click on the flags to see more information and graphs related to the growth of the infection.</FONT></P>
	
	<P><FONT size="3" face="Georgia">
		<UL type="disc">
		<li>According to these numbers, the growth rate of the virus is <STRONG><FONT color="F49F9F">{round(growthrate,4)}</FONT></STRONG>. One infected person infects, on average, <FONT color="F49F9F">{round(growthrate,4)}</FONT> healthy people. Without any control measures, this growth rate would have been betweeen <STRONG><FONT color="FE6868">2.0 to 2.5</FONT></STRONG>.

		Yesterday, the growth rate of the infection was {round(growthrate,4) - round(deltagrowthrate,4)}.</li><br><br>

		<li>There were {deltadeathsindia} deaths yesterday.</li><br><br>

		<li>The change in number of new cases today as compared to yesterday is	[New cases today - New cases yesterday]<br><br>

		<BLOCKQUOTE>‎Δnewcases		=	{deltadeltacases}</BLOCKQUOTE><br></li>

		<li>A negative value of ‎Δnewcases over a sustained period of time means that the exponential spread of the virus is slowing down.</li>
	</UL>
	</FONT></P>
	
	<P>
		<FONT face="monospace" color="rgb(128,128,128)">
			Last updated on  {get_data.date_primitive[0]} {get_data.date_primitive[1]} {get_data.date_primitive[2]} at GMT {get_data.time_primitive} (IST {get_data.time_ist})
		</FONT>
	</P>
	<P align="center"><FONT size="2" face="palatino"><br>
		<STRONG>Read the detailed report by the World Health Organization here </STRONG><br>
		<FONT face="monospace" size="3" color="rgb(128,128,128)">(last updated on {reportdate[0]} {reportdate[1]} {reportdate[2]})</FONT><br>

		<P align="center"><A href="https://www.who.int/"><img src="https://www.who.int/images/default-source/default-album/who-logo-rgb.png" width="200" height="62" vspace="10"></A></P>
		<TABLE align="center" frame="void" border="0" cellpadding="10" width="500"><tr><td align="center" bgcolor="AEA4A2"><A href="{reportlink}">who.int/default/coronavirus/</A></td></tr></TABLE><br>
	</FONT></P>
	
	<hr align="center" width="50%" size="4" noshade="1"><br>
	<P align="center">
		Automated email delivery by hrushikeshvaidya2002@gmail.com<br>
		Data from <A href="https://worldometers.info/coronavirus/country/india/">worldometers.info/coronavirus/india</A> and <A href="{reportlink}">WHO Situation Updates</A>
	</P>
</BODY>
</HTML>

	"""

	body = newhtmlmessage
    
	emaillist = ['hrushikeshvaidya2002@gmail.com','rohit71.vaidya@gmail.com','kshipra.rohit@gmail.com','arya.coolbhagwat38@gmail.com','eeshapendse@gmail.com','varad2110@gmail.com','awellwisher2929@gmail.com']
	#emaillist = ['hrushikeshvaidya2002@gmail.com']

	for a in emaillist:
	    #Setting up the email content
	    message = MIMEMultipart('Alternative')
	    message['Subject'] = f'({newinfections}, {newdeaths}, {newrecoveries})'
	    message['To'] = a
	    message['From'] = 'COVID-19 Update'
	    
	    custom_body = MIMEText(body, 'HTML')
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
	    
	
if __name__ == '__main__':
	remove_repeats()
	prepare_email()
	sendemail()
