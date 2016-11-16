from django.db import models

# Create your models here.

class User(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	cpf = models.CharField(max_length=11)
	lat_max = models.FloatField()
	lat_min = models.FloatField()
	long_max = models.FloatField()
	long_min = models.FloatField()

	#picture = models.ImageField()

    
class Connected_Arduinos(models.Model):
    user = models.ForeignKey(User)
 
class Arduinos_Time_Log(models.Model):
	arduino_id_fk = models.ForeignKey(Connected_Arduinos)
	time = models.DateField()
	sensor_status = models.BooleanField()

class Connected_Mobiles(models.Model):
	user_fk = models.ForeignKey(User)
	phone = models.CharField(max_length=50)

class Mobile_Log(models.Model):
	mobile_id_fk = models.ForeignKey(Connected_Mobiles) 
	time = models.DateField()
	gps = models.CharField(max_length=100)
	auth_required = models.BooleanField()
#class Authentication()

class Authentication(models.Model):
	log_id_fk = models.ForeignKey(Mobile_Log)
	log_source = models.CharField(max_length=100)
	time = models.DateField()
	gps = models.CharField(max_length=100)
	type = models.CharField(max_length=100)
	valid = models.BooleanField()