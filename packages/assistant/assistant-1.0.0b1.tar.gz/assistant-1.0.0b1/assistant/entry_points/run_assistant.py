import sys
# import asyncio

from assistant.main import main

def run():
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(1)

if __name__ == '__main__':
    run()