import os
import time

ts = time.strftime("%d%m%Y%H%S%M")

log_path = 'loggingbfs'
if not os.path.exists(log_path):
    os.mkdir(log_path)
log = open(f'{log_path}/bfs-{ts}.txt', 'w', encoding='utf-8')


def logging(text):
    log.write(text + "\n")


def close_log():
    log.close()
