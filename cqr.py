import pymysql
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
            print ("Error: unable to fetch data")

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
            print ("Error: unable to fetch data")
    def __del__(self):
        self.mysql_conn.close()