

#returns answer if user asks for player's birthday
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

    
#returns answer if user asks for player's weight
def getWeight(query):
    print("get weight")
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT weight FROM player WHERE id = '+str(query[0][0])
    c.execute(queryText)
    weight = c.fetchall()[0]
    conn.close()
    weight = int(weight[0] * 0.4535924 )
    return "Die Person wiegt " + str(weight) + "kg."


#returns answer if user asks for player's height
def getHeight(query):
    print("get Height")
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT height FROM player WHERE id = '+str(query[0][0])
    c.execute(queryText)
    height = c.fetchall()[0]
    print("height:" + str(height[0]))
    conn.close()
    return "Die Person ist " + str(height[0]) + "cm groß."


#returns answer if user asks for player's preferred foot
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
 

#returns answer if user asks for player's team
def getTeamOfPlayer(query):
    team = getTeamNameByAPIID(getTeamApiIDByPlayerID(query[0][0], ""))
    return "Der Spieler spielte in Saison 2015/2016 bei " +team + "." 

#returns answer if user asks for player's team at given season
def getTeamOfPlayerInSeason(query):
    team = getTeamNameByAPIID(getTeamApiIDByPlayerID(query[0][0], query[3][0]))
    return "Der Spieler spielte in Saison " + query[3][0]+ " bei " +team + "." 


#returns answer if user asks for seasons when player was in given team 
def getSeasonsOfPlayerInTeam(query):
    player = query[0][0]
    team = getTeamApiIDByID(query[2][0])
    allSeasons = ["2008/2009", "2009/2010", "2010/2011", "2011/2012", "2012/2013", "2013/2014", "2014/2015", "2015/2016"]
    seasons = []
    for season in allSeasons:
        team_with_player = getTeamApiIDByPlayerID(player, season)
        if team_with_player == team:
            seasons.append(season)      
    return "Die Person spielte " + str(seasons) + " beim diesem Verein."


#TODO: nicht in Umfrage
#returns answer if user asks for stats of two teams 
def getTeamVSTeamStats(query):
    team1 = getTeamApiIDByID(query[2][0])
    team2 = getTeamApiIDByID(query[2][1])
    
    season = query[3][0]
    if season:
        season_string = 'season = "' + season + '"'
    else:
        season_string = ''
        
    results = getTeamVsTeamStatsByTeamApiIDs(team1, team2, season_string)
    return "Ergebnisse von " + getTeamNameByAPIID(team1) + " gegen " +  getTeamNameByAPIID(team2) + ":" + results
    
    
    #team1 = getTeamApiBy(query[2][0])
    #team2 = getTeamNameByID(query[2][1])
    
    #if not season:
    #    season_string = 'season = "2015/2016"'
    #else:
    #    season_string = 'season = "' + season + '"'
    
    #results = getHomeGoalsAgainst( getTeamApiIDByID(query[2][0]), getTeamApiIDByID(query[2][1]), season_string)
    #results2 = getAwayGoalsAgainst( getTeamApiIDByID(query[2][0]), getTeamApiIDByID(query[2][1]), season_string)
    

#returns answer if user asks for team-stats of stage
def getStageStatsOfTeam(query):
    team = getTeamApiIDByID(query[2][0])
    stage = query[4][0]
    stage_string = 'stage = "' + stage + '"'
    
    if query[3]:
        season = query[3][0]
    else:
        season = "2015/2016"
    season_string = 'season = "' + season + '"'
              
    rival = getRivalApiID(team, stage_string, season_string)
    resultsTeam1 = getGoalsOfTeam(team, season_string, stage_string)
    resultsTeam2 = getGoalsOfTeam(rival, season_string, stage_string)

    stat_string = " gegen " +getTeamNameByAPIID(rival)+ " gespielt: " +str(resultsTeam1)+ ":" +str(resultsTeam2)
    return "Dieses Team hat an Spieltag " + stage + " in Saison " + season + stat_string  


#returns answer if user asks for rival
def getRival(query):
    team = getTeamApiIDByID(query[2][0])
    stage = query[4][0]
    stage_string = 'stage = "' + stage + '"'
    
    if query[3]:
        season = query[3][0]
    else:
        season = "2015/2016"
    season_string = 'season = "' + season + '"'
    
    rival = getRivalApiID(team, stage_string, season_string)
    return "Dieses Team hat an Spieltag " + stage + " in Saison " + season + " gegen " +getTeamNameByAPIID(rival)+ " gespielt."


