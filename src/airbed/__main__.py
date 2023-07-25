import sys

from airbed.platform.worker import Worker


def main():
    runner = None
    worker = Worker(runner)
    worker.start()

if __name__ == "__main__":
    sys.exit(main())
