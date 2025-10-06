import schedule
import time
from main import main

def job():
    print("Menjalankan jadwal crawling...")
    main()

schedule.every(6).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