#returns answer if user asks for player line-up
def getLineup(query):
    team = getTeamApiIDByID(query[2][0])
    stage = query[4][0]
    stage_string = 'stage = "' + stage + '"'
    
    if query[3]:
        season = query[3][0]
    else:
        season = "2015/2016"
    season_string = 'season = "' + season + '"'
    
    lineup = getLineupByTeamApiID(team, season_string, stage_string)
    print(lineup)
    return "Die Aufstellung dieses Teams an Spieltag" +stage+ " in Saison " +season+ " war wie folgt: " +str(lineup)


#returns answer if user asks if a team was home-team
def getWasHomeTeam(query):
    team = getTeamApiIDByID(query[2][0])
    stage = query[4][0]
    stage_string = 'stage = "' + stage + '"'
    
    if query[3]:
        season = query[3][0]
    else:
        season = "2015/2016"
    season_string = 'season = "' + season + '"'
    
    if isHomeTeam(team, season_string, stage_string):
        return "Diese Mannschaft spielte zum angegeben Spieltag daheim."
    else:
        return "Diese Mannschaft spielte zum angegeben Spieltag auswärts."
 

#returns answer if user asks for win/Defeat-stats
#all wins ever
def getNumWin(query):
    team = getTeamApiIDByID(query[2][0])
    num = getNumWinByTeamApiID(team, -1, True, '')
    return "Diese Mannschaft hat in den gesamten Aufzeichnungen " +str(num)+ "-mal gewonnen."

#all failures ever   
def getNumDefeat(query):
    team = getTeamApiIDByID(query[2][0])
    num = getNumWinByTeamApiID(team, -1, False, '')
    return "Diese Mannschaft hat in den gesamten Aufzeichnungen " +str(num)+ "-mal verloren."
    
#all wins of season  
def getNumWinInSeason(query):
    team = getTeamApiIDByID(query[2][0])
    season_string = 'season = "' + query[3][0] + '"'
    num = getNumWinByTeamApiID(team, -1, True, season_string)
    return "Diese Mannschaft hat in Saison " +str(query[3][0])+ " " +str(num)+ "-mal gewonnen."

#all failures of season    
def getNumDefeatInSeason(query):
    team = getTeamApiIDByID(query[2][0])
    season_string = 'season = "' + query[3][0] + '"'
    num = getNumWinByTeamApiID(team, -1, False, season_string)
    return "Diese Mannschaft hat in Saison " +str(query[3][0])+ " " +str(num)+ "-mal verloren."

#all wins against team ever      
def getNumWinAgainstTeam(query):
    team1 = getTeamApiIDByID(query[2][0])
    team2 = getTeamApiIDByID(query[2][1])
    num = getNumWinByTeamApiID(team1, team2, True, '')
    return "Mannschaft " +getTeamNameByAPIID(team1)+" hat " +str(num)+ "-mal gegen " +getTeamNameByAPIID(team2)+ " gewonnen."
    
#all failures against team ever    
def getNumDefeatAgainstTeam(query):
    team1 = getTeamApiIDByID(query[2][0])
    team2 = getTeamApiIDByID(query[2][1])
    num = getNumWinByTeamApiID(team1, team2, False, '')
    return "Mannschaft " +getTeamNameByAPIID(team1)+" hat " +str(num)+ "-mal gegen " +getTeamNameByAPIID(team2)+ " verloren."

#all wins against team of season        
def getNumWinAgainstTeamInSeason(query):
    team1 = getTeamApiIDByID(query[2][0])
    team2 = getTeamApiIDByID(query[2][1])
    season_string = 'season = "' + query[3][0] + '"'
    num = getNumWinByTeamApiID(team1, team2, True, season_string)
    return "Mannschaft " +getTeamNameByAPIID(team1)+" hat in Saison " +str(query[3][0])+ " " +str(num)+ "-mal gegen " +getTeamNameByAPIID(team2)+ " gewonnen."
    
#all failures against team of season   
def getNumDefeatAgainstTeamInSeason(query):
    team1 = getTeamApiIDByID(query[2][0])
    team2 = getTeamApiIDByID(query[2][1])
    season_string = 'season = "' + query[3][0] + '"'
    num = getNumWinByTeamApiID(team1, team2, False, season_string)
    return "Mannschaft " +getTeamNameByAPIID(team1)+" hat in Saison " +str(query[3][0])+ " " +str(num)+ "-mal gegen " +getTeamNameByAPIID(team2)+ " verloren."

    
