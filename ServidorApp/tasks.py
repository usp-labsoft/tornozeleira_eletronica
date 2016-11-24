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
def checkFaults():
	#String que sera retornada ao server. Contem os ids dos arduinos com problema
	faulty_ard = ""
	all_arduinos = Connected_Arduinos.objects.all()

	for arduino in all_arduinos:

		try:
			log = Arduinos_Time_Log.objects.filter(arduino_id_fk=arduino).order_by('-time')
			diff = timeManipulation(log[0].time)
			#print diff

			#Se a diferença entre o ultimo log enviado e o tempo atual for maior que 1h significa que o arduino deixou de enviar os logs periodicos -> defeito
			if diff > datetime.timedelta(minutes = 16):
				faulty_ard += str(arduino.id) + " "
				#print "faultyard"
		except:
			print "Nao ha log do arduino de id " + str(arduino.id)

		
	faulty_mob = ""
	all_mobiles = Connected_Mobiles.objects.all()

	for mobile in all_mobiles:
		try:
			log = Mobile_Log.objects.filter(mobile_id_fk=mobile).order_by('-time')
			# print log[0].time
			# print str(datetime.datetime.now())
			diff = timeManipulation(log[0].time)

			#print diff

			#Se a diferença entre o ultimo log enviado e o tempo atual for maior que 1h significa que o arduino deixou de enviar os logs periodicos -> defeito
			if diff > datetime.timedelta(minutes = 6):
				faulty_mob += str(mobile.id) + " "
				#print "faultymob"
			else:
				None
				#print "notfaultymob"
		except:
			print "Nao ha log do mobile de id " + str(mobile.id)

	# print "faulty_ard:",
	# print str(faulty_ard)
	# print "faulty_mob:",
	# print str(faulty_mob)

	#Enviar POST REQUEST para o servidor, com uma lista de arduinos e de mobiles que pararam de responder
	data = json.dumps({"faulty_ard":faulty_ard,"faulty_mob":faulty_mob,"type":"6"})
	print data
	clen = len(data)
	req = urllib2.Request('http://127.0.0.1:8000/', data, {'Content-Type': 'application/json', 'Content-Length': clen})
	f = urllib2.urlopen(req)


def timeManipulation(ard_time):
	#Fazendo operaçoes em string com a data atual e a data do log para poder efetuar contas
	t1 = str(ard_time).split("+")
	t1 = t1[0].split(".")

	t2 = str(datetime.datetime.now()).split(".")

	t1 = t1[0]
	t2 = t2[0]

	#Formatando as datas para poder efetuar as contas
	a = datetime.datetime.strptime(str(t1), "%Y-%m-%d %H:%M:%S")
	b = datetime.datetime.strptime(str(t2), "%Y-%m-%d %H:%M:%S")
	offset = datetime.datetime.strptime("0:30:0","%H:%M:%S")

	diff = b-a
	# print "Log: " + str(a)
	# print "Now: " + str(b)
	# print "Dif: " + str(diff)
	
	return diff