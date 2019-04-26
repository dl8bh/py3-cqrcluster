import telnetlib
import re
import time

# source: https://www.la1k.no/2017/11/01/parsing-a-dx-cluster-using-python-and-club-log/
# Open connection to telnet
#tn = telnetlib.Telnet("la3waa.ddns.net",8000)
tn = telnetlib.Telnet("telnet.reversebeacon.net",7000)
#tn.read_until("login: ")
#tn.write("dl8bh \n")
print("not logged in")
output = tn.read_until("Please enter your call: ")
print(output)
time.sleep(1)
tn.write("dl8bh\n")
tn.write("\n")
print("logged in")
# Define regular expressions
callsign_pattern = "([a-z|0-9|/|#|-]+)"
#callsign_pattern = "([a-z|0-9|/]+)"
frequency_pattern = "([0-9|.]+)"
mode_pattern = "([a-z|0-9]+)"
db_pattern = "([0-9]+)"
speedstring_pattern = "([WPM|BPS])"
cluster_pattern = re.compile("^DX de "+callsign_pattern+":\s+"+frequency_pattern+"\s+"+callsign_pattern+"\s+(.*)\s+(\d{4}Z)", re.IGNORECASE)
rbn_pattern = re.compile("^DX de "+callsign_pattern+"-[1-9|-]*#:\s+"+frequency_pattern+"\s+"+callsign_pattern+"\s+"+mode_pattern+"\s+"+db_pattern+" dB\s+"+db_pattern+"(.*)\s+(\d{4}Z)", re.IGNORECASE)
rbn_pattern = re.compile("^DX de "+callsign_pattern+":\s+"+frequency_pattern+"\s+"+callsign_pattern+"\s+"+mode_pattern+"\s+"+db_pattern+" dB\s+"+db_pattern+"(.*)\s+(\d{4}Z)", re.IGNORECASE)
#DX de LZ7AA-#:    7047.1  OE/PE1NYQ      RTTY  15 dB  45 BPS  CQ      1814Z
# Parse telnet
while (1):
    # Check new telnet info against regular expression
    telnet_output = tn.read_until("\n")
    print(telnet_output)
    match = rbn_pattern.match(telnet_output)
    # If there is a match, sort matches into variables
    if match:
        #print(telnet_output)
        spotter = match.group(1)
        frequency = float(match.group(2))
        spotted = match.group(3)
        comment = match.group(4).strip()
        spot_time = match.group(5)
        print(spotter)
        print(telnet_output)
    else:
        print(telnet_output)