def getAnswers():

    #query objects are the "refined queries" which contain arrays with the occurring id of
    #[0]Player/[1]League/[2]Team/[3]Season/[4]State bzw. Day


    answers = []
    answers.append([1,0,0,0,0, getBirthday, 0])
    answers.append([1,0,0,0,0, getWeight, 1])

    answers.append([1,0,0,0,0, getHeight, 6])
    answers.append([1,0,0,0,0, getPreferredFoot, 2])
    answers.append([1,0,0,0,0, getTeamOfPlayer, 3])
    answers.append([1,0,0,1,0, getTeamOfPlayerInSeason, 4])
    
    answers.append([0,0,2,0,0, getTeamVSTeamStats])
    answers.append([0,0,2,1,0, getTeamVSTeamStats])
        
    answers.append([1,0,1,0,0, getSeasonsOfPlayerInTeam, 5])
    
    answers.append([0,0,1,0,1, getStageStatsOfTeam, 16])
    answers.append([0,0,1,1,1, getStageStatsOfTeam, 7]) 
    
    answers.append([0,0,1,1,1, getRival, 8])
    
    answers.append([0,0,1,1,1, getLineup, 17]) 
    answers.append([0,0,1,0,1, getLineup, 9])
    
    answers.append([0,0,1,1,1, getWasHomeTeam, 11]) 
    answers.append([0,0,1,0,1, getWasHomeTeam, 18])
    
    answers.append([0,0,1,0,0, getNumWin, 19])
    answers.append([0,0,1,0,0, getNumDefeat, 21])
    answers.append([0,0,2,0,0, getNumWinAgainstTeam, 22])
    answers.append([0,0,2,0,0, getNumDefeatAgainstTeam, 23])
    
    answers.append([0,0,1,1,0, getNumWinInSeason, 10])
    answers.append([0,0,1,1,0, getNumDefeatInSeason, 20])
    answers.append([0,0,2,1,0, getNumWinAgainstTeamInSeason, 24])
    answers.append([0,0,2,1,0, getNumDefeatAgainstTeamInSeason, 12])
    
    return answers




#########################################################################################################################



#ungenutzt
def getHomeGoalsAgainst(team_api_id1, team_api_id2, season):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    
    season = " AND season = " + season 
    
    queryText = 'SELECT home_team_goal FROM match WHERE (home_team_api_id = '+str(team_api_id1)+' AND away_team_api_id = '+str(team_api_id2)+ ")" + season
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result

#ungenutzt
def getAwayGoalsAgainst(team_api_id1, team_api_id2, season):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()

    season = " AND season = " + season 
    
    queryText = 'SELECT away_team_goal FROM match WHERE (away_team_api_id = '+str(team_api_id1)+' AND home_team_api_id = '+str(team_api_id2)+ ')' + season
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result


#TODO? s.oben 
def getTeamVsTeamStatsByTeamApiIDs(team1_api_id, team2_api_id, season):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    
    queryText = 'SELECT home_team_goal, away_team_goal' #...
    
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return


#returns number of goals of a specific team in a specific game
def getGoalsOfTeam(team_api_id, season, stage):
    # 'stage = "' + query[4][0] + '"'
    # season_string = 'season = "' + season + '"'
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    if isHomeTeam(team_api_id, season, stage):
        queryText = 'SELECT home_team_goal FROM match WHERE ' + stage + ' AND ' + season + ' AND home_team_api_id =' +str(team_api_id)
    else:
        queryText = 'SELECT away_team_goal FROM match WHERE ' + stage + ' AND ' + season + ' AND away_team_api_id =' +str(team_api_id)
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result[0][0]


#returns API-ID of rival of a team at a specific game 
def getRivalApiID(team_api_id, stage, season):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT home_team_api_id, away_team_api_id FROM match WHERE ' + stage + ' AND ' + season + ' AND (home_team_api_id =' +str(team_api_id)+ ' OR away_team_api_id = ' +str(team_api_id)+ ')'
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    if result[0][0] == team_api_id:
        return result[0][1]
    else:
        return result[0][0]

    
#returns player line-up of a specific team at a specific game 
def getLineupByTeamApiID(team_api_id, season, stage):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()

    if isHomeTeam(team_api_id, season, stage):
        selection_string = 'home_player_1, home_player_2, home_player_3, home_player_4, home_player_5, home_player_6, home_player_7, home_player_8, home_player_9, home_player_10, home_player_11'
        queryText = 'SELECT '+selection_string+ ' FROM match WHERE ' +stage+ ' AND ' +season+ ' AND home_team_api_id =' +str(team_api_id)
    else:
        selection_string = 'away_player_1, away_player_2, away_player_3, away_player_4, away_player_5, away_player_6, away_player_7, away_player_8, away_player_9, away_player_10, away_player_11'
        queryText = 'SELECT '+selection_string+ ' FROM match WHERE ' +stage+ ' AND ' +season+ ' AND away_team_api_id =' +str(team_api_id)
    
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    
    lineup = []
    for player in result[0]:
        lineup.append(getPlayerNameByApiID(player))
        
    return lineup
    

