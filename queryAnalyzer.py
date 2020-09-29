#search for players##################################################################################

def getAllPlayerNames():
    import sqlite3
    sqlite_file = 'database.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('SELECT player_name FROM player')
    playerNames = c.fetchall()
    conn.close()
    #make system case insensitive
    import string
    playerNamesLower = list()
    for name in playerNames:
        name = name[0]
        playerNamesLower.append(name.lower())
    return playerNamesLower

#needed to handle "thomas mueller" and "mueller thomas"
def getReverseName(name):
    x = name.find(" ")
    if x > -1:
        return name[x+1:] + " "+ name[:x]
    return "XXX"

def getLastNames(allPlayerNames):
    import re
    #first split all team names
    lastNames = list()
    for name in allPlayerNames:
        wholeName = name
        lastName = wholeName
        if " " in wholeName and wholeName != "serey die":
            lastName = re.sub('\w+ ', '', wholeName, 1)
            lastName = re.sub(',.*$', '', lastName)
        lastNames.append(lastName)
    #remove dublicates
    for name in lastNames:
        if lastNames.count(name) > 1:
            lastNames = replaceDublicates(lastNames, name)
    return lastNames 

#remove dublicate names and mark them with content "DUBLICATES"
def replaceDublicates(nameList, checkElement):
    result = list()
    for name in nameList:
        if name == checkElement:
            result.append("DUBLICATE")
        else:
            result.append(name)
    return result

#returns the database id of the player by name
def getPlayerIDByName(name):
    import sqlite3
    sqlite_file = 'database.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    queryText = 'SELECT id FROM player WHERE lower(player_name) = "'+ str(name)+'"'
    c.execute(queryText)
    playerID = c.fetchall()
    conn.close()
    return playerID[0][0]

#Returns list with names of found players
def getPlayersInQuery(query):
    playerList = list()
    replace = "SPIELER"
    allPlayerNames = getAllPlayerNames()
    for name in allPlayerNames:
        seperateNameString = '(^| )'+name+'( |$|\W)'
        import re
        if re.search(seperateNameString, query):
            playerList.append(getPlayerIDByName(name))
            query = query.replace(name, replace)
        #user input pattern: Lastname Firstname instead of Firstname Lastname
        if name.find(" ") > -1:
            reverseName = getReverseName(name)
            seperateNameString = '(^| )'+reverseName+'( |$|\W)'
            import re
            if re.search(seperateNameString, query):
                playerList.append(getPlayerIDByName(name))
                index = query.find(getReverseName(name))
                query = query[0:index]+ replace + query[index+len(name):len(query)]
    #user input only includes players' last name
    lastNames = getLastNames(allPlayerNames)
    for i in range(len(lastNames)):
        seperateNameString = '(^| )'+lastNames[i]+'( |$|\W)'
        import re
        if re.search(seperateNameString, query):
            playerList.append(getPlayerIDByName(allPlayerNames[i]))
            query = query.replace(lastNames[i], replace)
    return [playerList, query]

#search for countries##################################################################################

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
    regExCountryList = ['belgi(an|sche?|en)', 'engl(and|(is(ch|h)e?))', 'fran(ce|zoesische?|kreich)', '(deutsche?|german)', 'ital(ienische?|ian|ien|y)', '(holla(endische?|nd)|niederla(endische?|nd)|dutch|netherland)', 'pol(nische?|ish|en|and)', 'portug(iesische?|uese|al)', '(scot(tish|land)|schott(lae?nd)?ische?)', 'spa(nische?|in|nien)', '(schweiz((er(ische?)?)?)|swiss|switzerland)']
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
    replace = "COUNTRY"
    for regEx in getRegExForCountries():
        combinedRegEx = regEx + " (League|Liga)"
        import re
        searchString = '(^| )'+combinedRegEx+'( |$|\W)'
        if re.search(searchString, query, re.IGNORECASE):
            matchedString = matchObject.group(0)
            query = query.replace(matchedString, replace)
            foundCountryList.append(getAllCountries()[getRegExForCountries().index(regEx)])
    return [foundCountryList, query]


#search for leagues##################################################################################

def getAllLeagues():
    import sqlite3
    sqlite_file = 'database.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('SELECT name FROM league')
    leagueNames = c.fetchall()
    conn.close()
    #make system case insensitive
    leagueNamesLower = list()
    for league in leagueNames:
        league = league[0]
        leagueNamesLower.append(league.lower())
    return leagueNamesLower

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
    queryText = 'SELECT id FROM league WHERE lower(name) = "'+ name+'"'
    c.execute(queryText)
    leagueID = c.fetchall()
    conn.close()
    return leagueID[0][0]

#returns a list with IDs of found leagues
def getLeaguesInQuery(query):
    leagueList = list()
    replace = "LEAGUE"
    for name in getAllLeagues():
        import re
        searchString = '(^| )'+name+'( |$|\W)'
        if re.search(searchString, query):
            query = query.replace(name, replace)
            leagueList.append(getLeagueIDByName(name))
        else:
            for part in getLeagueNameParts(name):
                seperateNameString = '(^| )'+part+'( |$|\W)'
                import re
                if re.search(seperateNameString, query):
                    query = query.replace(part, replace)
                    leagueList.append(getLeagueIDByName(name))
    #checks if there is country information for the league in the query (e.g. "deutsche Liga")
    countryList = getCountryListInQuery(query)[0]
    query = getCountryListInQuery(query)[1]
    for foundCountry in countryList:
        leagueList.append(getCountryIDByName(foundCountry[0]))
    return [leagueList, query]


