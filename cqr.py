import pymysql
from collections import OrderedDict
class cqrmysql:

    def __init__(self, MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB):
        self.mysql_conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
        self.mysql_cursor = self.mysql_conn.cursor()

    def get_clusters(self):
        try:
            # Execute the SQL command
            self.mysql_cursor.execute("SELECT * FROM dxclusters")
            # Fetch all the rows in a list of lists.
            results = self.mysql_cursor.fetchall()
            #pp = pprint.PrettyPrinter()
            #pp.pprint(results)
            clusters = dict()
            for row in results:
                cluster = {
                    "ID"    : row[0],
                    "NAME"  : row[1],
                    "HOST"  : row[2],
                    "PORT"  : row[3],
                    "CALL"  : row[4],
                    "PASS"  : row[5]
                }
                clusters[row[0]] = cluster
            #pp.pprint(clusters)
            return(clusters)
        except:
            print ("Error: unable to fetch cluster data")

    def get_modes(self):
        try:
            # Execute the SQL command
            self.mysql_cursor.execute("SELECT * FROM modes")
            # Fetch all the rows in a list of lists.
            results = self.mysql_cursor.fetchall()
            #pp = pprint.PrettyPrinter()
            #pp.pprint(results)
            modes = dict()
            for row in results:
                modes[row[1]] = row[0]
            #pp.pprint(modes)
            return(modes)
        except:
            print ("Error: unable to fetch mode data")
    
    def get_band_data(self):
        try:
            # Execute the SQL command
            self.mysql_cursor.execute("SELECT * FROM bands")
            # Fetch all the rows in a list of lists.
            results = self.mysql_cursor.fetchall()
            band_data = dict()
            for row in results:
                band = {
                    "ID"        : row[0],
                    "NAME"      : row[1],
                    "F_BEGIN"   : row[2],
                    "F_END"     : row[3],
                    "F_CW"      : row[4],
                    "F_RTTY"    : row[5],
                    "F_SSB"     : row[6]
                }
                band_data[row[0]] = band
            return(band_data)
        except:
            print ("Error: unable to fetch band data")
    
    def __del__(self):
        self.mysql_conn.close()

class helper:
    def __init__(self, mode_list, band_data):
        self.mode_list = mode_list
        self.band_data = band_data
    
    def freq_to_band(self, freq):
        for id in self.band_data:
            band = self.band_data[id]
            if band["F_BEGIN"] <= freq <= band["F_END"]:
                return(band)
        return(None)
        

    def freq_to_mode(self, freq):
        band = self.freq_to_band(freq)
        if freq <= band["F_CW"]:
            return(self.mode_list["CW"])
        elif band["F_SSB"] >= freq >= band["F_RTTY"]:
            return(self.mode_list["RTTY"])
        elif band["F_END"] >= freq >= band["F_SSB"]:
            return(self.mode_list["SSB"])
        else:
            return(None)
