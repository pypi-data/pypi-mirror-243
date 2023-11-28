import json
import random
import re
import signal
import string
from nltk.corpus import words
from sqlalchemy import text
from application.core.replace_utils import ReplaceUtils
from application.core.enums import Actions

patterns = {
            'tc': re.compile(r'\b(\d{4})[-.\s]?(\d{3})[-.\s]?(\d{4})\b'),
            'credit_card': re.compile(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})\b'),
            'email': re.compile(r'\b[A-Za-z0-9._*%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'phone': re.compile(r'\b(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})\b'),
            'password': re.compile(r'(\b[A-Za-z0-9_-]+:)\s*\b([A-Za-z0-9_-]+)\b'),
        }

replace_functions = {
                'email': ReplaceUtils.replace_email,
                'phone': ReplaceUtils.replace_phone_number,
                'tc': ReplaceUtils.replace_phone_number,
                'credit_card': ReplaceUtils.replace_credit_card_number,
                'password': ReplaceUtils.replace_password,
            }

word_list = []


class MaskUtils:
    def __init__(self, connection, args, chunk_size=500):
        self.connection = connection
        self.action = args['action']
        self.table = args['table']
        self.columns = args['columns']
        self.percentage = args['percentage']
        self.mask_type = args['mask_type']
        self.chunk_size = chunk_size
        self.masking_strategies = {
            Actions.REGEX_METHOD.value: self.mask_regex_text,
            Actions.SHUFFLE_METHOD.value: self.mask_shuffle_text,
            Actions.REVERSE_METHOD.value: self.mask_reverse_text,
            Actions.RANDOM_METHOD.value: self.mask_random_text,
            Actions.MIDDLE_MASK_CHAR_METHOD.value: self.mask_middle_text,
            Actions.START_METHOD.value: self.mask_start_text,
            Actions.END_METHOD.value: self.mask_end_text,
            Actions.NLTK_METHOD.value: self.randomize_text_length,
            Actions.MIDDLE_RANDOM_CHARACTER_METHOD.value: self.mask_middle_with_random_chars,
        }

    def check_mask_type(self):
        global word_list
        if self.mask_type == Actions.NLTK_METHOD.value:
            word_list = words.words()

    @staticmethod
    def handler(signum, frame):
        print("User interrupted the process. Custom message here.")
        raise SystemExit

    @staticmethod
    def mask_shuffle_text(text_data):
        if isinstance(text_data, str):
            char_list = list(text_data)
            index_list = list(range(len(char_list)))
            random.shuffle(index_list)
            new_text = ''.join(char_list[index] for index in index_list)
        else:
            new_text = text_data

        return new_text

    @staticmethod
    def mask_start_text(text_data):
        if isinstance(text_data, str):
            length = len(text_data)
            mask_length = int(length * (40 / 100.0))
            masked_part = Actions.MASK_CHAR.value * mask_length
            new_text = masked_part + text_data[mask_length:]
        else:
            new_text = text_data

        return new_text

    @staticmethod
    def mask_regex_text(text_data):
        new_text = text_data
        if isinstance(text_data, str):
            for pattern_name, pattern in patterns.items():
                replace_function = replace_functions.get(pattern_name, lambda x: x)
                new_text = pattern.sub(replace_function, text_data)
        else:
            new_text = text_data

        return new_text

    @staticmethod
    def mask_reverse_text(text_data):
        new_text = text_data[::-1]
        return new_text

    @staticmethod
    def mask_random_text(text_data):
        if isinstance(text_data, str):
            length = len(text_data)
            num_to_replace = int(length * (40 / 100.0))
            indices_to_replace = random.sample(range(length), num_to_replace)
            modified_list = list(text_data)
            for index in indices_to_replace:
                modified_list[index] = Actions.MASK_CHAR.value

            new_text = ''.join(modified_list)
        else:
            new_text = text_data

        return new_text

    @staticmethod
    def mask_middle_text(text_data):
        length = len(text_data)
        start_length = int(length * (25 / 100.0))
        end_length = int(length * (25 / 100.0))
        middle_length = length - start_length - end_length

        if middle_length <= 0:
            new_text = text_data
        else:
            new_text = text_data[:start_length] + (Actions.MASK_CHAR.value * middle_length) + text_data[-end_length:]

        return new_text

    @staticmethod
    def mask_end_text(text_data):
        if isinstance(text_data, str):
            length = len(text_data)
            mask_length = int(length * (60 / 100.0))
            masked_part = Actions.MASK_CHAR.value * mask_length
            new_text = text_data[:-mask_length] + masked_part
        else:
            new_text = text_data
        return new_text

    @staticmethod
    def mask_middle_with_random_chars(text_data):
        length = len(text_data)
        start_length = int(length * 0.25)
        end_length = int(length * 0.25)
        middle_length = length - start_length - end_length
        if middle_length <= 0:
            new_text = text_data
        else:
            random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=middle_length))
            new_text = text_data[:start_length] + random_chars + text_data[-end_length:]

        return new_text

    @staticmethod
    def randomize_text_length(text_data):
        text_length = len(text_data)
        new_text = []
        while sum(len(word) for word in new_text) + len(new_text) - 1 < text_length:
            random_word = random.choice(word_list)
            new_text.append(random_word)

        total_length = sum(len(word) for word in new_text) + len(new_text) - 1
        if total_length > text_length:
            last_word = new_text[-1]
            new_text[-1] = last_word[:len(last_word) - (total_length - text_length)]

        new_text = ' '.join(new_text).strip()
        return new_text

    def mask_text(self, text_data):
        mask_function = self.masking_strategies.get(self.mask_type)
        if mask_function:
            new_text = mask_function(text_data)
        else:
            new_text = text_data
        return new_text

    def mask_json_data(self, json_data):
        masked_data = json_data.copy()
        for key, value in masked_data.items():
            if isinstance(value, str) and value.startswith('{'):
                masked_data[key] = MaskUtils.mask_json_data(self, json.loads(value))
            elif isinstance(value, list):
                masked_list = []
                for item in value:
                    if isinstance(item, list):
                        masked_list.append(MaskUtils.mask_array_data(self, item))
                    elif isinstance(item, str) and item.startswith('{'):
                        masked_list.append(MaskUtils.mask_json_data(self, json.loads(item)))
                    elif isinstance(item, dict):
                        masked_list.append(MaskUtils.mask_json_data(self, item))
                    else:
                        masked_list.append(self.mask_text(item))
                masked_data[key] = masked_list
            elif isinstance(value, dict) or (isinstance(value, str) and value.startswith('{')):
                if isinstance(value, str):
                    value = json.loads(value)
                masked_data[key] = MaskUtils.mask_json_data(value)
            elif isinstance(value, str):
                masked_data[key] = self.mask_text(value)

        masked_json_data = json.dumps(masked_data)

        return masked_json_data

    def mask_array_data(self, array_data):
        masked_list = []
        if isinstance(array_data, list):
            for item in array_data:
                if isinstance(item, list):
                    masked_list.append(MaskUtils.mask_array_data(self, item))
                elif isinstance(item, dict) or (isinstance(item, str) and item.startswith('{')):
                    masked_list.append(self.mask_json_data(json.loads(item)))
                else:
                    masked_list.append(self.mask_text(item))
        else:
            masked_list = array_data
        return masked_list

    def get_table_columns(self):
        result = self.connection.execute(text(
            f"SELECT column_name FROM information_schema.columns WHERE table_name = '{self.table}' AND column_name <> 'id'"
        ).params(table=self.table))

        columns = []
        for row in result:
            columns.append(row[0])
        return columns

    def delete_rows_in_chunks(self):

        signal.signal(signal.SIGINT, MaskUtils.handler)

        try:
            if not 0 <= self.percentage <= 100:
                print("Error: Percentage should be between 0 and 100.")
                return

            with self.connection.begin():
                total_rows = self.connection.execute(text(f'SELECT COUNT(*) FROM {self.table}')).scalar()
                rows_to_delete = int(total_rows * (self.percentage / 100))

                if rows_to_delete > 0:
                    chunks = (rows_to_delete + self.chunk_size - 1) // self.chunk_size

                    for chunk in range(chunks):
                        offset = chunk * self.chunk_size
                        limit = min(self.chunk_size, rows_to_delete - offset)

                        delete_query = text(
                            f'DELETE FROM {self.table} WHERE ctid IN (SELECT ctid FROM {self.table} ORDER BY RANDOM() OFFSET :offset LIMIT :limit)'
                        ).bindparams(offset=offset, limit=limit)
                        self.connection.execute(delete_query)
                        print(f"{chunk + 1} chunks processed.")

                    print(f"{self.percentage}% of data deleted from the {self.table} table.")
                else:
                    print(f"No rows to delete from the {self.table} table.")
        except Exception as e:
            print(f"Error: {e}")
            self.connection.rollback()

    def is_column_maskable(self, column_name):
        query = text(f'SELECT data_type FROM information_schema.columns WHERE table_name = :table_name AND column_name = :column_name')\
            .bindparams(table_name=self.table, column_name=column_name)
        result = self.connection.execute(query, {"table_name": self.table, "column_name": column_name}).scalar()

        if not result:
            return False, None

        data_type = result.lower()
        maskable_types = ['array', 'text', 'jsonb', 'character varying']
        is_maskable = data_type in maskable_types

        if is_maskable:
            data_type = data_type
        else:
            data_type = None

        return is_maskable, data_type

    def masking(self):

        self.check_mask_type()

        columns = self.columns if self.columns else self.get_table_columns()

        count = 0
        try:

            total_rows = self.connection.execute(text(f"SELECT COUNT(*) FROM {self.table}")).scalar()

            signal.signal(signal.SIGINT, MaskUtils.handler)

            for column in columns:
                maskable, data_type = self.is_column_maskable(column)
                if not maskable:
                    print(f"Skipping column '{column}' because its type is not maskable.")
                    continue

                for offset in range(0, total_rows, self.chunk_size):
                    query = text(
                        f"SELECT id, {column} FROM {self.table} ORDER BY id LIMIT {self.chunk_size} OFFSET {offset};"
                    )
                    id_and_column_data = self.connection.execute(query).fetchall()

                    for tuple_data in id_and_column_data:
                        row_id, old_value = tuple_data
                        if old_value is not None:
                            if data_type == 'character varying' or data_type == 'text':
                                old_value = self.mask_text(old_value)
                            elif data_type == 'jsonb':
                                old_value = MaskUtils.mask_json_data(self, old_value)
                            elif data_type == 'array':
                                old_value = MaskUtils.mask_array_data(self, old_value)

                            update_query = text(
                                f"UPDATE {self.table} SET {column} = :regenerated_value WHERE id = :row_id"
                            )
                            self.connection.execute(update_query, {"regenerated_value": old_value, "row_id": row_id})
                            self.connection.commit()
                        count += 1

                    print(f"Updated {count} rows in {self.table} for {column}, offset: {offset}")
                    count = 0

            self.connection.close()
        except Exception as e:
            print("error : ", e)

