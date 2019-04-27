import os
import telnetlib
import re
import time
import configparser
from datetime import datetime
import cqrmysql


CFG = configparser.ConfigParser()
CFG.read(os.path.expanduser(os.path.dirname(__file__) + '/cluster.cfg'))
MYSQL_HOST  = CFG.get('CLUSTER', 'mysql_host')
MYSQL_PORT  = CFG.get('CLUSTER', 'mysql_port')
MYSQL_USER  = CFG.get('CLUSTER', 'mysql_user')
MYSQL_PASS  = CFG.get('CLUSTER', 'mysql_pass')
MYSQL_DB    = CFG.get('CLUSTER', 'mysql_db')

database = cqrmysql.cqrmysql(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
modes = database.get_modes()
clusters = database.get_clusters()


# source: https://www.la1k.no/2017/11/01/parsing-a-dx-cluster-using-python-and-club-log/
# Open connection to telnet
cluster_id = 6
owncall = clusters[cluster_id]["CALL"] + "\n"
password = clusters[cluster_id]["PASS"] + "\n"
remote_host = clusters[cluster_id]["HOST"]
remote_port = clusters[cluster_id]["PORT"]
tn = telnetlib.Telnet(remote_host, remote_port)
print("connected")
time.sleep(1)
tn.write(owncall.encode('utf-8'))
if password:
    print("entering password")
    time.sleep(1)
    tn.write(password.encode('utf-8'))
print("logged in")
# Define regular expressions
# callsign pattern that matches also skimmer-calls
de_callsign_pattern = "([a-z|0-9|/|#|-]+)"
# classical callsign pattern
dx_callsign_pattern = "([a-z|0-9|/]+)"
frequency_pattern = "([0-9|.]+)"
mode_pattern = "([a-z|0-9]+)"
db_pattern = "([0-9]+)"
speedstring_pattern = "([WPM|BPS])"
cluster_pattern = re.compile("^DX de "+de_callsign_pattern+":\s+"+frequency_pattern+"\s+"+dx_callsign_pattern+"\s+(.*)\s+(\d{4}Z)", re.IGNORECASE)

# RBN
# DX de LZ7AA-#:    7047.1  OE/PE1NYQ      RTTY  15 dB  45 BPS  CQ      1814Z
rbn_pattern = re.compile("^DX de "+de_callsign_pattern+":\s+"+frequency_pattern+"\s*"+dx_callsign_pattern+"\s+"+mode_pattern+"\s+"+db_pattern+" dB\s+"+db_pattern+"(.*)\s+(\d{4}Z)", re.IGNORECASE)

# alternative RBN pattern that excludes skimmer suffix in de calls
# rbn_pattern = re.compile("^DX de "+callsign_pattern+"-[1-9|-]*#:\s+"+frequency_pattern+"\s+"+callsign_pattern+"\s+"+mode_pattern+"\s+"+db_pattern+" dB\s+"+db_pattern+"(.*)\s+(\d{4}Z)", re.IGNORECASE)
# Parse telnet
while (1):
    # Check new telnet info against regular expression
    telnet_output = tn.read_until(b'\n').decode('utf-8')
    #telnet_output = tn.read_eager()
    print(telnet_output)
    rbnmatch = rbn_pattern.match(telnet_output)
    clustermatch = cluster_pattern.match(telnet_output)
    # If there is a match, sort matches into variables
    if rbnmatch:
        de_call = rbnmatch.group(1)
        qrg = float(rbnmatch.group(2))
        dx_call = rbnmatch.group(3)
        mode = modes[rbnmatch.group(4).strip()]
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
            database.mysql_cursor.execute(sql)
            # Commit your changes in the database
            database.mysql_conn.commit()
        except:
            # Rollback in case there is any error
            database.mysql_conn.rollback()



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