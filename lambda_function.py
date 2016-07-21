# Lambda function to pull Sydney weather from the BOM. 
# Used to pre-process the output so an Arduino doesn't have to parse the whole file.
# Simon Brown <github@t2kv.io>

from __future__ import print_function

import json
from ftplib import FTP
import datetime

retval = ""

print('Loading function')   

def parseFile(x):
    #print(x)
    if 'Sydney' in x: 
      daynames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
      (location,state,issue_date,issue_time,product_code,forecast_date,max_temp,forecast,blank) = x.split('#')
      (y, m, d) = ( int(forecast_date[0:4]) , int(forecast_date[4:6]) , int(forecast_date[6:8]) )
      weekday = daynames[datetime.date(y, m, d).weekday()]
      global retval
      retval = "%s: %s %s" % (weekday, max_temp, forecast)
      return retval

def lambda_handler(event, context):
    global retval
    from ftplib import FTP
    ftp = FTP('ftp2.bom.gov.au')
    ftp.login()
    ftp.cwd('anon/gen/fwo')
    ftp.retrlines("RETR IDA00100.dat", parseFile)
    ftp.quit()
    return retval
