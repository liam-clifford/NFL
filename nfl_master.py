
import urllib2
import requests
from bs4 import BeautifulSoup
import string 
import csv
import urllib
import decimal
import re
import numpy as np
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from collections import OrderedDict
from itertools import izip, repeat



date_today = datetime.date.today()
year = date_today.year

GAME_DATA_week_num = range(1,15) # weeks in season for GAME LOG DATA (there are 21 weeks up to the super bowl)
DVP_week_num = [13] # configure to get a single week's data for defense v position



###################################################################################################################################################
#	NFL DEFENSE V POSITION


url_list = [] # going to house all url's
url_list_ext = [] # includes urls of "next" pages

pos_string = ["QB","WR","RB","TE","K","DST"]

for i in pos_string:
	for item in DVP_week_num:
		url = "https://www.cbssports.com/fantasy/football/stats/posvsdef/" + "{}".format(i) + "/all/" + "{}".format(item) + "/standard"
		url_list.append(url)

file = open("NFL_defensive_stats.csv", "w") # create csv
writer = csv.writer(file)

for link in url_list:
	page = urllib2.urlopen(link).read()
	soup = BeautifulSoup(page, "html.parser")
	for tr in soup.find_all('tr')[3:]: # skip over first 3 header rows
		try:
			tds = tr.find_all('td')
			if len(str(tds[0])) == 35:
				continue
			else:
				if link.find("QB") >= 58:
					print tds[0].text, tds[1].text, tds[2].text, tds[3].text, tds[4].text, tds[5].text, tds[6].text, tds[7].text, tds[8].text, tds[9].text, tds[10].text, tds[11].text, tds[12].text, tds[13].text				
					writer.writerow(["{}".format(DVP_week_num)[1:len("{}".format(DVP_week_num))-1],tds[0].text, link[58:60],"vs.", re.sub("'",'',str(tds[1]).split('<td align="left" width="25%"><a href="#" onclick="toggleDetailedStats( this, this.parentNode, ')[1].split(' );')[0]), tds[2].text, tds[3].text, tds[4].text, tds[5].text, tds[6].text, tds[7].text, tds[8].text, tds[9].text, tds[10].text, tds[11].text, tds[12].text, tds[13].text])
				else:
					if link.find("RB") >= 58 or link.find("WR") >= 58 or link.find("TE") >= 58:
						print tds[0].text, tds[1].text, tds[2].text, tds[3].text, tds[4].text, tds[5].text, tds[6].text, tds[7].text, tds[8].text, tds[9].text, tds[10].text, tds[11].text, tds[12].text					
						writer.writerow(["{}".format(DVP_week_num)[1:len("{}".format(DVP_week_num))-1],tds[0].text, link[58:60],"vs.", re.sub("'",'',str(tds[1]).split('<td align="left" width="25%"><a href="#" onclick="toggleDetailedStats( this, this.parentNode, ')[1].split(' );')[0]), tds[2].text, tds[3].text, tds[4].text, tds[5].text, tds[6].text, tds[7].text, tds[8].text, tds[9].text, tds[10].text, tds[11].text, tds[12].text])
					else:
						continue 
		except:
			continue

	for tr in soup.find_all('tr')[2:]: # skip over first 2 header rows
		try:
			tds = tr.find_all('td')
			if len(str(tds[0])) == 35:
				continue
			else:
				if link.find("DST") >= 58:
					print tds[0].text, tds[1].text, tds[2].text, tds[3].text, tds[4].text, tds[5].text, tds[6].text, tds[7].text, tds[8].text, tds[9].text, tds[10].text, tds[11].text, tds[12].text, tds[13].text					
					writer.writerow(["{}".format(DVP_week_num)[1:len("{}".format(DVP_week_num))-1],tds[0].text, link[58:61],"vs.", re.sub("'",'',str(tds[1]).split('<td align="left" width="25%"><a href="#" onclick="toggleDetailedStats( this, this.parentNode, ')[1].split(' );')[0]), tds[2].text, tds[3].text, tds[4].text, tds[5].text, tds[6].text, tds[7].text, tds[8].text, tds[9].text, tds[10].text, tds[11].text, tds[12].text, tds[13].text])
				else:
					if link.find("K") >= 58:
						print tds[0].text, tds[1].text, tds[2].text, tds[3].text, tds[4].text, tds[5].text, tds[6].text, tds[7].text, tds[8].text, tds[9].text					
						writer.writerow(["{}".format(DVP_week_num)[1:len("{}".format(DVP_week_num))-1],tds[0].text, link[58:59],"vs.", re.sub("'",'',str(tds[1]).split('<td align="left" width="25%"><a href="#" onclick="toggleDetailedStats( this, this.parentNode, ')[1].split(' );')[0]), tds[2].text, tds[3].text, tds[4].text, tds[5].text, tds[6].text, tds[7].text, tds[8].text, tds[9].text])
					
		except:
			continue
file.close()

###################################################################################################################################################
#	NFL GAME DATA

url_list = [] # going to house all url's
url_list_ext = [] # includes urls of "next" pages

pos_string = ["pass_att&c1comp=gt&c1val=1&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&order_by=pass_rating&from_link=1",
"rec&c1comp=gt&c1val=1&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&order_by=rec_yds&from_link=1",
"rush_att&c1comp=gt&c1val=1&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&order_by=rush_yds&from_link=1"]

page_extension = ["&offset=100","&offset=200"]

for i in pos_string:
	for item in GAME_DATA_week_num:
		url = "https://www.pro-football-reference.com/play-index/pgl_finder.cgi?request=1&match=game&year_min=" + "{}".format(year) + "&year_max=" + "{}".format(year) + "&season_start=1&season_end=-1&age_min=0&age_max=99&game_type=A&league_id=&team_id=&opp_id=&game_num_min=0&game_num_max=99&week_num_min=" + "{}".format(item) + "&week_num_max=" + "{}".format(item) + "&game_day_of_week=&game_location=&game_result=&handedness=&is_active=&is_hof=&c1stat=" + "{}".format(i)
		url_list.append(url)

