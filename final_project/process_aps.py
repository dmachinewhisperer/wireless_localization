import find_apsV3 
import pandas as pd
import random
import sqlite3
import json

#Notes
#1. find_apsV3 must be imported before this module, whereever it is to be used

#feature vector ordering 
def create_fv_ordering_db(connection):

    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fv_ordering (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bssid INTEGER
        )
    ''')
    connection.commit()


def bssid_exists(connection, bssid):
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM fv_ordering WHERE bssid = ?', (bssid,))
    return cursor.fetchone()[0] > 0

def update_fv(connection):
    #global detected_aps

    create_fv_ordering_db(connection)
    cursor = connection.cursor()

    #detected_aps = detect_aps(7)
    #print(find_apsV3.detected_aps)

    bssids = find_apsV3.detected_aps['bssid'].values

    for bssid in bssids:
      if not bssid_exists(connection, bssid):
          cursor.execute('INSERT INTO fv_ordering (bssid) VALUES (?)', (bssid,))
          connection.commit()


#fingerprints
def create_fingerprint_db(connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fingerprints (
            id INTEGER PRIMARY KEY,
            location_tag TEXT,
            fingerprint TEXT
        )
    ''')
    connection.commit()


#checks if location X have been fingerprinted
def location_exists(connection, location):
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM fingerprints WHERE location_tag = ?', (location,))
    return cursor.fetchone()[0] > 0

#contructs and maintains fingeprints ordering according to FV ordering
def construct_fingerprint(connection):
    #global detected_aps

    create_fingerprint_db(connection)
    cursor = connection.cursor()

    exists = True
    while(exists):
      location = input("Enter Location tAG: ")
      exists = location_exists(connection, location)

    df = find_apsV3.detected_aps[['bssid', 'dBm_signal']]
    fingerprint_elements = df.set_index('bssid')['dBm_signal'].to_dict()


    query = 'SELECT DISTINCT bssid FROM fv_ordering ORDER BY id'
    bssids = pd.read_sql_query(query, connection)['bssid']

    fv_ordering_df = pd.DataFrame({'dBm_signal': ["?"] * len(bssids)}, index=bssids)
    fv_ordering = fv_ordering_df.to_dict()['dBm_signal']

    for key in  fingerprint_elements.keys():
      fv_ordering[key] = fingerprint_elements[key]

    #serilaize key:values for debuggin
    #serial_fingerprint = json.dumps(fv_ordering.values())
    #serial_fingerprint = json.dumps(fv_ordering.values())
    
    #serialize values: for degugging
    serial_fingerprint = ' '.join([str(val) for val in fv_ordering.values()])
    cursor = connection.cursor()
    cursor.execute('INSERT INTO fingerprints (location_tag, fingerprint) VALUES (?, ?)', (location, serial_fingerprint))
    connection.commit()

    print("\nDatabase Updated.")
