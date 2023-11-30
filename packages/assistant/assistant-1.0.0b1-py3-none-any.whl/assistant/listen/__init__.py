import os, sys

from assistant import HOME

def enable_service_now(version = False):
    if not os.path.isfile("/usr/lib/systemd/user/assistant.listen.service"):
        print("No listen service present.")
        print("To download it type:")
        print("    wget https://gitlab.com/waser-technologies/technologies/assistant/-/raw/main/assistant.listen.service.example")
        print("    mv assistant.listen.service.example /usr/lib/systemd/user/assistant.listen.service")

    if not any([
        os.path.exists(f"{HOME}/.config/systemd/user/default.target.wants/assistant.listen.service"),
        os.path.exists("/usr/lib/systemd/user/default.target.wants/assistant.listen.service"),
    ]):       
        print("Listen STT service for Assistant is disabled.")
        print("To enable it type:")
        print(f"systemctl --user enable --now dmt listen assistant")
        print(f"systemctl --user enable --now assistant.listen")


if __name__ == '__main__':
    from assistant.listen.main import main
    try:
        main()
    except KeyboardInterrupt:
        exit(1)
