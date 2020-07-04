"""
The basic script which initializes the variables we want to store.
Opens a file called virus_data and stores the variables in it.
"""
#The last elements of these lists are stored as lines in the file (separated by a space).
infections = []
deaths = []
recoveries = []
dates = []
times = []
wholink = []
whodate = []
worldcases = []
worlddeaths = []
worldrecoveries = []
growthrates = []
newcases = []


emaillist = []

def store():
	"""
	Stores the values of infections, deaths, recoveries, and dates in the file virus_data.txt in the cwd.
	"""

	data = open('virus_data.txt', mode='a')
	data.write(str(infections[-1]) + ' ' + str(deaths[-1]) + ' ' + str(recoveries[-1]) + ' ' + str(dates[-1]) + ' ' + str(times[-1]) + ' ' + wholink[-1] + ' ' +whodate[-1] + ' ' + str(worldcases[-1]) + ' ' + str(worlddeaths[-1]) + ' ' + str(worldrecoveries[-1]) + ' ' + str(growthrates[-1]) + ' ' + newcases[-1] + '\n')
	data.close()