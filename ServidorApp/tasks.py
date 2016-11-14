# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def timer():
	mins = 0
	while mins != 1:
	    #print ">>>>>>>>>>>>>>>>>>>>>", mins
	    # Sleep for a minute
	    time.sleep(60)
	    # Increment the minute total
	    mins += 1
	print "Finished"