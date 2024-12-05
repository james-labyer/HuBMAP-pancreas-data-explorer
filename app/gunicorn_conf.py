import multiprocessing

# calculate number of workers
cores = multiprocessing.cpu_count()
num_workers = 2 * cores + 1

# Gunicorn config variables
worker_tmp_dir = "/dev/shm"
workers = num_workers
threads = 4
worker_class = "gthread"
log_file = "gunicorn_logs"
host = "0.0.0.0"
port = "8050"
loglevel = "info"
