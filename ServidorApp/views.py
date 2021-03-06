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
from django.http import HttpResponse

import json
import time
import urllib
import urllib2
import datetime



# Create your views here.
@csrf_exempt
def Servidor_Home(request):
	if request.method == 'POST':

		#Authentication.objects.all().delete()
		#Arduinos_Time_Log.objects.all().delete()

		#obj = User.objects.get(id=2)

		#print obj.first_name
		#c = Connected_Mobiles(user_fk = obj, phone = '222222222')
		#a = Connected_Arduinos(user_fk = obj)
		#a.save()
		#c.save()

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
			#print serializer.validated_data

			fn = serializer.validated_data.pop('first_name')
			ln = serializer.validated_data.pop('last_name')
			cpf= serializer.validated_data.pop('cpf')
			lmax = serializer.validated_data.pop('lat_max')
			lmin = serializer.validated_data.pop('lat_min')
			lomax = serializer.validated_data.pop('long_max')
			lomin = serializer.validated_data.pop('long_min')
		
			#u = User(first_name=fn,last_name=ln,cpf=cpf,lat_max=lmax,lat_min=lmin,long_max=lomax,long_min=lomin)
			#u.save()
			#c = Connected_Mobiles(user_fk = u, phone = '222222222')
			#a = Connected_Arduinos(user_fk = u)
			return HttpResponse('\nUsuario cadastrado com sucesso\n\n')

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
			obj = Connected_Mobiles.objects.get(id = mobile_id)
			user = obj.user_fk


			#Gerando pedindo de autorizaçao aleatorimamente
			auth = True #fazer random


			#Salva o Log gerado no BD
			mob = Mobile_Log(mobile_id_fk = obj, time = time, gps = gps)
			mob.save()
			
			#print mob.id
			#Gerar um token (id da task), enviar pro celular esse token e colocar numa lista
			#Ativar o timer assincrono
			#O celular manda request de novo com type = 2, e ele para o timer
			#Se um timer estourar, o celery indica que a task foi terminated, a partir disso dar um jeito de exibir essa informaçao (LOGGER??)
			if auth == True:
				#print "test"
				t = timer.delay(user.id, mob.id)
				print t.id
				None


			#Enviar post para celular pedindo pra ele se autenticar:	
			#data = json.dumps({"user_id":str(user_id),"mobile_log_id":str(mobile_log_id),"type":"4"})
			#print data
			#clen = len(data)
			#req = urllib2.Request('http://127.0.0.1:8000/', data, {'Content-Type': 'application/json', 'Content-Length': clen})
			#f = urllib2.urlopen(req)


			#Se o usuario saiu da area de cobertura, gerar um aviso:
			if lati >= user.lat_max or lati <= user.lat_min or longi >= user.long_max or longi <= user.long_min:
				print "Usuario: " + str(user.id) + " fora da área de cobertura"

			return HttpResponse('\nLog do Mobile cadastrado com sucesso\n\n')


		#Tipo 2 indica recebimento de Autenticaçao, portanto, o timer do background para
		elif type == 2:
			content = autSerializer(json_data_received)
			content = JSONRenderer().render(content.data)
			
			stream = BytesIO(content)
			data = JSONParser().parse(stream)
			serializer = autSerializer(data=data) #cria nova instância
			serializer.is_valid()

			mobile_id = serializer.validated_data.pop('mobile_id')
			time = serializer.validated_data.pop('time')
			gps = serializer.validated_data.pop('gps')
			aux = gps.split(";")
			lati = float(aux[0])
			longi = float(aux[1])
			valid = serializer.validated_data.pop('valid')
			type_aut = serializer.validated_data.pop('type_aut')
			task_id = serializer.validated_data.pop('task_id')

			mob = Connected_Mobiles.objects.get(id=mobile_id)
			#moblog = Mobile_Log.objects.filter(mobile_id_fk=mob).order_by('-time')
			#print moblog[0].id
			user = mob.user_fk



			#Se o usuario saiu da area de cobertura, gerar um aviso:
			if lati >= user.lat_max or lati <= user.lat_min or longi >= user.long_max or longi <= user.long_min:
				print "Usuario: " + str(user.id) + " fora da área de cobertura"

			#Para o timer associado a essa autenticaçao
			try:
				revoke(str(task_id), terminate=True)
				#salva no DB
				auth = Authentication(time=time,gps=gps,type=type_aut,valid=valid)
				auth.save()
				return HttpResponse('\nAutenticaçao realizada com sucesso\n\n')
			except:
				#a autenticaçao chegou atrasada	e o timer estourou - DECIDIR O QUE FAZER					
				print "Falha na Autenticaçao do usuario id: " + str(user.id)
				return HttpResponse('\Falha na autenticaçao, apesar de enviada, ela chegou atrasada e houve timeout\n\n')


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

			obj = Connected_Arduinos.objects.get(id = arduino_id)
			user = obj.user_fk
			mob = Connected_Mobiles.objects.get(user_fk=user)

			#print sensor_status

			if sensor_status == True:
				#Enviar post para celular pedindo pra ele se autenticar:	
				t = timer.delay(user.id, mob.id)
				print t.id
				#data = json.dumps({"user_id":str(user_id),"mobile_log_id":str(mobile_log_id),"type":"4"})
				#print data
				#clen = len(data)
				#req = urllib2.Request('http://127.0.0.1:8000/', data, {'Content-Type': 'application/json', 'Content-Length': clen})
				#f = urllib2.urlopen(req)
			
			#Cria o log do arduino
			obj = Connected_Arduinos.objects.get(id = arduino_id)
			ard = Arduinos_Time_Log(arduino_id_fk=obj,time=time,sensor_status=sensor_status)
			ard.save()

			return HttpResponse('\nLog de Arduino cadastrado com sucesso\n\n')


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
			#print "type5"
			c = checkFaults.delay()

		#Tipo 6 indica que a resposta da verificaçao chegou e recebe os ids dos arduinos e mobiles com defeito
		elif type == 6:
			json_data_received = json.loads(request.body)
			content = faultySerializer(json_data_received)
			content = JSONRenderer().render(content.data)

			stream = BytesIO(content)
			data = JSONParser().parse(stream)
			serializer = faultySerializer(data=data) #cria nova instância
			serializer.is_valid()

			faulty_ard = serializer.validated_data.pop('faulty_ard')
			faulty_mob = serializer.validated_data.pop('faulty_mob')

			print "Ids de mobiles defeituosos:",
			print faulty_mob
			print "Ids de arduinos defeituosos:",
			print faulty_ard

	return render(request, 'ServidorApp/Servidor_Home.html', {})