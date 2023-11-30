from assistant.listen.main import main

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(1)