#returns boolean if a team was playing at home at specific game
def isHomeTeam(team_api_id, season, stage):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT home_team_api_id, away_team_api_id FROM match WHERE ' + stage + ' AND ' + season + ' AND (home_team_api_id =' +str(team_api_id)+ ' OR away_team_api_id = ' +str(team_api_id)+ ')'
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    if result[0][0] == team_api_id:
        return True
    else:
        return False


#returns number of wins of a specific team
#params:
# - team_api_id: the team user wants info about
# - team2_api_id: if user wants to knwo num wins against team2 (default: -1)
# - isAskedForWin: boolean True: count wins, boolean False: counts failures
# - season: season-String to specify query to a season
def getNumWinByTeamApiID(team_api_id, team2_api_id, isAskedForWin, season):
    #has user asked for one-team-only (if) or team-vs-team (else) stats?
    if team2_api_id == -1:
        where_team_string1 = '(home_team_api_id = ' +str(team_api_id)+ ')'
        where_team_string2 = '(away_team_api_id = ' +str(team_api_id)+ ')'
    else:
        where_team_string1 = '(home_team_api_id = ' +str(team_api_id)+ ' AND away_team_api_id = ' +str(team2_api_id)+ ')' 
        where_team_string2 = '(away_team_api_id = ' +str(team_api_id)+ ' AND home_team_api_id = ' +str(team2_api_id)+ ')' 

    #has user asked for win (if) or Defeat (else) stats?
    if isAskedForWin:
        where_string = '(' +where_team_string1+ ' AND home_team_goal > away_team_goal) OR (' +where_team_string2+ ' AND away_team_goal > home_team_goal)'
    else:
        where_string = '(' +where_team_string1+ ' AND home_team_goal < away_team_goal) OR (' +where_team_string2+ ' AND away_team_goal < home_team_goal)'
    
    #has user asked for stats of specific season?
    if not season == "":
        where_string = season + ' AND (' + where_string + ')'

    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT COUNT(id) FROM match WHERE ' + where_string
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result[0][0]


#returns home-matches of player by player-api-id and season
def getHomeMatchesOfPlayer(player_api_id, season):
    if(season == ""):
        season = 'season = "2015/2016"'
    else:
        season = 'season = "' + season + '"'

    
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()

    queryText = 'SELECT id FROM match WHERE ' +season+' AND ( home_player_1 =' + str(player_api_id) + ' OR home_player_2 =' + str(player_api_id) + ' OR home_player_3 =' + str(player_api_id)+ ' OR home_player_4 =' + str(player_api_id)+ ' OR home_player_5 =' + str(player_api_id)+ ' OR home_player_6 =' + str(player_api_id)+ ' OR home_player_7 =' + str(player_api_id)+ ' OR home_player_8 =' + str(player_api_id)+ ' OR home_player_9 =' + str(player_api_id)+ ' OR home_player_10 =' + str(player_api_id)+ ' OR home_player_11 =' + str(player_api_id) + ")"

    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result

#ungenutzt
#returns player-API-ID by player-name

def getPlayerAPIIdByName(player_name):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT player_api_id FROM player WHERE player_name = "' + player_name +'"'
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result[0][0]


#returns player-API-ID by player-id
def getPlayerAPIIdById(player_id):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT player_api_id FROM player WHERE id = "' + str(player_id) +'"'
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result[0][0]


#returns player-name by player-api-id
def getPlayerNameByApiID(player_api_id):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT player_name FROM player WHERE player_api_id = ' + str(player_api_id)
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result[0][0]
    


#returns team-API-ID by player-id
def getTeamApiIDByPlayerID(player_id, season):
    matches = getHomeMatchesOfPlayer(getPlayerAPIIdById(player_id),season)
    if matches:
        import sqlite3
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        #print(str(matches[0][0]))
        queryText = 'SELECT home_team_api_id FROM match WHERE id = ' + str(matches[0][0])
        c.execute(queryText)
        result = c.fetchall()
        conn.close()
        return result[0][0]

    
#returns team-name by team-api-id    

def getTeamNameByAPIID(team_api_id):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT team_long_name FROM team WHERE team_api_id = ' + str(team_api_id)
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result[0][0]


#returns team-api-id by team-id
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


#ungenutzt
#returns team-name by team-id
def getTeamNameByID(team_id):
    import sqlite3
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    queryText = 'SELECT team_long_name FROM team WHERE id = ' + str(team_id)
    c.execute(queryText)
    result = c.fetchall()
    conn.close()
    return result[0][0]

#ungenutzt
#returns team-api-is by team-name

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