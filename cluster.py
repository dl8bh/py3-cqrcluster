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
        self.dxcc_resolution = False
        # Define regular expressions

        # callsign pattern that matches also skimmer-calls
        de_callsign_pattern = "([a-z|0-9|/|#|-]+)"
        # classical callsign pattern
        dx_callsign_pattern = "([a-z|0-9|/]+)"
        frequency_pattern = "([0-9|.]+)"
        mode_pattern_list = ''
        for mode in mode_list:
            mode_pattern_list +=  mode + "|"
        mode_pattern = '(' + mode_pattern_list[:-1] + ')'
        db_pattern = "([0-9]+)"
        self.cluster_pattern = re.compile("^DX de "+dx_callsign_pattern+":\s+"+frequency_pattern+"\s+"+dx_callsign_pattern+"\s+(.*)\s+(\d{4}Z)", re.IGNORECASE)
        # RBN
        # DX de LZ7AA-#:    7047.1  OE/PE1NYQ      RTTY  15 dB  45 BPS  CQ      1814Z
        # 
        self.rbn_pattern = re.compile("^DX de "+de_callsign_pattern+":\s+"+frequency_pattern+"\s*"+dx_callsign_pattern+"\s+"+mode_pattern+"\s+"+db_pattern+" dB\s+"+db_pattern+"(.*)\s+(\d{4}Z)", re.IGNORECASE)
        self.cc_data_pattern = re.compile("^DX de "+de_callsign_pattern+":\s+"+frequency_pattern+"\s*"+dx_callsign_pattern+"\s+"+mode_pattern+"\s+"+db_pattern+" dB\s+(.*)\s+(\d{4}Z)", re.IGNORECASE)
        # alternative RBN pattern that excludes skimmer suffix in de calls
        # rbn_pattern = re.compile("^DX de "+callsign_pattern+"-[1-9|-]*#:\s+"+frequency_pattern+"\s+"+callsign_pattern+"\s+"+mode_pattern+"\s+"+db_pattern+" dB\s+"+db_pattern+"(.*)\s+(\d{4}Z)", re.IGNORECASE)
    
    def enable_dxcc_resolution(self, CTYFILES_PATH, CTYFILES_URL, AUTOFETCH_FILES):
        from pydxcc import dxcc
        self.dxcc_resolver = dxcc(CTYFILES_PATH, CTYFILES_URL, AUTOFETCH_FILES)
        self.dxcc_resolution = True

    def connect(self, cluster_id):
        owncall = self.clusters[cluster_id]["CALL"] + "\n"
        password = self.clusters[cluster_id]["PASS"] + "\n"
        remote_host = self.clusters[cluster_id]["HOST"]
        remote_port = self.clusters[cluster_id]["PORT"]
        self.tn = telnetlib.Telnet(remote_host, remote_port)
        self.cluster_id = cluster_id
        print("connected")
        time.sleep(1)
        self.tn.write(owncall.encode('latin-1'))
        if password:
            print("entering password")
            time.sleep(1)
            self.tn.write(password.encode('latin-1'))
        print("logged in")
        # Parse telnet

    def run(self):
        while (1):
            try:
                telnet_output = self.tn.read_until(b'\n').decode('latin-1')
            except TimeoutError:
                print("Reconnecting")
                self.connect(self.cluster_id)
                continue
            rbnmatch = self.rbn_pattern.match(telnet_output)
            cc_datamatch = self.cc_data_pattern.match(telnet_output)
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
            print("\n\n")
            if rbnmatch:
                print("SKIMMER: " + telnet_output)
                de_call = rbnmatch.group(1)
                qrg = float(rbnmatch.group(2))
                dx_call = rbnmatch.group(3)
                if self.dxcc_resolution:
                    adif = self.dxcc_resolver.call2dxcc(dx_call)[1]["adif"]
                else:
                    adif = None
                mode_id = self.modes[rbnmatch.group(4).strip()]
                db = int(rbnmatch.group(5))
                speed = int(rbnmatch.group(6))
                spot_time_string = rbnmatch.group(8)
                spot_time = "{}:{}".format(spot_time_string[0:2], spot_time_string[2:4])
                band = self.helper.freq_to_band(qrg/1000)
                if not band:
                    band_id = None
                else:
                    band_id = band["ID"]
                print("de:{} qrg:{} dx_call:{} adif:{} mode:{} db:{} speed:{} time:{}".format(de_call, qrg, dx_call, adif, mode_id, db, speed, spot_time))
                self.database.add_cluster_entry(de_call, qrg, band_id, dx_call, adif, mode_id, comment, speed, db, spot_time, True, self.cluster_id)

            elif cc_datamatch:
                print("CC_DATA: " + telnet_output)
                de_call = cc_datamatch.group(1)
                qrg = float(cc_datamatch.group(2))
                dx_call = cc_datamatch.group(3)
                if self.dxcc_resolution:
                    adif = self.dxcc_resolver.call2dxcc(dx_call)[1]["adif"]
                else:
                    adif = None
                mode_id = self.modes[cc_datamatch.group(4).strip()]
                db = int(cc_datamatch.group(5))
                spot_time_string = cc_datamatch.group(7)
                spot_time = "{}:{}".format(spot_time_string[0:2], spot_time_string[2:4])
                band = self.helper.freq_to_band(qrg/1000)
                if not band:
                    band_id = None
                else:
                    band_id = band["ID"]
                print("NOSPEED de:{} qrg:{} dx_call:{} adif:{} mode:{} db:{} speed:{} time:{}".format(de_call, qrg, dx_call, adif, mode_id, db, speed, spot_time))
                self.database.add_cluster_entry(de_call, qrg, band_id, dx_call, adif, mode_id, comment, speed, db, spot_time, True, self.cluster_id)

            elif clustermatch:
                print("CLUSTER: " + telnet_output)
                de_call = clustermatch.group(1)
                qrg = float(clustermatch.group(2))
                dx_call = clustermatch.group(3)
                if self.dxcc_resolution:
                    adif = self.dxcc_resolver.call2dxcc(dx_call)[1]["adif"]
                else:
                    adif = None
                comment = clustermatch.group(4).strip()
                spot_time_string = clustermatch.group(5)
                spot_time = "{}:{}".format(spot_time_string[0:2], spot_time_string[2:4])
                mode_id = self.helper.freq_to_mode(qrg/1000)
                band = self.helper.freq_to_band(qrg/1000)
                if not band:
                    band_id = None
                else:
                    band_id = band["ID"]
                print("CLUSTER: de:{} qrg:{} dx_call:{} adif:{} comment:{} time:{}".format(de_call, qrg, dx_call, adif, comment, spot_time))
                self.database.add_cluster_entry(de_call, qrg, band_id, dx_call, adif, mode_id, comment, speed, db, spot_time, False, self.cluster_id)
            else:
                print("NOMATCH: " + telnet_output)
            