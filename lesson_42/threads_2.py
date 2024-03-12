import logging
import threading
import time

async def sleep_function():
    logging.info("Sleep start")
    time.sleep(5)
    logging.info("Sleep finish")


def hard_work_function():
    def fib(n):
        return n if n <= 1 else fib(n - 1) + fib(n - 2)

    logging.info("Hard work start")
    result = fib(34)
    logging.info(f"Hard work finish, result: {result}")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    target = sleep_function
    thread_count = 10

    logging.info("Main    : before running thread")
    threads = [threading.Thread(target=target) for i in range(thread_count)]
    for thread in threads:
        thread.start()

    logging.info("Main    : wait for the thread to finish")

    for thread in threads:
        thread.join()

    logging.info("Main    : all done")