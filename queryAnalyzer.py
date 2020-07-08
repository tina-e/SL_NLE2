#search for players##################################################################################

def getAllPlayerNames():
    import sqlite3
    sqlite_file = 'database.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('SELECT player_name FROM player')
    playerNames = c.fetchall()
    conn.close()
    return playerNames

#needed to handle "thomas mueller" and "mueller thomas"
def getReverseName(name):
    x = name.find(" ")
    if x > -1:
        return name[x+1:] + " "+ name[:x]
    return "XXX"

#returns the database id of the player by name
def getPlayerIDByName(name):
    import sqlite3
    sqlite_file = 'database.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    queryText = 'SELECT id FROM player WHERE player_name = "'+ str(name)+'"'
    c.execute(queryText)
    playerID = c.fetchall()
    conn.close()
    return playerID[0][0]

#Returns list with names of found players
def getPlayersInQuery(query):
    playerList = list()
    for name in getAllPlayerNames():
        if  name[0].find(" ") > -1 and name[0] in query or getReverseName(name[0]) in query:
            playerList.append(getPlayerIDByName(name[0]))
    return playerList


#search for leagues##################################################################################

def getAllCountries():
    import sqlite3
    sqlite_file = 'database.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('SELECT name FROM country')
    countryNames = c.fetchall()
    conn.close()
    return countryNames

def getRegExForCountries():
    regExCountryList = ['belgi(an|sch|en)', 'engl(and|(is(ch|h)))', 'fran(ce|zoesisch|kreich)', '(deutsch|german)', 'ital(ienisch|ian|ien|y)', '(holla(endisch|nd)|niederla(endisch|nd)|dutch|netherland)', 'pol(nisch|ish|en|and)', 'portug(iesisch|uese|al)', '(scot(tish|land)|schott(lae?nd)?isch)', 'spa(nisch|in|nien)', '(schweiz((er(isch)?)?)|swiss|switzerland)']
    return regExCountryList

#return the database id of the country by name
def getCountryIDByName(name):
    import sqlite3
    sqlite_file = 'database.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    queryText = 'SELECT id FROM country WHERE name = "'+ name+'"'
    c.execute(queryText)
    countryID = c.fetchall()
    conn.close()
    return countryID[0][0]

#searches country information in the query
def getCountryListInQuery(query):
    import re
    foundCountryList = list()
    for regEx in getRegExForCountries():
        #if re.search(regEx + " (League|Liga)", query):
        if re.search(regEx, query, re.IGNORECASE):
            foundCountryList.append(getAllCountries()[getRegExForCountries().index(regEx)])
    return foundCountryList


#search for leagues##################################################################################

def getAllLeagues():
    import sqlite3
    sqlite_file = 'database.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('SELECT name FROM league')
    leagueNames = c.fetchall()
    conn.close()
    return leagueNames

#needed to handle input like e.g. "1. Bundesliga" instead of "Germany 1. Bundesliga"
def getLeagueNameParts(name):
    wordsGivenLeague = list()
    #do not ignore country-info for england and scotland because their league has the same name
    if "England" not in name and "Scotland" not in name:
        wordsGivenLeague= name.split()
        wordsGivenLeague.pop(0)
    #merge list elements with single characters
    for element in wordsGivenLeague:
        if len(element) < 3:
            index = wordsGivenLeague.index(element)
            if index < 1:
                wordsGivenLeague[0] = element + wordsGivenLeague[1]
            else:
                wordsGivenLeague[1] = wordsGivenLeague[1] + element
    #remove words used in more league-names
    ambiguiteWords = ['League', 'Liga', 'LIGA']
    for word in ambiguiteWords:
        if word in wordsGivenLeague:
            wordsGivenLeague.remove(word)
    return wordsGivenLeague

#returns the database id of the league by name
def getLeagueIDByName(name):
    import sqlite3
    sqlite_file = 'database.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    queryText = 'SELECT id FROM league WHERE name = "'+ name+'"'
    c.execute(queryText)
    leagueID = c.fetchall()
    conn.close()
    return leagueID[0][0]

#returns a list with IDs of found leagues
def getLeaguesInQuery(query):
    leagueList = list()
    for name in getAllLeagues():
        if name[0] in query:
            leagueList.append(getLeagueIDByName(name[0]))
        else:
            for part in getLeagueNameParts(name[0]):
                if part in query:
                    leagueList.append(getLeagueIDByName(name[0]))
    #checks if there is country information for the league in the query (e.g. "deutsche Liga")             
    for foundCountry in getCountryListInQuery(query):
        leagueList.append(getCountryIDByName(foundCountry[0]))
    return leagueList


#search for teams##################################################################################

def getAllTeamNames():
    import sqlite3
    sqlite_file = 'database.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('SELECT team_long_name FROM team')
    teamNames = c.fetchall()
    for i in range(0, len(teamNames)):
        teamNames[i] = teamNames[i][0]
    conn.close()
    #remove dublicate entries
    teamNames = list(set(teamNames))
    return teamNames

