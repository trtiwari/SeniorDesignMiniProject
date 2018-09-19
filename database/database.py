import sqlite3
import random
import matplotlib.pyplot as plt

def query(DOC_ROOT, userid, source, time_start, time_end):
    '''
    Get temp and humidity for the time range [<time_start>, <time_end>] for specified <userid> and <source>.

    Args:
        DOC_ROOT (str): Path to project directory
        userid (str): Unique id for user
        source (int): Source number
        time_start (int): Start time for pulling out temp and hum values
        time_end (int): End time for pulling out temp and hum values

    Returns:
    '''
    output = []
    command = '''SELECT temp, humidity from temprh WHERE userid=? and source=? and time=?'''
    try:
        cur = sqlite3.connect(DOC_ROOT + "/database/data.db").cursor()
        for time in range(time_start, time_end+1):
            cur.execute(command, (userid, source, time))
            result = cur.fetchone()
            if result is not None:
                output.append(result)
    except sqlite.Error as e:
        print('query() Error %s: ' % e.args[0])
    finally:
        cur.close()
    
    return(output)

def get_sources(DOC_ROOT, userid):
    '''
    Select unique source, label pairs for <userid>.

    Args:
        DOC_ROOT (str): Path to project directory
        userid (str): Unique id for user

    Returns:
        result (list of tuples): List of all unique (source, label) pairs for <userid>
    '''
    command = '''SELECT DISTINCT source, label from temprh WHERE userid=?'''
    try:
        cur = sqlite3.connect(DOC_ROOT + "/database/data.db").cursor()
        cur.execute(command, (userid,))
        result = cur.fetchall()
    except sqlite.Error as e:
        print('get_sources() Error %s' % e.args[0])
    finally:
        cur.close()
    
    return result

def get_label(DOC_ROOT, userid, source):
    '''
    Get label of source belonging to <userid>.

    Args:
        DOC_ROOT (str): Path to project directory
        userid (str): Unique id for user
        source (int): Source number
        
    Returns:
        result[0] (str): Name of source
    '''
    command = '''SELECT DISTINCT label from temprh WHERE userid=? and source=? '''
    try:
        cur = sqlite3.connect(DOC_ROOT + "/database/data.db").cursor()
        cur.execute(command, (userid, source))
        result = cur.fetchone()
    except sqlite.Error as e:
        print('get_label() Error %s' % e.args[0])
    finally:
        cur.close()
    
    return result[0]

def save_graph(DOC_ROOT, time, temp, humidity, userid, source):
    '''
    Plot and save graphs of time vs temp and time vs humidity for source belonging to <userid>
    Plots are saved in folder tmp/, which is cleared upon user sign out.

    Args:
        DOC_ROOT (str): Path to project directory
        time (list): List of time (by hour) values to plot against temperature and humidity
        temp (list): List of temperature values to plot against time 
        humidity (list): List of humidity values to plot against time 
        userid (str): Unique id for user
        source (int): Source number

    Returns:
        None
    ''' 
    # plot temp vs time
    plt.figure(figsize=(12,8))
    plt.plot(time, temp, color='red')
    plt.title('Temperature', fontsize=24)
    plt.xlabel('Hour', fontsize=18)
    plt.ylabel('Fahrenheit', fontsize=18)
    plt.xticks(range(24))
    plt.tick_params(labelsize=15)
    plt.ylim(0,100)
    plt.savefig(DOC_ROOT + '/tmp_files/'+userid+'_'+str(source)+'_temp.png')

    # plot humidity vs time
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
    '''
    For <userid>, add a source with label <label>
    Args:
        DOC_ROOT (str): Path to project directory
        userid (str): Unique id for user
        label (str): Name of source

    Returns:
        None
    '''
    connection = sqlite3.connect(DOC_ROOT + "/database/data.db") 
    cur = connection.cursor()

    # Get new source number
    command_get_sources = ''' SELECT DISTINCT source from temprh WHERE userid=? '''
    try:
        cur.execute(command_get_sources, (userid,))
        distinct_sources = cur.fetchall()
        new_source = len(distinct_sources) + 1
    except sqlite.Error as e:
        print('add_source() Error %s' % e.args[0])

    ### Insert source for userid into table by logging temp and humidity for 24 hours
    command = ''' INSERT into temprh(userid,source,label,time,temp,humidity) VALUES(?,?,?,?,?,?); '''
    # Keep randomly generated temp and hum values within reasonable ranges
    temp_mid = random.randint(10,91)
    hum_mid = random.randint(10,91)
    try:
        for i in range(24):
            # Randomly generate temp and hum 
            temp_i = random.randint(temp_mid-10, temp_mid+10)
            hum_i = random.randint(hum_mid-10, hum_mid+10)
            # Insert temp and hum at hour <i> into table
            cur.execute(command, (userid, new_source, label, i, temp_i, hum_i)) 

        connection.commit()
    except sqlite.Error as e:
        print('add_source() Error %s' % e.args[0])
    finally:
        cur.close()
        connection.close()

def create_table():
    '''
    Create table located in data.db called temprh

    Args: 
        None

    Returns:
        None
    '''
    # Create table with primary key (unique identifier) as (userid, source, time)
    create_table = ''' CREATE TABLE IF NOT EXISTS temprh (
        userid text NOT NULL,
        source integer NOT NULL,
        label text NOT NULL, 
        time integer,
        temp integer,
        humidity real,
        PRIMARY KEY (userid, source, time)
          ); '''

    try:
        connection = sqlite3.connect("database/data.db")
        cur = connection.cursor()
        cur.execute(create_table)
        
        connection.commit()
    except sqlite.Error as e:
        print('create_table() Error %s' % e.args[0])
    finally:
        cur.close()
        connection.close()
    