import sqlite3
import random
import matplotlib.pyplot as plt

def query(DOC_ROOT, userid, source, time_start, time_end):
    # Get temp and humidity for the time range [<time_start>, <time_end>] for specified <userid> and <source>
    output = []
    cur = sqlite3.connect(DOC_ROOT + "/database/data.db").cursor()
    for time in range(time_start, time_end+1):
        command = '''SELECT temp, humidity from temprh WHERE userid=? and source=? and time=?'''
        cur.execute(command, (userid, source, time))
        result = cur.fetchone()
        if result is not None:
            output.append(result)

    cur.close()
    return(output)

def get_sources(DOC_ROOT, userid):
    # select unique source, label pairs
    command = '''SELECT DISTINCT source, label from temprh WHERE userid=?'''
    cur = sqlite3.connect(DOC_ROOT + "/database/data.db").cursor()
    cur.execute(command, (userid,))
    result = cur.fetchall()

    cur.close()
    return result

def get_label(DOC_ROOT, userid, source):
    command = '''SELECT DISTINCT label from temprh WHERE userid=? and source=? '''
    cur = sqlite3.connect(DOC_ROOT + "/database/data.db").cursor()
    cur.execute(command, (userid,source))
    result = cur.fetchone()

    cur.close()
    return result[0]

def save_graph(DOC_ROOT, time, temp, humidity, userid, source):
    # plot temp
    plt.figure(figsize=(12,8))
    plt.plot(time, temp, color='red')
    plt.title('Temperature', fontsize=24)
    plt.xlabel('Hour', fontsize=18)
    plt.ylabel('Fahrenheit', fontsize=18)
    plt.xticks(range(24))
    plt.tick_params(labelsize=15)
    plt.ylim(0,100)
    plt.savefig(DOC_ROOT + '/tmp_files/'+userid+'_'+str(source)+'_temp.png')

    # plot humidity
    plt.figure(figsize=(12,8))
    plt.plot(time, humidity, color='blue')
    plt.title('Humidity', fontsize=24)
    plt.xlabel('Hour', fontsize=18)
    plt.ylabel('Percent Relative Humidity', fontsize=18)
    plt.xticks(range(24))
    plt.tick_params(labelsize=15)
    plt.ylim(0,100)
    plt.savefig(DOC_ROOT + '/tmp_files/'+userid+'_'+str(source)+'_hum.png')

def add_source(DOC_ROOT, userid, label):
    connection = sqlite3.connect(DOC_ROOT + "/database/data.db") 
    cur = connection.cursor()

    # Get new source number
    command_get_sources = ''' SELECT DISTINCT source from temprh WHERE userid=? '''
    cur.execute(command_get_sources, (userid,))
    distinct_sources = cur.fetchall()
    new_source = len(distinct_sources) + 1

    # Insert source for userid into table by loggin temp and humidity for 24 hours
    command = ''' INSERT into temprh(userid,source,label,time,temp,humidity) VALUES(?,?,?,?,?,?); '''

    random.seed(new_source)
    temp_mid = random.randint(5,96)
    hum_mid = random.randint(5,96)
    for i in range(24):
        temp_i = random.randint(temp_mid-5, temp_mid+5)
        hum_i = random.randint(hum_mid-5, hum_mid+5)
        cur.execute(command, (userid, new_source, label, i, temp_i, hum_i))

    connection.commit()

    cur.close()
    connection.close()

def create_table():
    connection = sqlite3.connect("database/data.db")

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
    
    connection.commit()

    cur.close()
    connection.close()
    