def getAllTeamAbbrevs():
    import sqlite3
    sqlite_file = 'database.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('SELECT team_short_name FROM team')
    teamAbbrevs = c.fetchall()
    conn.close()
    return teamAbbrevs

#split the team names to find e.g. "Bayern" instead of "FC Bayern Munich"
def splitTeamNames():
    #first split all team names
    teamNamesSplitted = list()
    teamNames = getAllTeamNames()
    for team in teamNames:
        teamNamesSplitted.append(team.split())
    #remove abbrevs and numbers
    for i in range(len(teamNamesSplitted)):
        #print(teamNamesSplitted[i])
        for part in teamNamesSplitted[i]:
            if len(part) < 4:
                teamNamesSplitted[i].remove(part)
    #remove dublicates
    for i in range(len(teamNamesSplitted)):
        for part in teamNamesSplitted[i]:
            if isDublicate(teamNamesSplitted, part) == True:
                mergeElement(teamNamesSplitted, part)
    return teamNamesSplitted   

#check if there are teams that include the same names (e.g. "Manchester United" and "Manchester City")
def isDublicate(teamList, checkElement):
    count = 0
    for team in teamList:
        for element in team:
            if element == checkElement:
                count += 1
    if count < 2:
        return False
    else:
        return True

#merge e.g. "[Manchester, United]" to "[Manchester United]" to prevent ambiguity (with "Manchester City")
def mergeElement(completeList, dublicateElement):
    for i in range(len(completeList)):
        for j in range(len(completeList[i])):
            if completeList[i][j] == dublicateElement:
                if j+1 == len(completeList[i]):
                    completeList[i][j] = completeList[i][j-1] + " " + dublicateElement
                else:
                    completeList[i][j] = dublicateElement + " " + completeList[i][j+1]  

def getTeamIDByName(name):
    import sqlite3
    sqlite_file = 'database.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    queryText = 'SELECT id FROM team WHERE team_long_name = "'+ name+'"'
    c.execute(queryText)
    teamID = c.fetchall()
    conn.close()
    return teamID[0][0]

def getTeamIDByAbbrev(teamAbbrev):
    import sqlite3
    sqlite_file = 'database.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    queryText = 'SELECT id FROM team WHERE team_short_name = "'+ teamAbbrev+'"'
    c.execute(queryText)
    teamID = c.fetchall()
    conn.close()
    return teamID[0][0]

#returns a list with IDs of found teams
def getTeams(query):
    import re
    teamList = list()
    #is the input a valid abbreviation for a team
    allTeamAbbrevs = getAllTeamAbbrevs()
    for abbrev in allTeamAbbrevs:
        if abbrev[0] in query:
            if isDublicate(allTeamAbbrevs, abbrev[0]) == False:
                teamList.append(getTeamIDByAbbrev(abbrev[0]))
            #else: Ausgabe: Definieren genauer, es gibt mehrere Teams mit dieser Abkürzung
    #is the input a valid name for a team
    allTeamNames = getAllTeamNames()
    for name in allTeamNames:
        if name in query:
            teamList.append(getTeamIDByName(name))
    #is the input a valid tranformed name for a team
    splittedTeamNames = splitTeamNames()
    for i in range(len(splittedTeamNames)):
        for part in splittedTeamNames[i]:
            #make sure the part is detached
            searchString = " "+part+"( |\W)"
            if re.search(searchString, query):
                teamList.append(getTeamIDByName(allTeamNames[i]))
    teamList = list(set(teamList))
    return teamList


#search for seasons##################################################################################

def getAllSeasons():
    import sqlite3
    sqlite_file = 'database.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('SELECT season FROM match')
    seasons = c.fetchall()
    allSeasons = list()
    for i in range(0, len(seasons)):
        if seasons[i][0] not in allSeasons:
            allSeasons.append(seasons[i][0]) 
    conn.close()
    return allSeasons

def getAllSeasonAbbrevs():
    abbrevList = list()
    allSeasons = getAllSeasons()
    for season in allSeasons:
        season = season[1:]
        season = season[1:]
        season = season[0:4: ] + season[5: : ]
        season = season[0:3: ] + season[4: : ]
        abbrevList.append(season)
    return abbrevList

def getSeasonByAbbrev(abbrev):
    allSeasons = getAllSeasons()
    allAbbrevs = getAllSeasonAbbrevs()
    for element in allAbbrevs:
        if abbrev == element:
            index = allAbbrevs.index(element)
            return allSeasons[index]

def getSeasons(query):
    seasonList = list()
    allSeasons = getAllSeasons()
    for season in allSeasons:
        if season in query:
            seasonList.append(season)
    allAbbrevs = getAllSeasonAbbrevs()
    for abbrev in allAbbrevs:
        if abbrev in query:
            seasonList.append(getSeasonByAbbrev(abbrev))
    return seasonList


#search for stages##################################################################################

def getStages(query):
    import re
    stageList = list()
    searchString = "\d+\.?\s?Spieltag"
    matchObject = re.findall(searchString, query)
    for match in matchObject:
        stageString = ""
        for element in match:
            if element != "." and element != "S" and element != " ":
                stageString = stageString + element
            else: break
        stageList.append(stageString)
    return stageList