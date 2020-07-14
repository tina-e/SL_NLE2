

def getBirthday(query):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT birthday FROM player WHERE id = '+str(query[0][0])
    c.execute(queryText)
    birthday = c.fetchall()[0]
    conn.close()
    bday = str(birthday[0])
    return "Der Geburtstag ist am " + bday[8:10] + "." + bday[5:7] + "." + bday[0:4] + "."
    
def getWeight(query):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT weight FROM player WHERE id = '+str(query[0][0])
    c.execute(queryText)
    weight = c.fetchall()[0]
    conn.close()
    weight = int(weight[0] * 0.4535924 )
    return "Die Person wiegt " + str(weight) + "kg."
    
def getPreferredFoot(query):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT preferred_foot FROM player_attributes INNER JOIN player ON player.player_api_id = player_attributes.player_api_id WHERE player.id = '+str(query[0][0])
    c.execute(queryText)
    preferredFoot = c.fetchall()[0]
    conn.close()
    if(preferredFoot[0] == "left"):
        preferredFoot = 'links'
    else:
        preferredFoot = 'rechts'
        
    return "Der bevorzugte Fuß ist " + preferredFoot + "." 
    
def getTeamOfPlayer(query):
    team = getTeamNameByAPIID(getTeamApiIDByPlayerID(query[0][0], ""))
    return "Der Spieler spielte in Saison 2015/2016 bei " +team + "." 

def getTeamOfPlayerInSeason(query):
    team = getTeamNameByAPIID(getTeamApiIDByPlayerID(query[0][0], query[3][0]))
    return "Der Spieler spielte in Saison " + query[3][0]+ " bei " +team + "." 
    
    
def getTeamVSTeamStats(query):
    # 2 Team (1 Season)
    season = query[3][0]
    #if(season == ""):
    #    season = "season = '2015/2016'"
    #else:
    #    season = "season = '" + season +"'"
    team1 = getTeamNameByID(query[2][0])
    team2 = getTeamNameByID(query[2][1])
    
    
    results = getHomeGoalsAgainst(query[2][0],query[2][1], season)
    results2 = getAwayGoalsAgainst(query[2][0],query[2][1], season)
    #return "Team 1 ist: " + team1 + " Team 2 ist " +  team2 + "."
    return results+results2
    
    
def getAnswers():

    #query objects are the "refined queries" which contain arrays with the occurring id of Player/League/Team/Season

    answers = []
    answers.append([1,0,0,0,0, getBirthday])
    answers.append([1,0,0,0,0, getWeight])
    answers.append([1,0,0,0,0, getPreferredFoot])
    answers.append([1,0,0,0,0, getTeamOfPlayer])
    answers.append([1,0,0,1,0, getTeamOfPlayerInSeason])
    answers.append([0,0,2,0,0, getTeamVSTeamStats])
    answers.append([0,0,2,1,0, getTeamVSTeamStats])
    return answers







def getHomeGoalsAgainst(team_id1, team_id2, season):
    team_api_id1 = getTeamApiIDByID(team_id1)
    team_api_id2 = getTeamApiIDByID(team_id2)
    
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    
    season = '"' + season + '"'
    season = " AND season = " + season 
    
    queryText = 'SELECT home_team_goal FROM match WHERE (home_team_api_id = '+str(team_api_id1)+' AND away_team_api_id = '+str(team_api_id2)+ ")" + season
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result
    
def getAwayGoalsAgainst(team_id1, team_id2, season):
    team_api_id1 = getTeamApiIDByID(team_id1)
    team_api_id2 = getTeamApiIDByID(team_id2)
    
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    
    season = '"' + season + '"'
    season = " AND season = " + season 
    
    queryText = 'SELECT away_team_goal FROM match WHERE (away_team_api_id = '+str(team_api_id1)+' AND home_team_api_id = '+str(team_api_id2)+ ")" + season
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result



def getAPIIDOfPlayer(player_id):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT player_api_id FROM player WHERE id =' + str(player_id)
    c.execute(queryText)
    result = c.fetchall()[0]
    conn.close()
    return result[0]
  
def getHomeMatchesOfPlayer(player_api_id, season):
    if(season == ""):
        season = "season = '2015/2016'"
    else:
        season = "season = '" + season +"'"
    
    
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT id FROM match WHERE ' +season+' AND home_player_1 =' + str(player_api_id) + ' OR home_player_2 =' + str(player_api_id) + ' OR home_player_3 =' + str(player_api_id)+ ' OR home_player_4 =' + str(player_api_id)+ ' OR home_player_5 =' + str(player_api_id)+ ' OR home_player_6 =' + str(player_api_id)+ ' OR home_player_7 =' + str(player_api_id)+ ' OR home_player_8 =' + str(player_api_id)+ ' OR home_player_9 =' + str(player_api_id)+ ' OR home_player_10 =' + str(player_api_id)+ ' OR home_player_11 =' + str(player_api_id)
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result
    
def getPlayerAPIIdByName(player_name):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT player_api_id FROM player WHERE player_name = "' + player_name +'"'
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result[0][0]

def getPlayerAPIIdById(player_id):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT player_api_id FROM player WHERE id = "' + str(player_id) +'"'
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result[0][0]
    
    
def getTeamApiIDByPlayerID(player_id, season):

    matches = getHomeMatchesOfPlayer(getPlayerAPIIdById(player_id),season)
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    #print(str(matches[0][0]))
    queryText = 'SELECT home_team_api_id FROM match WHERE id = ' + str(matches[0][0])
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result[0][0]
    
def getTeamNameByAPIID(team_api_id):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT team_long_name FROM team WHERE team_api_id = ' + str(team_api_id)
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result[0][0]
   
def getTeamNameByID(team_id):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT team_long_name FROM team WHERE id = ' + str(team_id)
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result[0][0]
    
def getTeamApiIDByID(team_id):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    team_id = '"' + str(team_id) + '"'
    queryText = 'SELECT team_api_id FROM team WHERE id = ' + str(team_id)
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result[0][0]
    
def getTeamApiIDByName(team_name):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    team_name = '"' + team_name + '"'
    queryText = 'SELECT team_api_id FROM team WHERE team_long_name =' + team_name
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    #return queryText
    return result[0][0]