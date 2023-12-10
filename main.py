import re

COMMANDS = {}

# PHONES = {
#     "Jhon": "1234567890",
#     "Billy": "987654321",
#     "Mary": "1029384756"
# }

PHONES = {}

EXIT_FLAG = False


def normalize_phone_no(phone):
    # phone number validity check
    if re.search(r"[^\d()\-+]", phone):
        raise ValueError("Incorrect phone number format")
    return re.sub(r"[()\-+]", "", phone)


def command_handler(command):
    def input_error(func):
        def wrapper(*args):
            try:
                return func(*args)
            except TypeError as err:
                return f"Incorrect input: {err}\n{help_command()}"
            except ValueError as err:
                return err

        commands = (command, ) if isinstance(command, str) else command
        for i in commands:
            COMMANDS[i] = wrapper

        return wrapper
    return input_error


@command_handler("help")
def help_command(*args):
    return "Usage: command [name] [phone number]\nlist - list all commands"


@command_handler("list")
def list_command(*args):
    return "\n".join(COMMANDS)


@command_handler("show all")
def show_all_command(*args):
    if not PHONES:
        raise ValueError("It's empty. There are no any records.")
    output = [f"{name}: {phone}" for name, phone in PHONES.items()]
    return "\n".join(output)


@command_handler(("good bye", "close", "exit", "."))
def exit_command(*args):
    global EXIT_FLAG
    EXIT_FLAG = True
    return "Good bye!"


@command_handler("hello")
def hello_command(*args):
    return "How can I help you?"


@command_handler("add")
def add_command(name, phone):
    phone = normalize_phone_no(phone)
    if PHONES.get(name):
        raise ValueError(f'Name "{name}" already exist')
    PHONES[name] = phone
    return f"New name {name} and phone number {phone} have been added"


@command_handler("remove")
def remove_command(name):
    if not PHONES.get(name):
        raise ValueError(f'Name "{name}" does not exist')
    PHONES.pop(name)
    return f"{name} phone number has been removed"


@command_handler("change")
def change_command(name, phone):
    phone = normalize_phone_no(phone)
    if not PHONES.get(name):
        raise ValueError(f'Name "{name}" does not exist')
    PHONES[name] = phone
    return f"{name} phone number has been changed to {phone}"


@command_handler("phone")
def phone_command(name):
    if not PHONES.get(name):
        raise ValueError(f'Name "{name}" does not exist')
    return f"{name}: {PHONES[name]}"


def main():
    while not EXIT_FLAG:
        input_string = input(">>> ")
        input_string = input_string.strip()

        # some workaround: adding space at the end of the string
        # need for correct detection of the command without args
        # will be further stripped
        input_string += " "

        command = None
        for check_command in COMMANDS:

            if input_string.lower().startswith(f"{check_command} "):
                command = check_command
                args = input_string[len(check_command):]

                # removing excess spaces
                args = args.strip()
                args = re.sub(r"\s+", " ", args)

                args = args.split(" ")
                break

        if command is None:
            print("No such command")
            continue

        print(COMMANDS[command](*args))


if __name__ == "__main__":
    main()
