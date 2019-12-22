import schedule
import time


def job():
    print("I'm working...")


schedule.every(10).minutes.do(job)
schedule.every().day.at("18:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)