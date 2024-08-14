import multiprocessing

bind = "localhost:8889"

workers = multiprocessing.cpu_count()*2 + 1
worker_class = 'tornado'
max_reuqests = 1000

timeout = 90
keep_alive = 2
debug = True
