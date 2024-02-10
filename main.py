import multiprocessing, server, disc

if __name__ == "__main__":
  multiprocessing.Process(target=disc.run).start()
  server.run()
