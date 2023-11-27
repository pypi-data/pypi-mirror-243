import os
from InquirerPy.validator import NumberValidator
from application.core.enums import Actions
from InquirerPy import inquirer
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


class Utils:
    def __init__(self, conn):
        self.conn = conn

    @staticmethod
    def handler(signum, frame):
        print("User interrupted the process. Custom message here.")
        raise SystemExit

    @staticmethod
    def connect_db():
        try:
            db_uri = os.environ.get('SQLALCHEMY_DATABASE_URI')
            engine = create_engine(db_uri)
            conn = engine.connect()
            return conn
        except SQLAlchemyError as e:
            return None

    def table_exists(self, table_name):
        query = text("SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = :table_name)")
        result = self.conn.execute(query, {'table_name': table_name})
        return result.scalar()

    def column_exists(self, table_name, column_name):
        query = text("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.columns 
                WHERE table_name = :table_name AND column_name = :column_name
            );
        """)
        result = self.conn.execute(query, {'table_name': table_name, 'column_name': column_name})
        return result.scalar()

    def read_user_args(self):
        if self.conn is None:
            print("Please set up your database before using this tool.")
            print("Usage-Documentation: https://github.com/BurakTass/masking/blob/main/README.md")
            return

        action = inquirer.select(
            message="Select your action",
            choices=['delete', 'mask']
        ).execute()

        while True:
            table = inquirer.text(message="What's your table name?").execute()
            if Utils.table_exists(self, table):
                break
            else:
                print("Table does not exist. Please try again.")

        user_args = {
            'action': action,
            'table': table,
            'percentage': 0,
            'columns': [],
            'place_to_mask': None,
            'mask_type': 'regex'
        }

        if action == Actions.DELETE.value:
            percentage = inquirer.text(
                message="Enter the percentage of data to be deleted (0-100):",
                validate=NumberValidator(float_allowed=True, message="Please enter a valid number between 0 and 100."),
                filter=lambda value: float(value) if 0 <= float(value) <= 100 else 0,
                default="0"
            ).execute()
            user_args['percentage'] = percentage
        elif action == Actions.MASK.value:
            while True:
                columns = inquirer.text(
                    message="Enter the columns to be masked, separated by spaces:").execute().split()
                existing_columns = []
                missing_columns = []

                for col in columns:
                    if Utils.column_exists(self, table, col):
                        existing_columns.append(col)
                    else:
                        missing_columns.append(col)

                if missing_columns:
                    print(f"The following columns do not exist in the table: {', '.join(missing_columns)}")
                    retry = inquirer.confirm("Do you want to enter the columns again?").execute()
                    if not retry:
                        break
                else:
                    break
            mask_type = inquirer.select(
                message="Select your mask type",
                choices=['shuffle', 'regex', 'reverse', 'middle',
                         'start', 'end', 'random_char', 'nltk', 'random_character']
            ).execute()

            user_args['mask_type'] = mask_type
            user_args['columns'] = columns

        return user_args


