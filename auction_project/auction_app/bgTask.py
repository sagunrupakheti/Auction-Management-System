import datetime

import schedule
from schedule import Scheduler
import threading
import time

from .models import *

def checkTime():
    auction = Auction.objects.all().filter(auction_status='Live') | Auction.objects.all().filter(auction_status='Advanced Bidding')
    for a in auction:
        if a.auction_date < date.today():
           Auction.objects.all().filter(auction_id= a.auction_id).update(auction_status='Expired')

def checkAdvanced():
    auction = Auction.objects.all().filter(auction_status='Advanced Bidding')
    for a in auction:
        if a.auction_date == date.today():
            Auction.objects.all().filter(auction_id= a.auction_id).update(auction_status='Live')



def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run

Scheduler.run_continuously = run_continuously

def start_scheduler():
    scheduler = Scheduler()
    scheduler.run_continuously()
    scheduler.every(10).seconds.do(checkTime)
    scheduler.every(10).seconds.do(checkAdvanced)



