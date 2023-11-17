import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'FTIUAJY'
HOMEPAGE = 'https://fti.uajy.ac.id/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
threadQueue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


#Membuat Worker thread

def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def work():
    while True:
        url = threadQueue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        threadQueue.task_done()


def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        threadQueue.put(link)
    threadQueue.join()
    crawl()


#Mengecek apakah ada link di queue.txt
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links))+' links in the queue')
        create_jobs()


create_workers()
crawl()

