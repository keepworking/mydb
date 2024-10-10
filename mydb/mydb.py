from .kv import Kv

import argparse
import sqlite3


class Command:
    def __init__(self):
        self.kv = Kv()

    def add(self, args):
        try:
            self.kv.insert(args.key, args.value)
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
        print(result[0])


def main():

    command = Command()

    parser = argparse.ArgumentParser(description="mydb is onwen kv database")

    subparsers = parser.add_subparsers(dest="command", help="Choose what you want")

    # add command
    parser_add = subparsers.add_parser(
        "add", help="Add key-value pair", aliases=["insert", "put"]
    )
    parser_add.add_argument("key", type=str, help="The key to add")
    parser_add.add_argument("value", type=str, help="The value to add")
    parser_add.set_defaults(func=command.add)

    # rm command
    parser_remove = subparsers.add_parser(
        "remove", help="Delete key-value pair", aliases=["delete", "rm"]
    )
    parser_remove.add_argument("key", type=str, help="The key to remove")
    parser_remove.set_defaults(func=command.remove)

    # move command
    parser_move = subparsers.add_parser(
        "move", help="Move key to athore key", aliases=["replace", "mv"]
    )
    parser_move.add_argument("fromKey", type=str, help="The key to move")
    parser_move.add_argument("toKey", type=str, help="The destination key to move")
    parser_move.set_defaults(func=command.move)

    # get command
    parser_get = subparsers.add_parser(
        "get", help="Get key-value pair", aliases=["read"]
    )
    parser_get.add_argument("key", type=str, help="The key to get")
    parser_get.set_defaults(func=command.get)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()
