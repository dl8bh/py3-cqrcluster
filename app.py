import os
import telnetlib
import re
import time
import configparser
from datetime import datetime
from cqr import cqrmysql
from cluster import cluster


CFG = configparser.ConfigParser()
CFG.read(os.path.expanduser(os.path.dirname(__file__) + '/cluster.cfg'))
MYSQL_HOST  = CFG.get('CLUSTER', 'mysql_host')
MYSQL_PORT  = CFG.get('CLUSTER', 'mysql_port')
MYSQL_USER  = CFG.get('CLUSTER', 'mysql_user')
MYSQL_PASS  = CFG.get('CLUSTER', 'mysql_pass')
MYSQL_DB    = CFG.get('CLUSTER', 'mysql_db')

database = cqrmysql(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
mode_list = database.get_modes()
cluster_list = database.get_clusters()


# source: https://www.la1k.no/2017/11/01/parsing-a-dx-cluster-using-python-and-club-log/
# Open connection to telnet
cluster_id = 6
dxc = cluster(database, cluster_list, mode_list)
dxc.connect(6)