import sqlite3
import matplotlib.pyplot as plt

def query(userid, source, time_start, time_end):
    # Get temp and humidity for the time range [<time_start>, <time_end>] for specified <userid> and <source>
    output = []
    cur = sqlite3.connect("data.db").cursor()
    for time in range(time_start, time_end+1):
        command = '''SELECT temp, humidity from temprh WHERE userid=? and source=? and time=?'''
        cur.execute(command, (userid, source, time))
        result = cur.fetchone()
        if result is not None:
            output.append(result)
    return(output)

def get_sources(userid):
    # select unique source, label pairs
    command = '''SELECT DISTINCT source, label from temprh WHERE userid=?'''
    cur = sqlite3.connect("data.db").cursor()
    cur.execute(command, (userid,))
    result = cur.fetchall()
    return result

def get_label(userid, source):
    command = '''SELECT DISTINCT label from temprh WHERE userid=? '''
    cur = sqlite3.connect("data.db").cursor()
    cur.execute(command, (userid,))
    result = cur.fetchone()
    return result[0]

def save_graph(time, temp, humidity, userid, source):
    # plot temp
    plt.figure(figsize=(10,8))
    plt.plot(time, temp, color='red')
    plt.title('Temperature', fontsize=18)
    plt.xlabel('Hour', fontsize=16)
    plt.ylabel('Fahrenheit', fontsize=16)
    plt.savefig('../tmp_files/'+userid+'_'+str(source)+'temp.png')

    # plot humidity
    plt.figure(figsize=(10,8))
    plt.plot(time, humidity, color='blue')
    plt.title('Humidity', fontsize=18)
    plt.xlabel('Hour', fontsize=16)
    plt.ylabel('Relative Humidity', fontsize=16)
    plt.savefig('../tmp_files/'+userid+'_'+str(source)+'_hum.png')

def add_source(userid, source, label):
    connection = sqlite3.connect("data.db") 
    cur = connection.cursor()

    # Check if source unique to userid
    command_get_sources = ''' SELECT DISTINCT source from temprh WHERE userid=? '''
    cur.execute(command_get_sources, (userid,))
    distinct_sources = cur.fetchall()
    distinct_sources = [i[0] for i in distinct_sources]
    if source in distinct_sources:
        print("ERROR: Source for user already exists!")
        return

    # Insert source for userid into table by loggin temp and humidity for 24 hours
    command = ''' INSERT into temprh(userid,source,label,time,temp,humidity) VALUES(?,?,?,?,?,?); '''
    for i in range(1,25):
       cur.execute(command, (userid, source, label, i, i+1, i+2))

    connection.commit()

if __name__ == "__main__":

    connection = sqlite3.connect("data.db")

    create_table = ''' CREATE TABLE IF NOT EXISTS temprh (
        userid text NOT NULL,
        source integer NOT NULL,
        label text NOT NULL, 
        time integer,
        temp integer,
        humidity real,
        PRIMARY KEY (userid, source, time)
    ); '''

    cur = connection.cursor()
    cur.execute(create_table)
    
    add_source('jhua', 1, 'ma first source')
    tempHumidity = query('jhua', 1, 1, 100)
    temp = [i[0] for i in tempHumidity]
    humidity = [i[1] for i in tempHumidity]
  
    save_graph(range(1,25), temp, humidity, 'jhua', 1) 


    add_source('jhua', 3, 'ma first source')
    add_source('jhua', 4, 'ma twoth source')
    add_source('aa', 1, 'ma first source')
    add_source('aa', 7, 'ma first source')
    get_label('jhua', 1)
    