for string in page_extension:
	for link in url_list:
		if link.find("pass_att") >= 349 and link.find("pass_att") <= 351: # no extension needed for passing stats
			url_ext = link
		else:
			if len(link) >= 474 and len(link) <= 476:
				url_ext = link + "{}".format(string)
				url_list_ext.append(url_ext)
			else:
				if len(link) >= 480 and len(link) <= 482 and string == "&offset=200":
					url = link
				else:
					url_ext = link + "{}".format(string)	# there's not usually >200 rushers in 1 week
					url_list_ext.append(url_ext)

url_list.extend(url_list_ext) # conjoins two list of URLs

file = open("NFL_data.csv", "w") # create csv
writer = csv.writer(file)


for link in url_list:
	page = urllib2.urlopen(link).read()
	soup = BeautifulSoup(page, "html.parser")
	for tr in soup.find_all('tr')[2:]: # skip over first 2 header rows
		try:
			tds = tr.find_all('td')
			if link.find("pass_att") >= 349 and link.find("pass_att") <= 351: # passing stats   			
				writer.writerow([tds[0].text, "Passing", tds[2].text, tds[3].text, tds[5].text, tds[6].text, tds[7].text, tds[8].text, tds[9].text, tds[10].text, tds[11].text, tds[12].text, tds[13].text, tds[14].text, tds[15].text, tds[16].text, tds[17].text, tds[18].text, tds[19].text, tds[20].text, tds[21].text, tds[22].text,year])

			else:
				if (len(link) >= 474 and len(link) <= 476) or (len(link) >= 485 and len(link) <= 487): # receiving stats / if and or statment
					writer.writerow([tds[0].text, "Receiving", tds[2].text, tds[3].text, tds[5].text, tds[6].text, tds[7].text, tds[8].text, tds[9].text, tds[10].text, tds[11].text, tds[12].text, tds[13].text, tds[14].text, tds[15].text, tds[16].text, tds[17].text, tds[18].text,year])
				
				else:	
					if (len(link) >= 480 and len(link) <= 482) or (len(link) >= 491 and len(link) <= 493): # rushing stats / if and or statment
						writer.writerow([tds[0].text, "Rushing", tds[2].text, tds[3].text, tds[5].text, tds[6].text, tds[7].text, tds[8].text, tds[9].text, tds[10].text, tds[11].text, tds[12].text, tds[13].text, tds[14].text, tds[15].text,year])

					else:
						continue
		except:
			continue

file.close()

###################################################################################################################################################
#	NFL POSITION DATA


url_list = []
pos_data = []

pos_string = ["passing","rushing","receiving","kicking"]

for i in pos_string:
	url = "https://www.pro-football-reference.com/years/" + "{}".format(year) + "/" + "{}".format(i) + ".htm"
	url_list.append(url)

for i in url_list:
	p = requests.get(i)
	soup = BeautifulSoup(p.content, "html.parser")
	data = soup.find_all("tr")
	for item in data:
		try:
			tds = item.find_all('td')
			team = tds[1].text
			url_string = 'https://www.pro-football-reference.com'
			player_ID = re.sub('="',"",str(item).split("href")[1].split("</a>")[0]).split('">')[0]
			url_player_ID = url_string + player_ID # creates url for next loop 	
			name = re.sub('">',"",str(item).split(".htm")[1].split("</a>")[0]) # data for next loop 
			name = re.sub("'",'',name)
			if name == '':
				continue
			else:

				p = requests.get(url_player_ID)
				soup = BeautifulSoup(p.content, "html.parser")
				data = soup.find_all("p")

				for x in data:
					try:
						pos = str(x).split("<strong>Position</strong>: ")[1][0:2]
						pos = pos.replace('\n','') # replace all extra line spaces in string
						if pos == "TE" or pos == "QB" or pos == "WR" or pos == "RB" or pos == "FB" or pos[:1] == "K":
							player_data = name, pos, team
							pos_data.append(player_data)
						else:
							continue
					except:
						continue
		except:
			continue

unique_list = list(OrderedDict(izip(pos_data, repeat(None)))) # create list of non duplicate list of players

file = open("NFL_player_positions.csv", "w") # create csv
writer = csv.writer(file)

for i in unique_list:
	name = re.sub("'",'',str(i).split(',')[0])[1:]
	pos = re.sub("'",'',str(i).split(',')[1])[1:]
	team = re.sub("'",'',str(i).split(',')[2])[1:][1:]
	team = team[:len(team)-1]
	writer.writerow([name, pos, team])
file.close()

###################################################################################################################################################
#	NFL SL DEFENSE DATA

url = "https://www.pro-football-reference.com/years/" + "{}".format(year) + "/opp.htm"

file = open("NFL_sl_defense.csv", "w") # create csv
writer = csv.writer(file)

page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page, "html.parser")
for tr in soup.find_all('tr'): # skip over first 3 header rows
	try:
		tds = tr.find_all('td')
		writer.writerow([tds[0].text, tds[1].text, tds[2].text, tds[3].text, tds[4].text, tds[5].text, tds[6].text, tds[7].text, tds[8].text, tds[9].text, tds[10].text, tds[11].text, tds[12].text, tds[13].text, tds[14].text, tds[15].text, tds[16].text, tds[17].text, tds[18].text, tds[19].text, tds[20].text, tds[21].text, tds[22].text, tds[23].text, tds[24].text, tds[25].text, tds[26].text])
	except:
		continue
file.close()

###################################################################################################################################################







