import telnetlib
import time
import re
class entry:

    def __init__(self, de_call, qrg, dx_call, mode, comment, speed, db, clx_timestamp, source):
        pass

class cluster:

    def __init__(self, database, cluster_list, mode_list):
        self.clusters = cluster_list
        self.database = database
        self.modes = mode_list
        
        # Define regular expressions

        # callsign pattern that matches also skimmer-calls
        self.de_callsign_pattern = "([a-z|0-9|/|#|-]+)"
        # classical callsign pattern
        self.dx_callsign_pattern = "([a-z|0-9|/]+)"
        self.frequency_pattern = "([0-9|.]+)"
        self.mode_pattern = "([a-z|0-9]+)"
        self.db_pattern = "([0-9]+)"
        self.speedstring_pattern = "([WPM|BPS])"
        self.cluster_pattern = re.compile("^DX de "+self.de_callsign_pattern+":\s+"+self.frequency_pattern+"\s+"+self.dx_callsign_pattern+"\s+(.*)\s+(\d{4}Z)", re.IGNORECASE)
        # RBN
        # DX de LZ7AA-#:    7047.1  OE/PE1NYQ      RTTY  15 dB  45 BPS  CQ      1814Z
        self.rbn_pattern = re.compile("^DX de "+self.de_callsign_pattern+":\s+"+self.frequency_pattern+"\s*"+self.dx_callsign_pattern+"\s+"+self.mode_pattern+"\s+"+self.db_pattern+" dB\s+"+self.db_pattern+"(.*)\s+(\d{4}Z)", re.IGNORECASE)
        # alternative RBN pattern that excludes skimmer suffix in de calls
        # rbn_pattern = re.compile("^DX de "+callsign_pattern+"-[1-9|-]*#:\s+"+frequency_pattern+"\s+"+callsign_pattern+"\s+"+mode_pattern+"\s+"+db_pattern+" dB\s+"+db_pattern+"(.*)\s+(\d{4}Z)", re.IGNORECASE)
    def connect(self, cluster_id):
        owncall = self.clusters[cluster_id]["CALL"] + "\n"
        password = self.clusters[cluster_id]["PASS"] + "\n"
        remote_host = self.clusters[cluster_id]["HOST"]
        remote_port = self.clusters[cluster_id]["PORT"]
        tn = telnetlib.Telnet(remote_host, remote_port)
        print("connected")
        time.sleep(1)
        tn.write(owncall.encode('utf-8'))
        if password:
            print("entering password")
            time.sleep(1)
            tn.write(password.encode('utf-8'))
        print("logged in")
        # Parse telnet
        while (1):
            # Check new telnet info against regular expression
            telnet_output = tn.read_until(b'\n').decode('utf-8')
            #telnet_output = tn.read_eager()
            print(telnet_output)
            rbnmatch = self.rbn_pattern.match(telnet_output)
            clustermatch = self.cluster_pattern.match(telnet_output)
            # If there is a match, sort matches into variables
            if rbnmatch:
                de_call = rbnmatch.group(1)
                qrg = float(rbnmatch.group(2))
                dx_call = rbnmatch.group(3)
                mode = self.modes[rbnmatch.group(4).strip()]
                db = int(rbnmatch.group(5))
                speed = int(rbnmatch.group(6))
                spot_time_string = rbnmatch.group(8)
                spot_time = "{}:{}".format(spot_time_string[0:2], spot_time_string[2:4])
                #band = qrg_to_band(qrg)
                print("de:{} qrg:{} dx_call:{} mode:{} db:{} speed{}: time:{}".format(de_call, qrg, dx_call, mode, db, speed, spot_time))
                sql = "INSERT INTO cluster(de_call, qrg, dx_call, speed, db, clx_timestamp, mode_id, source) VALUES ('{}', {}, '{}', '{}', '{}', '{}', {}, {})".format(de_call, qrg, dx_call, speed, db, spot_time, mode, cluster_id)
                print(sql)
                try:
                    # Execute the SQL command
                    self.database.mysql_cursor.execute(sql)
                    # Commit your changes in the database
                    self.database.mysql_conn.commit()
                except:
                    # Rollback in case there is any error
                    self.database.mysql_conn.rollback()



            elif clustermatch:
                print(telnet_output)
                de_call = clustermatch.group(1)
                qrg = float(clustermatch.group(2))
                dx_call = clustermatch.group(3)
                comment = clustermatch.group(4).strip()
                spot_time = clustermatch.group(5)
                #band = qrg_to_band(qrg)
                print("de:{} qrg:{} dx_call:{} comment:{} time:{}".format(de_call, qrg, dx_call, comment, spot_time))
            else:
                pass