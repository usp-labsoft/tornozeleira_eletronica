# coding=UTF-8
# Create your tasks here

from __future__ import absolute_import, unicode_literals
from django.db import models
from ServidorApp.models import *
from celery import shared_task
import time
import json
import urllib
import urllib2
import datetime

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


@shared_task
def add(x, y):
	#String que sera retornada ao server. Contem os ids dos arduinos com problema
	faulty_ard = ""
	obj = Arduinos_Time_Log.objects.latest('id')
	#print obj.id
	for id in range(1,obj.id+1):
		try:
			ard = Arduinos_Time_Log.objects.get(id=int(id))

			#Fazendo operaçoes em string com a data atual e a data do log para poder efetuar contas
			t1 = str(ard.time).split("+")
			t1 = t1[0].split(".")

			t2 = str(datetime.datetime.now()).split(".")

			t1 = t1[0]
			t2 = t2[0]

			#Formatando as datas para poder efetuar as contas
			a = datetime.datetime.strptime(str(t1), "%Y-%m-%d %H:%M:%S")
			b = datetime.datetime.strptime(str(t2), "%Y-%m-%d %H:%M:%S")
			offset = datetime.datetime.strptime("0:30:0","%H:%M:%S")

			diff = b-a
			print "Log: " + str(a)
			print "Now: " + str(b)
			print "Dif: " + str(diff)
			print "Off: " +str(offset)

			#Se a diferença entre o ultimo log enviado e o tempo atual for maior que 1h significa que o arduino deixou de enviar os logs periodicos -> defeito
			if diff > datetime.timedelta(minutes = 6):
				faulty_ard += str(ard.id) + " "
				print "AHA"



		except:	
			None	


	print str(faulty_ard)


	#Enviar POST REQUEST para o servidor, com uma lista de arduinos que pararam de responder
	# data = json.dumps({"user_id":str(user_id),"mobile_log_id":str(mobile_log_id),"type":"4"})
	# print data
	# clen = len(data)
	# req = urllib2.Request('http://127.0.0.1:8000/', data, {'Content-Type': 'application/json', 'Content-Length': clen})
	# f = urllib2.urlopen(req)

	return x + y