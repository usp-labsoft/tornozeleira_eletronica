# coding=UTF-8

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ServidorApp.models import *
from ServidorApp.serializers import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.utils.six import BytesIO
from rest_framework.response import Response
from django.http import JsonResponse
from tasks import *
from celery.task.control import revoke

import json
import time
import urllib
import urllib2
import datetime



# Create your views here.
@csrf_exempt
def Servidor_Home(request):
	#print request.header
	#obj = User.objects.latest('id')
	#print obj.first_name
	#u = Connected_Mobiles(user_fk = obj, phone = "1178541234")
	#u.save()

	if request.method == 'POST':
		#instance = Arduinos_Time_Log.objects.get(id=12)
		#print instance.id
		#instance.delete()
		#Fazendo Parse Inicial para saber qual tipo de informaçao foi recebida
		json_data_received = json.loads(request.body)
		content = initialSerializer(json_data_received)
		content = JSONRenderer().render(content.data)

		stream = BytesIO(content)
		data = JSONParser().parse(stream)
		serializer = initialSerializer(data=data) #cria nova instância
		serializer.is_valid()
		type = serializer.validated_data.pop('type')

		#Se o tipo for 0, o POST veio de um arduino enviando seu status
		if type == 0:
			content = userSerializer(json_data_received)
			content = JSONRenderer().render(content.data)
			#print content
			stream = BytesIO(content)
			data = JSONParser().parse(stream)
			serializer = userSerializer(data=data) #cria nova instância
			serializer.is_valid()
			print serializer.validated_data

			fn = serializer.validated_data.pop('first_name')
			ln = serializer.validated_data.pop('last_name')
			cpf= serializer.validated_data.pop('cpf')
			lmax = serializer.validated_data.pop('lat_max')
			lmin = serializer.validated_data.pop('lat_min')
			lomax = serializer.validated_data.pop('long_max')
			lomin = serializer.validated_data.pop('long_min')
		
			#u = User(first_name=fn,last_name=ln,cpf=cpf,lat_max=lmax,lat_min=lmin,long_max=lomax,long_min=lomin)
			#u.save()

		#TIpo 1 indica que recebeu um log do Mobile
		elif type == 1:
			content = mobileLogSerializer(json_data_received)
			content = JSONRenderer().render(content.data)
			#print content
			stream = BytesIO(content)
			data = JSONParser().parse(stream)
			serializer = mobileLogSerializer(data=data) #cria nova instância
			serializer.is_valid()
			#print serializer.errors

			#print serializer.validated_data

			#Obtendo os dados enviados
			mobile_id = serializer.validated_data.pop('mobile_id')
			gps = serializer.validated_data.pop('gps')
			aux = gps.split(";")
			lati = float(aux[0])
			longi = float(aux[1])
			time = serializer.validated_data.pop('time')

			#Relacionado o mobile_log ao usuario correspondente
			user = User.objects.get(id=int(mobile_id))


			#Gerando pedindo de autorizaçao aleatorimamente
			auth = True #fazer random


			#Salva o Log gerado no BD
			obj = Connected_Mobiles.objects.get(id = mobile_id)
			mob = Mobile_Log(mobile_id_fk = obj, time = time, gps = gps, auth_required = auth)
			mob.save()

			#Gerar um token (id da task), enviar pro celular esse token e colocar numa lista
			#Ativar o timer assincrono
			#O celular manda request de novo com type = 2, e ele para o timer
			#Se um timer estourar, o celery indica que a task foi terminated, a partir disso dar um jeito de exibir essa informaçao (LOGGER??)
			if auth == True:
				t = timer.delay(user.id, mob.id)
				#print t.id
				None


			#Enviar post para celular pedindo pra ele se autenticar:	
			#data = json.dumps({"user_id":str(user_id),"mobile_log_id":str(mobile_log_id),"type":"4"})
			#print data
			#clen = len(data)
			#req = urllib2.Request('http://127.0.0.1:8000/', data, {'Content-Type': 'application/json', 'Content-Length': clen})
			#f = urllib2.urlopen(req)


			#Se o usuario saiu da area de cobertura, gerar um aviso:
			if lati >= user.lat_max or lati <= user.lat_min or longi >= user.long_max or longi <= user.long_min:
				print "Fora da área de cobertura"


		#Tipo 2 indica recebimento de Autenticaçao, portanto, o timer do background para
		elif type == 2:
			content = autSerializer(json_data_received)
			content = JSONRenderer().render(content.data)
			
			stream = BytesIO(content)
			data = JSONParser().parse(stream)
			serializer = autSerializer(data=data) #cria nova instância
			serializer.is_valid()
			
			mobile_log_id_fk = serializer.validated_data.pop('mobile_log_id_fk')
			time = serializer.validated_data.pop('time')
			gps = serializer.validated_data.pop('gps')
			aux = gps.split(";")
			lati = float(aux[0])
			longi = float(aux[1])
			valid = serializer.validated_data.pop('valid')
			type_aut = serializer.validated_data.pop('type_aut')
			task_id = serializer.validated_data.pop('task_id')

			moblog = Mobile_Log.objects.get(id=int(mobile_log_id_fk))
			mob = Connected_Mobiles.objects.get(id=moblog.id)
			user = mob.user_fk


			#Se o usuario saiu da area de cobertura, gerar um aviso:
			if lati >= user.lat_max or lati <= user.lat_min or longi >= user.long_max or longi <= user.long_min:
				print "Fora da área de cobertura"

			#Para o timer associado a essa autenticaçao
			try:
				revoke(str(task_id), terminate=True)
				#salva no DB
				auth = Authentication(log_id_fk=moblog,log_source="Mobile",time=time,gps=gps,type=type_aut,valid=valid)
				#auth.save()
				print "succeeded"
				

			except:
				#a autenticaçao chegou atrasada	e o timer estourou - DECIDIR O QUE FAZER					
				print "failed"

		#return JsonResponse(serializer.data)

		#Tipo 3 indica que o servidor recebeu Log de um arduino
		elif type == 3:
			#print "T"
			json_data_received = json.loads(request.body)
			content = arduinoLogSerializer(json_data_received)
			content = JSONRenderer().render(content.data)
			#print content

			stream = BytesIO(content)
			data = JSONParser().parse(stream)
			serializer = arduinoLogSerializer(data=data) #cria nova instância
			serializer.is_valid()

			arduino_id = serializer.validated_data.pop('arduino_id_fk')
			time = serializer.validated_data.pop('time')
			sensor_status = serializer.validated_data.pop('sensor_status')

			if sensor_status == False:
				#Enviar post para celular pedindo pra ele se autenticar:	
				#data = json.dumps({"user_id":str(user_id),"mobile_log_id":str(mobile_log_id),"type":"4"})
				#print data
				#clen = len(data)
				#req = urllib2.Request('http://127.0.0.1:8000/', data, {'Content-Type': 'application/json', 'Content-Length': clen})
				#f = urllib2.urlopen(req)
				None
			
			#Cria o log do arduino
			obj = Connected_Arduinos.objects.get(id = arduino_id)
			ard = Arduinos_Time_Log(arduino_id_fk=obj,time=time,sensor_status=sensor_status)
			ard.save()



		#Tipo 4 indica que o Servidor recebeu um alerta de TimeOut de autenticaçao de um usuario		
		elif type == 4:
			json_data_received = json.loads(request.body)
			content = timeoutSerializer(json_data_received)
			content = JSONRenderer().render(content.data)

			stream = BytesIO(content)
			data = JSONParser().parse(stream)
			serializer = timeoutSerializer(data=data) #cria nova instância
			serializer.is_valid()

			user_id = serializer.validated_data.pop('user_id')
			mobile_log_id = serializer.validated_data.pop('mobile_log_id')

			print "ALERTA DE TIME OUT: USUARIO " + str(user_id)

		#Tipo 5 indica que foi agendado uma verificaçao do status dos arduinos
		elif type == 5:
			print "YAS"
			c = add.delay(2,3)


	return render(request, 'ServidorApp/Servidor_Home.html', {})