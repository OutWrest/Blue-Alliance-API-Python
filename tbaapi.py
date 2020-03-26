import requests as re
import json

class blueAPI:
	apiKey = ""
	eventKey = ""
	blueAPIWeb = ""
	eventTeams = ""
	currentYear = ""

	def __init__(self, apiKey, eventKey):
		self.apiKey = apiKey
		self.eventKey = eventKey
		self.blueAPIWeb = "https://www.thebluealliance.com/api/v3"
		#self.eventTeams = (re.get('{}/event/{}/teams'.format(self.blueAPIWeb, self.eventKey), headers={'X-TBA-Auth-Key':self.apiKey})).json()
		self.eventTeams = self.getRequest('/event/{}/teams'.format(self.eventKey))
		self.currentYear = self.getRequest('/status')['current_season']

	def getRequest(self, queryURL): #prob dont use since you'd have to put eventID again.
		#can also be used outside of the functions below by using the eventkey "EVENTKEY"
		#Returns the Json list of any requests. If request requires the previous eventKey, please put EVENTKEY instead of the event key again.
		if('EVENTKEY' in queryURL):
			queryURL = queryURL.replace("EVENTKEY", self.eventKey)
		api = "https://www.thebluealliance.com/api/v3"
		resp = re.get(api+queryURL, headers={'X-TBA-Auth-Key':self.apiKey}).json()
		for key in resp:
			if('Error' in key):
				print('The query \"{}\"" raised an error. Please double check info:\n Error returned: {}\n API Key: {}\n Current Year: {}'.format(api+queryURL, resp['Error'], self.apiKey, self.currentYear))
				exit()
		return resp

	def getTeams(self, city=False, name=False, nickname=True, school_name=False, team_number=True):
		#Returns the teams that are playing, can customize the return.
		teams = []
		for team in self.eventTeams:
			current_team = {}
			if(team_number):
				current_team['team_number'] = team['team_number']
			if(nickname):
				current_team['nickname'] = team['nickname']
			if(school_name):
				current_team['school_name'] = team['school_name']
			if(city):
				current_team['city'] = team['city']
			if(name):
				current_team['name'] = team['name']
			teams.append(current_team)

		return teams

	def getTeamInfo(self, team_number, region_lock=True):
		#Given a teams number, it will return information about that team.
		#region_lock, if false, can return info outside that specified regional.
		if(region_lock):
			return self.getRequest('/team/{}/events/{}/statuses'.format('frc'+str(team_number), self.currentYear))[self.eventKey]
		else:
			return self.getRequest('/team/{}/events/{}/statuses'.format('frc'+str(team_number), self.currentYear))

	def getScores(self, oprs=True, dprs=True, ccwms=True, team_number=0):
		#Returns the scores (OPRS DPRS CCWMS) of the given regional. 
		#You can specify if you specifically want a team's score or indiviidal scores or both
		scores = self.getRequest('/event/EVENTKEY/oprs')
		scores_wanted = {}
		if(team_number == 0):
			if(oprs):
				scores_wanted['oprs'] = scores['oprs']
			if(dprs):
				scores_wanted['dprs'] = scores['dprs']
			if(ccwms):
				scores_wanted['ccwms'] = scores['ccwms']
		else:
			try:
				if(oprs):
					scores_wanted['oprs'] = scores['oprs']['frc'+str(team_number)]
				if(dprs):
					scores_wanted['dprs'] = scores['dprs']['frc'+str(team_number)]
				if(ccwms):
					scores_wanted['ccwms'] = scores['ccwms']['frc'+str(team_number)]
			except KeyError:
				scores_wanted['oprs'] = 0
				scores_wanted['dprs'] = 0
				scores_wanted['ccwms'] = -100
		return scores_wanted

	def getPredicitons(self):
		#Returns TBA's predictions of the given regional.
		return self.getRequest('/event/EVENTKEY/predictions')

	def getRankings(self):
		#Returns the rankings of the given regional
		return self.getRequest('/event/EVENTKEY/rankings')

	def getMatches(self, simple=True):
		#Returns matches on the given regional
		if(simple):
			return self.getRequest('/event/EVENTKEY/matches/simple')
		else:
			return self.getRequest('/event/EVENTKEY/matches')

	def getMatchKeys(self):
		#returns match keys of the given regional
		return self.getRequest('/event/EVENTKEY/matches/keys')

	def getMatchInfo(self, matchKey, simple=True):
		#Returns match info given a matchkey. Not region specific
		#simple, if true returns the simiplifed results. Otherwise it will return all the info TBA has.
		if(simple):
			return self.getRequest('/match/{}/simple'.format(matchKey))
		else:
			return self.getRequest('/match/{}'.format(matchKey))






