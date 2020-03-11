import os
import time

ts = time.strftime("%d%m%Y-%H%S%M")

log_path = 'logging'
if not os.path.exists(log_path):
    os.mkdir(log_path)
log = open(f'{log_path}/bfs-{ts}.txt', 'w', encoding='utf-8')


def write_log(text):
    pass
    # global log
    # log.write(text + "\n")


def close_log():
    pass
    # global log
    # log.close()
