import sqlite3
import warnings
import sys

from process_aps import update_fv, construct_fingerprint, detected_aps
from find_aps import detect_aps

# Suppress all warnings
warnings.filterwarnings("ignore")




if __name__ == "__main__":

    #Redirect the standard output to the file
    with open('out.txt', 'w') as file:
   
        sys.stdout = file

        db = "devdb.db"
        # connection = sqlite3.connect(db)
        detect_aps()
        #print(detected_aps)
        #for _ in range(1,100):
        #    print("Done")
        #update_fv(connection)
        #construct_fingerprint(connection)

        #connection.close() """