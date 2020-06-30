
def getAllPlayerNames():
    import sqlite3
    sqlite_file = 'database.sqlite'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('SELECT player_name FROM player')
    playerNames = c.fetchall()
    conn.close()
    return playerNames