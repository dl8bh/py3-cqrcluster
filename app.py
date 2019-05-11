import os
import telnetlib
import re
import time
import configparser
from datetime import datetime
import cqr
from cluster import cluster


CFG = configparser.ConfigParser()
CFG.read(os.path.expanduser(os.path.dirname(os.path.abspath(__file__)) + '/cluster.cfg'))
MYSQL_HOST  = CFG.get('CLUSTER', 'mysql_host')
MYSQL_PORT  = CFG.get('CLUSTER', 'mysql_port')
MYSQL_USER  = CFG.get('CLUSTER', 'mysql_user')
MYSQL_PASS  = CFG.get('CLUSTER', 'mysql_pass')
MYSQL_DB    = CFG.get('CLUSTER', 'mysql_db')

database = cqr.cqrmysql(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
mode_list = database.get_modes()
band_data = database.get_band_data()
cluster_list = database.get_clusters()


cluster_id = 5
dxc = cluster(database, cluster_list, mode_list, band_data)
dxc.connect(cluster_id)
dxc.run()