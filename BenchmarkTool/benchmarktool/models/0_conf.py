# coding: utf8
"""
Application static configuration
"""

"Database connection"
DB_USERNAME = '<username>'
DB_PASS = '<password>'
DB_ADDRESS = '<domain or IP>'
DB_NAME = '<database name>'

" Site config "
HOST_URL = 'http://<dns or ip>:8000/'
APPLICATION = "<application_name>/"

BENCHMARK_SCRIPT = "<full path and name of benchmark script (ex. /usr/local/share/pyheston/GetArgs.py)>"
FPGA_BENCHMARK_PATH = "<full path of the benchmark scripts for FPGA>"
FPGA_BENCHMARK_SCRIPT_ML = "<name of the multilevel script for FPGA simulations>"
FPGA_BENCHMARK_SCRIPT_SL = "<name of the singlelevel script for FPGA simulations>"

" E-mail configuration"
M_USERNAME = '<username>'
M_PASSWORD = '<password>'
M_SERVER = '<smtp server domain or ip>:<port>'
M_DOMAIN = '<e-mail domain>'
