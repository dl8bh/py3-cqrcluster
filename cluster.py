import os
import telnetlib
import re
import time
import configparser
from datetime import datetime
import pymysql
import pprint


CFG = configparser.ConfigParser()
CFG.read(os.path.expanduser(os.path.dirname(__file__) + '/cluster.cfg'))
MYSQL_HOST  = CFG.get('CLUSTER', 'mysql_host')
MYSQL_PORT  = CFG.get('CLUSTER', 'mysql_port')
MYSQL_USER  = CFG.get('CLUSTER', 'mysql_user')
MYSQL_PASS  = CFG.get('CLUSTER', 'mysql_pass')
MYSQL_DB    = CFG.get('CLUSTER', 'mysql_db')

mysql_conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
mysql_cursor = mysql_conn.cursor()

def get_clusters():
    try:
   # Execute the SQL command
        mysql_cursor.execute("SELECT * FROM dxclusters")
        # Fetch all the rows in a list of lists.
        results = mysql_cursor.fetchall()
        pp = pprint.PrettyPrinter()
        pp.pprint(results)
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
        pp.pprint(clusters)
        return(clusters)
    except:
        print ("Error: unable to fetch data")

    

clusters = get_clusters()

def close_database_connection():
    mysql_conn.close()

# source: https://www.la1k.no/2017/11/01/parsing-a-dx-cluster-using-python-and-club-log/
# Open connection to telnet
owncall = clusters[6]["CALL"]
mode = "rbn"
remote_host = clusters[6]["HOST"]
remote_port = clusters[6]["PORT"]
loginstring=''
if mode == "rbn":
    expect_string = ('Please enter your call: ')
    login_string = '{}\n'.format(owncall)
elif mode == "cc":
    expect_string = ('login: ')
    login_string = '{} \n'.format(owncall)
tn = telnetlib.Telnet(remote_host, remote_port)
print("connected")
output = tn.read_until(expect_string.encode('utf-8'))
print(output)
time.sleep(1)
tn.write(login_string.encode('utf-8'))
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
        mode = rbnmatch.group(4).strip()
        db = int(rbnmatch.group(5))
        speed = int(rbnmatch.group(6))
        spot_time = rbnmatch.group(8)
        #band = qrg_to_band(qrg)
        print("de:{} qrg:{} dx_call:{} mode:{} db:{} speed{}: time:{}".format(de_call, qrg, dx_call, mode, db, speed, spot_time))
    elif clustermatch:
        print(telnet_output)
        de_call = clustermatch.group(1)
        qrg = float(clustermatch.group(2))
        dx_call = clustermatch.group(3)
        comment = clustermatch.group(4).strip()
        spot_time = clustermatch.group(5)
        #band = qrg_to_band(qrg)
        print("de:{} qrg:{} dx_call:{} mode:{} db:{} speed{}: time:{}".format(de_call, qrg, dx_call, mode, db, speed, spot_time))
    else:
        print(telnet_output)