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
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    queryText = 'SELECT id FROM country WHERE name = "'+ name+'"'
    c.execute(queryText)
    countryID = c.fetchall()
    conn.close()
    return countryID[0][0]

#searches country information in the query
def getCountryListInQuery(query):
    foundCountryList = list()
    for regEx in getRegExForCountries():
        #if re.search(regEx + " (League|Liga)", query):
        if re.search(regEx, query, re.IGNORECASE):
            foundCountryList.append(getAllCountries()[getRegExForCountries().index(regEx)])
    return foundCountryList


#search for leagues##################################################################################

def getAllLeagues():
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
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    queryText = 'SELECT id FROM league WHERE name = "'+ name+'"'
    c.execute(queryText)
    leagueID = c.fetchall()
    conn.close()
    return leagueID[0][0]

#returns a list with names of found leagues
def getLeaguesInQuery(query):
    leagueList = list()
    for name in getAllLeagues():
        if name[0] in query:
            leagueList.append(name[0])
        else:
            for part in getLeagueNameParts(name[0]):
                if part in query:
                    leagueList.append(getLeagueIDByName(name[0]))
    #checks if there is country information for the league in the query (e.g. "deutsche Liga")             
    for foundCountry in getCountryListInQuery(query):
        leagueList.append(getCountryIDByName(foundCountry))
    return leagueList