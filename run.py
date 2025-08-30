import multiprocessing

# To run Jarvis
def startJarvis():
        from engine.db import dbs
        # print("Checking if the database has been made or not...")
        if dbs != 0:
            pass
        elif dbs == 0:
            dbs()
        from main import start
        start()

# To run hotword
def listenHotword():
        # print("Wisdom is running.")
        from engine.features import hotword
        hotword()

# Start both processes
if __name__ == '__main__':
        p1 = multiprocessing.Process(target=startJarvis)
        p2 = multiprocessing.Process(target=listenHotword)
        p1.start()
        p2.start()
        p1.join()

        if p2.is_alive():
            p2.terminate()
            p2.join()

        print("System stopped.")
