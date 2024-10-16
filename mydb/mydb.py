from .kv import Kv

import argparse
import sqlite3
import sys
import subprocess


class Command:
    def __init__(self):
        self.kv = Kv()

    def add(self, args):
        if args.value is None:
            print("Enter the value (end with Ctrl+D):")
            value = sys.stdin.buffer.read()

        try:
            self.kv.insert(args.key, value)
            self.kv.commit()
        except sqlite3.IntegrityError:
            if input("key is already exist. update it? (Y/n)") != "n":
                self.kv.update(args.key, args.value)
                self.kv.commit()

    def remove(self, args):
        self.kv.delete(args.key)
        self.kv.commit()

    def move(self, args):
        try:
            self.kv.move(args.fromKey, args.toKey)
        except sqlite3.IntegrityError:
            if input("destination key is already exist. overide it? (Y/n)") != "n":
                self.kv.delete(args.toKey)
                self.kv.move(args.fromKey, args.toKey)
        self.kv.commit()

    def get(self, args):
        result = self.kv.get(args.key)
        if result == None:
            print("data not found.")
            return
        if isinstance(result[0], bytes):
            if args.binary:
                sys.stdout.buffer.write(result[0])
            else:
                print(
                    "The data is binary and cannot be printed to the console. Use the --binary option to save it to a file."
                )
                if input("print anywhere (N/y)") == "y":
                    print(result[0])
        else:
            print(result[0])

    def search(self, args):
        results = self.kv.search_keys(args.pattern)
        if results:
            for key in results:
                print("- ", key)
        else:
            print("No keys found matching the pattern.")

    def checkUseRedirect(self):
        result = False
        try:
            useRedirect = self.kv.get("mydb.config.redirect")
            if useRedirect != None and useRedirect[0] == "true":
                sshTarget = self.kv.get("mydb.config.sshTarget")

                if sshTarget == None:
                    result = False
                else:
                    result = True
        except Exception as e:
            print("checkUseRedirect")
            print(e)
            result = False

        return result

    def redirect(self, args):
        try:
            useRedirect = self.kv.get("mydb.config.redirect")[0]
            sshTarget = self.kv.get("mydb.config.sshTarget")[0]

            newArgs = []
            for arg in args:
                if " " in arg:
                    arg = f'"{arg}"'
                newArgs.append(arg)

            sshCommand = (
                ["ssh"] + sshTarget.split(" ") + ["~/.local/bin/mydb"] + newArgs
            )

            if useRedirect == "true":
                sshproc = subprocess.Popen(
                    sshCommand, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr
                )
                sshproc.communicate()
        except Exception as e:
            print("command redirect failed as follow")
            print(e)

        pass


def main():

    command = Command()

    parser = argparse.ArgumentParser(description="mydb is onwen kv database")

    subparsers = parser.add_subparsers(dest="command", help="Choose what you want")

    # add command
    parser_add = subparsers.add_parser(
        "add", help="Add key-value pair", aliases=["insert", "put", "local_add"]
    )
    parser_add.add_argument("key", type=str, help="The key to add")
    parser_add.add_argument(
        "value",
        type=str,
        nargs="?",
        help="The value to add (optional, can be provided via stdin)",
    )
    parser_add.set_defaults(func=command.add)

    # rm command
    parser_remove = subparsers.add_parser(
        "remove", help="Delete key-value pair", aliases=["delete", "rm", "local_remove"]
    )
    parser_remove.add_argument("key", type=str, help="The key to remove")
    parser_remove.set_defaults(func=command.remove)

    # move command
    parser_move = subparsers.add_parser(
        "move", help="Move key to athore key", aliases=["replace", "mv", "local_move"]
    )
    parser_move.add_argument("fromKey", type=str, help="The key to move")
    parser_move.add_argument("toKey", type=str, help="The destination key to move")
    parser_move.set_defaults(func=command.move)

    # search command
    parser_search = subparsers.add_parser(
        "search", help="Search for keys matching a pattern", aliases=["find"]
    )
    parser_search.add_argument("pattern", type=str, help="The pattern to search for")
    parser_search.set_defaults(func=command.search)

    # get command
    parser_get = subparsers.add_parser(
        "get", help="Get key-value pair", aliases=["read", "local_get"]
    )
    parser_get.add_argument("key", type=str, help="The key to get")
    parser_get.add_argument(
        "--binary", action="store_true", help="Output binary data to a file"
    )
    parser_get.set_defaults(func=command.get)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        # redirect command over ssh if enabled
        if command.checkUseRedirect() == True and "local" not in args.command:
            command.redirect(sys.argv[1:])
        else:
            args.func(args)


if __name__ == "__main__":
    main()
