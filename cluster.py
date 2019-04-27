import telnetlib
import time
import re
import cqr

class cluster:

    def __init__(self, database, cluster_list, mode_list, band_data):
        self.clusters = cluster_list
        self.database = database
        self.modes = mode_list
        self.band_data = band_data
        self.helper = cqr.helper(mode_list, band_data)
        
        # Define regular expressions

        # callsign pattern that matches also skimmer-calls
        de_callsign_pattern = "([a-z|0-9|/|#|-]+)"
        # classical callsign pattern
        dx_callsign_pattern = "([a-z|0-9|/]+)"
        frequency_pattern = "([0-9|.]+)"
        mode_pattern = "([a-z|0-9]+)"
        db_pattern = "([0-9]+)"
        self.cluster_pattern = re.compile("^DX de "+de_callsign_pattern+":\s+"+frequency_pattern+"\s+"+dx_callsign_pattern+"\s+(.*)\s+(\d{4}Z)", re.IGNORECASE)
        # RBN
        # DX de LZ7AA-#:    7047.1  OE/PE1NYQ      RTTY  15 dB  45 BPS  CQ      1814Z
        self.rbn_pattern = re.compile("^DX de "+de_callsign_pattern+":\s+"+frequency_pattern+"\s*"+dx_callsign_pattern+"\s+"+mode_pattern+"\s+"+db_pattern+" dB\s+"+db_pattern+"(.*)\s+(\d{4}Z)", re.IGNORECASE)
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
            telnet_output = tn.read_until(b'\n').decode('utf-8')
            rbnmatch = self.rbn_pattern.match(telnet_output)
            clustermatch = self.cluster_pattern.match(telnet_output)
            de_call = None
            qrg = None
            dx_call = None
            mode_id = None 
            comment = None
            speed = None
            db = None
            spot_time = None
            band_id = None
            
            if rbnmatch:
                de_call = rbnmatch.group(1)
                qrg = float(rbnmatch.group(2))
                dx_call = rbnmatch.group(3)
                mode_id = self.modes[rbnmatch.group(4).strip()]
                db = int(rbnmatch.group(5))
                speed = int(rbnmatch.group(6))
                spot_time_string = rbnmatch.group(8)
                spot_time = "{}:{}".format(spot_time_string[0:2], spot_time_string[2:4])
                band = self.helper.freq_to_band(qrg/1000)
                band_id = band["ID"]
                print("de:{} qrg:{} dx_call:{} mode:{} db:{} speed{}: time:{}".format(de_call, qrg, dx_call, mode_id, db, speed, spot_time))
                self.database.add_cluster_entry(de_call, qrg, band_id, dx_call, mode_id, comment, speed, db, spot_time, cluster_id)



            elif clustermatch:
                print(telnet_output)
                de_call = clustermatch.group(1)
                qrg = float(clustermatch.group(2))
                dx_call = clustermatch.group(3)
                comment = clustermatch.group(4).strip()
                spot_time_string = clustermatch.group(5)
                spot_time = "{}:{}".format(spot_time_string[0:2], spot_time_string[2:4])
                mode_id = self.helper.freq_to_mode(qrg/1000)
                band = self.helper.freq_to_band(qrg/1000)
                band_id = band["ID"]
                print("de:{} qrg:{} dx_call:{} comment:{} time:{}".format(de_call, qrg, dx_call, comment, spot_time))
                self.database.add_cluster_entry(de_call, qrg, band_id, dx_call, mode_id, comment, speed, db, spot_time, cluster_id)
            else:
                print(telnet_output)
            