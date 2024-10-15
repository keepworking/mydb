# MyDB Command-Line Tool

MyDB is a command-line key-value database application that allows you to perform various operations on a local SQLite database. It provides commands to add, remove, move, get, and search for key-value pairs.

## Installation

To install MyDB, clone the repository and navigate to the project directory. Then, run the following command to install the necessary dependencies:

```bash
pip install -r requirements.txt
```

## Usage

The MyDB tool provides several commands to interact with the database. Below are the available commands and their descriptions:

### Add a Key-Value Pair

To add a key-value pair to the database, use the `add` command:

```bash
mydb add <key> <value>
```

You can also provide the value via standard input:

```bash
echo "value" | mydb add <key>
```

### Remove a Key-Value Pair

To remove a key-value pair from the database, use the `remove` command:

```bash
mydb remove <key>
```

### Move a Key to Another Key

To move a key to another key, use the `move` command:

```bash
mydb move <fromKey> <toKey>
```

### Get a Key-Value Pair

To retrieve a value for a given key, use the `get` command:

```bash
mydb get <key>
```

If the value is binary, use the `--binary` option to output it to a file:

```bash
mydb get <key> --binary
```

### Search for Keys

To search for keys matching a pattern, use the `search` command:

```bash
mydb search <pattern>
```

## SSH Redirection

MyDB supports command redirection over SSH if configured. To enable this feature, set the `mydb.config.redirect` key to `true` and specify the SSH target in `mydb.config.sshTarget`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