#search for teams##################################################################################

def getAllTeamNames():
    import sqlite3
    sqlite_file = 'database.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('SELECT team_long_name FROM team')
    teamNames = c.fetchall()
    conn.close()
    #make system case insensitive
    teamNamesLower = list()
    for team in teamNames:
        team = team[0]
        teamNamesLower.append(team.lower())
    #remove dublicate entries
    teamNamesLower = list(set(teamNamesLower))
    return teamNamesLower

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
def splitTeamNames(allTeamNames):
    #first split all team names
    teamNamesSplitted = list()
    offCutParts = list()
    teamNames = allTeamNames
    for team in teamNames:
        teamNamesSplitted.append(team.split())
    #remove abbrevs and numbers
    for i in range(len(teamNamesSplitted)):
        for part in teamNamesSplitted[i]:
            if len(part) < 4:
                offCutParts.append(part)
                teamNamesSplitted[i].remove(part)
    #remove dublicates
    for i in range(len(teamNamesSplitted)):
        for part in teamNamesSplitted[i]:
            if isDublicate(teamNamesSplitted, part) == True or part == "den":
                mergeElement(teamNamesSplitted, part)
    return teamNamesSplitted, offCutParts   

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
    print(name)
    import sqlite3
    sqlite_file = 'database.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    queryText = 'SELECT id FROM team WHERE lower(team_long_name) = "'+ name+'"'
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
def getTeamsInQuery(query):
    import re
    teamList = list()
    replace = "TEAM"
    #is the input a valid abbreviation for a team
    allTeamAbbrevs = getAllTeamAbbrevs()
    for abbrev in allTeamAbbrevs:
        import re
        searchString = '(^| )'+abbrev[0]+'( |$|\W)'
        if re.search(searchString, query):
            if isDublicate(allTeamAbbrevs, abbrev[0]) == False:
                query = query.replace(abbrev[0], replace)
                teamList.append(getTeamIDByAbbrev(abbrev[0]))
    #is the input a valid name for a team
    allTeamNames = getAllTeamNames()
    for name in allTeamNames:
        import re
        searchString = '(^| )'+name+'( |$|\W)'
        if re.search(searchString, query):
            query = query.replace(name, replace)
            teamList.append(getTeamIDByName(name))
    #is the input a valid tranformed name for a team
    splittedTeamNames, offCutTeamParts = splitTeamNames(allTeamNames)
    for i in range(len(splittedTeamNames)):
        for part in splittedTeamNames[i]:
            #make sure the part is detached
            import re
            searchString = '(^| )'+part+'( |$|\W)'
            matchedObject = re.search(searchString, query)
            if matchedObject:
                matchedString = matchedObject.group(0)[1:][:-1]
                query = query.replace(matchedString, replace)
                teamList.append(getTeamIDByName(allTeamNames[i]))
    #remove abbrevs of query (e.g. "FC")
    for part in offCutTeamParts:
        searchString = '(^| )'+part+'( |$|\W)'
        query = query.replace(searchString, " ")
    teamList = list(set(teamList))
    return [teamList, query]

    
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

def getAllSeasonAbbrevs(allSeasons):
    abbrevList = list()
    for season in allSeasons:
        season = season[1:]
        season = season[1:]
        season = season[0:4: ] + season[5: : ]
        season = season[0:3: ] + season[4: : ]
        abbrevList.append(season)
    return abbrevList

def getSeasonByAbbrev(abbrev, allSeasons, allAbbrevs):
    for element in allAbbrevs:
        if abbrev == element:
            index = allAbbrevs.index(element)
            return allSeasons[index]

def getSeasonsInQuery(query):
    seasonList = list()
    replace = "SEASON"
    allSeasons = getAllSeasons()
    for season in allSeasons:
        import re
        searchString = '(^| )'+season+'( |$|\W)'
        if re.search(searchString, query):
            query = query.replace(season, replace)
            seasonList.append(season)
    allAbbrevs = getAllSeasonAbbrevs(allSeasons)
    for abbrev in allAbbrevs:
        import re
        searchString = '(^| )'+abbrev+'( |$|\W)'
        if re.search(searchString, query):
            query = query.replace(abbrev, replace)
            seasonList.append(getSeasonByAbbrev(abbrev, allSeasons, allAbbrevs))
    query = query.replace("saison", "") 
    return [seasonList, query]


#search for stages##################################################################################

def getStages(query):
    import re
    stageList = list()
    replace = "STAGE"
    searchString = re.compile("(\d+\.?\s?spieltag)")
    matchObject = searchString.findall(query)
    print(matchObject)
    for match in matchObject:
        print(match)
        query = query.replace(match, replace)
        stageString = ""
        for element in match:
            print(element)
            if element != "." and element != "s" and element != " ":
                stageString = stageString + element
            else: break
        stageList.append(stageString)
    return [stageList, query]
