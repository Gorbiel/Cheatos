import argparse
import argcomplete

from .utils import ensure_cheato_dir, get_version
from .completers import cheato_name_completer, tag_name_completer
from .commands import (
    add_cheato, edit_cheato, edit_tags, remove_cheato,
    list_cheatos, list_all_tags, show_cheato, rename_cheato
)
from .io import export_cheatos, import_cheatos, check_first_time


def main():
    """
    Entry point for the Cheatos CLI tool.

    This function sets up argument parsing, shell completion, and dispatches
    execution to the correct command based on user input.
    """
    ensure_cheato_dir()
    check_first_time()

    parser = argparse.ArgumentParser(description="Cheatos: Your terminal post-it notes manager")

    # Global --version flag
    parser.add_argument(
        "--version",
        action="version",
        version=f"cheatos v{get_version()}"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        metavar="<command>",
        title="Available commands"
    )

    # cheatos help — show this help message
    help_parser = subparsers.add_parser("help", help="Show help")

    # cheatos list [--tag TAG] — list all cheatos or filter by tag
    list_parser = subparsers.add_parser("list", help="List all cheatos")
    tag_arg = list_parser.add_argument("--tag", help="Filter by tag")
    tag_arg.completer = tag_name_completer

    # cheatos show NAME — display a single cheato
    show_parser = subparsers.add_parser("show", help="Show a cheato")
    name_arg = show_parser.add_argument("name")
    name_arg.completer = cheato_name_completer

    # cheatos add NAME — create a new cheato using $EDITOR
    add_parser = subparsers.add_parser("add", help="Add a new cheato")
    add_parser.add_argument("name")

    # cheatos edit NAME [--tags] — edit content or tags of a cheato
    edit_parser = subparsers.add_parser("edit", help="Edit a cheato")
    edit_name_arg = edit_parser.add_argument("name")
    edit_name_arg.completer = cheato_name_completer
    edit_parser.add_argument("--tags", action="store_true", help="Edit tags of a cheato")

    # cheatos remove NAME — delete a cheato
    rm_parser = subparsers.add_parser("remove", help="Remove a cheato")
    rm_name_arg = rm_parser.add_argument("name")
    rm_name_arg.completer = cheato_name_completer

    # cheatos rename OLD_NAME NEW_NAME — rename a cheato
    rename_parser = subparsers.add_parser("rename", help="Rename a cheato")
    old_arg = rename_parser.add_argument("old_name")
    old_arg.completer = cheato_name_completer
    rename_parser.add_argument("new_name")

    # cheatos tags — list all unique tags
    tags_parser = subparsers.add_parser("tags", help="List all unique tags")

    # cheatos export FILE_PATH — export all cheatos to a file
    export_parser = subparsers.add_parser("export", help="Export all cheatos")
    export_parser.add_argument("file_path", help="Output file path (.json or .bson)")

    # cheatos import FILE_PATH [--force] — import cheatos from a file
    import_parser = subparsers.add_parser("import", help="Import cheatos from file")
    import_parser.add_argument("file_path", help="Path to import file (.json or .bson)")
    import_parser.add_argument("--force", action="store_true", help="Overwrite existing cheatos")

    # Enable autocompletion
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    # Command dispatch
    if args.command == "list":
        list_cheatos(args.tag)
    elif args.command == "show":
        show_cheato(args.name)
    elif args.command == "add":
        add_cheato(args.name)
    elif args.command == "edit":
        if args.tags:
            edit_tags(args.name)
        else:
            edit_cheato(args.name)
    elif args.command == "remove":
        remove_cheato(args.name)
    elif args.command == "tags":
        list_all_tags()
    elif args.command == "rename":
        rename_cheato(args.old_name, args.new_name)
    elif args.command == "export":
        export_cheatos(args.file_path)
    elif args.command == "import":
        import_cheatos(args.file_path, force=args.force)
    elif args.command == "help":
        parser.print_help()
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    main()
