import process_aps
import find_apsV3
import make_map

import warnings
import sqlite3
import sys

# Suppress all warnings
warnings.filterwarnings("ignore")


if __name__ == "__main__":


    db = "devdb.db"
    connection = sqlite3.connect(db)

    #find_apsV3.detect_aps()
    #print(detected_aps)

    make_map.get_radio_map()
   
    process_aps.update_fv(connection)
    process_aps.construct_fingerprint(connection)

    connection.close()