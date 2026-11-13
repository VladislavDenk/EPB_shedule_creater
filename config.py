import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.environ.get("name_db")

PATH_TO_FILE: str = Path(r"{}".format(os.environ.get("path_to_file")))

SENDER: str = os.environ.get("sender_email")
PASSWORD: str = os.environ.get("password_sender_email")
HOST: str = os.environ.get("smtp_server_mail")
PORT: int = int(os.environ.get("smtp_port_mail"))
MESSAGE = os.environ.get("message")

TEAMS_ROW = os.environ.get("teams", "")
TEAMS = [t.strip() for t in TEAMS_ROW.split(",") if t.strip()]

RECIPIENTS_SCL = os.environ.get("recipients_scl", "")
RECIPIENTS_GAZOIL = os.environ.get("recipients_gazoil", "")
RECIPIENTS_RAZVITIE = os.environ.get("recipients_razvitie", "")

INDEX_COLUMN_WITH_ADDRESSES = os.environ.get("index_column_with_addresses")
TITLE_COLUMN_WITH_ADDRESSES = os.environ.get("title_column_with_address")