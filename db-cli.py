#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse, os, os.path

from app import db

APP_DATADIR = "/tmp/parallel-markets"
DB_FILEPATH = f"{APP_DATADIR}/app.db"


parser = argparse.ArgumentParser()
parser.add_argument(
    "-c", "--create",
    action="store_true",
    dest="create",
    default=False,
    help=f"create instance of SQLite DB at {DB_FILEPATH}, if it doesn't yet exist",
)
parser.add_argument(
    "-f", "--force",
    action="store_true",
    dest="force",
    default=False,
    help=f"can be used in combination with -c / --create to forcefully make a new database",
)
parser.add_argument(
    "-r", "--remove",
    action="store_true",
    dest="remove",
    default=False,
    help=f"remove SQLite DB file {DB_FILEPATH}, if it exists",
)
parser.add_argument(
    "-i", "--investors",
    action="store_true",
    dest="inspect_investors",
    default=False,
    help=f"check-out the contents of 'investor' table",
)
parser.add_argument(
    "-d", "--documents",
    action="store_true",
    dest="inspect_documents",
    default=False,
    help=f"check-out the contents of 'document' table",
)


def create_db(force: bool):
    if force:
        remove_db()

    if not os.path.isdir(APP_DATADIR):
        os.mkdir(APP_DATADIR)

    if not os.path.isfile(DB_FILEPATH):
        db.create_all()
        print(f"SQLite DB file created at: {DB_FILEPATH}")
    else:
        print(f"{DB_FILEPATH} DB file already exists")
        print(f"use -f / --force option to overwrite & recreate anew")

def remove_db():
    try:
        os.remove(DB_FILEPATH)
        print(f"DB file {DB_FILEPATH} successfully removed")
    except FileNotFoundError:
        print(f"DB file {DB_FILEPATH} does not exist")


def inspect_table(table_name):
    if os.path.isfile(DB_FILEPATH):
        import sqlite3
        con = sqlite3.connect(DB_FILEPATH)
        
        if table_name == "investor":
            sql_stmt = "SELECT * from investor;"
            table_header = "Investors"
        elif table_name == "document":
            sql_stmt = "SELECT i.fullname, d.filename from investor i INNER JOIN document d ON i.id=d.investor_id;"
            table_header = "Documents"
        else:
            assert False, "this should never be reached!"

        data = con.execute(sql_stmt).fetchall()
        print("-"*30, table_header, "-"*30)
        for d in data:
            print(d)
        print()
    else:
        print(f"{DB_FILEPATH} does not exist")
        print(f"use -c / --create to first create one, then upload investor info through web app")


if __name__ == "__main__":
    parsed_args = parser.parse_args()

    inspect_db = parsed_args.inspect_investors or parsed_args.inspect_documents
    if inspect_db:
        if parsed_args.inspect_investors:
            inspect_table("investor")
        if parsed_args.inspect_documents:
            inspect_table("document")
    elif parsed_args.create and parsed_args.remove:
        print("-c / --create & -r / --remove are mutually exclusive")
    elif parsed_args.create:
        create_db(parsed_args.force)
    elif parsed_args.remove:
        remove_db()
    else:
        inspect_table()
