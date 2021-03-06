from pyquery import PyQuery as pq
import requests,csv,sys

statsPath = sys.path[0] + "/stats/"

for i in range(1,11):
	r = requests.get("http://games.espn.go.com/flb/playertable/prebuilt/activestats?leagueId=9042&teamId="+str(i)+"&filter=1&scoringPeriodId=83&mode=bydate&view=stats&context=activestats&ajaxPath=playertable/prebuilt/activestats&r=23572953")
	statsTable = pq(r.text)('.playertableFrameInnerShell')
	with open(statsPath+'stats-'+str(i)+'.csv', 'w') as csvfile:
		filewriter = csv.writer(csvfile)
		for row in pq(statsTable)('.tableBody').filter(lambda i:pq(this).attr['bgcolor'] != "#e0e0a8"):
			rowList = []
			for cell in pq(row)('td'):
				rowList.append(pq(cell).text())
			filewriter.writerow(rowList)
