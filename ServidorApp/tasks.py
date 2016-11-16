# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
import json
import urllib
import urllib2



@shared_task
def timer(user_id, mobile_log_id):
	mins = 0
	while mins != 1:
	    #print ">>>>>>>>>>>>>>>>>>>>>", mins
	    # Sleep for a minute
	    time.sleep(60)
	    # Increment the minute total
	    mins += 1

	#Enviar POST REQUEST para o servidor, indicando que houve um Timeout
	data = json.dumps({"user_id":str(user_id),"mobile_log_id":str(mobile_log_id),"type":"4"})
	print data
	clen = len(data)
	req = urllib2.Request('http://127.0.0.1:8000/', data, {'Content-Type': 'application/json', 'Content-Length': clen})
	f = urllib2.urlopen(req)