from pyquery import PyQuery as pq
import requests
import csv

baseUrl = "http://games.espn.go.com/flb/boxscorefull"
params = {
	"leagueId" : 9042,
	"seasonId" : 2014,
	"view"     : "scoringperiod",
	"version"  : "full"
}

def getRowData(row):
	d = pq(row) 
	name = d('a').eq(0).text()
	pos = d('td.playerSlot').text()
	pts = d('td.appliedPoints').text()
	return {
		'pos': pos,
		'name': name,
		'pts': pts
	}

for i in range(1,11):
	params['teamId'] = i
	with open('stats/dailystats-'+str(i)+'.csv', 'w') as csvfile:
		filewriter = csv.writer(csvfile)
		for j in range(1,200):
			params['scoringPeriodId'] = j
			r = requests.get(baseUrl, params=params)
			datesRow = pq(r.text)('.games-fullcol .bodyCopy').eq(3)
			date = pq(datesRow)('b').filter(lambda i:i==1).text()
			if(date != ''):
				rowList = [date]

				battersTable = pq(r.text)('#playertable_0')
				for k in range(0,9):
					rowData = getRowData(pq(battersTable)(".pncPlayerRow").eq(k))
					rowList.extend([rowData["name"],rowData["pts"]])

				pitchersTable = pq(r.text)('#playertable_1')
				for k in range(0,8):
					rowData = getRowData(pq(pitchersTable)(".pncPlayerRow").eq(k))
					rowList.extend([rowData["name"],rowData["pts"]])

				filewriter.writerow(rowList)
				if(date == 'Today'):
					break