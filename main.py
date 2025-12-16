import csv

class Customer:
    def __init__(self, data: dict):
        self.name = data.get('name', '')
        self.device_type = data.get('device_type', '')
        self.browser = data.get('browser', '')
        self.sex = data.get('sex', '')
        self.age = data.get('age')
        self.bill = data.get('bill')
        self.region = data.get('region', '')

    def get_name(self):
        return self.name

    def get_device_type(self):
        return self.device_type

    def get_browser(self):
        return self.browser

    def get_sex(self):
        return self.sex

    def get_age(self):
        return self.age

    def get_bill(self):
        return self.bill

    def get_region(self):
        return self.region



class Reader:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.csv_reader = None
        self.file = None

    def get_customer(self):

        try:
            if self.csv_reader is None:
                file = open(self.filepath, 'r')
                self.csv_reader = csv.DictReader(file)

            row = next(self.csv_reader)
            return Customer(row)

        except StopIteration:
            self.close()
            return None

        except Exception as e:
            print(f'Ошибка чтения файла {e}')
            self.close()
            return None
    def close(self):
        if self.file:
            self.file.close()

    def __del__(self):
        self.close()


class Formatter:
    def __init__(self):
        self.formatted_message = ""

    def _get_year_word(self, age: int) :
        if 11 <= age % 100 <= 19:
            return "лет"
        last_digit = age % 10
        if last_digit == 1:
            return "год"
        elif 2 <= last_digit <= 4:
            return "года"
        else:
            return "лет"

    def format_customer(self, data: Customer):
        name = data.get_name()
        sex = data.get_sex().lower()
        age = data.get_age()
        bill = data.get_bill()
        device = data.get_device_type()
        browser = data.get_browser()
        region = data.get_region()

        if sex == 'female':
            gender_text = "женского пола"
            action_word = "совершила"
        else:
            gender_text = "мужского пола"
            action_word = "совершил"

        device_map = {
            'mobile': 'мобильного',
            'desktop': 'десктопного',
            'tablet': 'планшетного',
            '': 'неизвестного'
        }

        device_text = device_map.get(device, device)

        year_word = self._get_year_word(int(age))

        self.formatted_message = (
            f"Пользователь {name} {gender_text}, {age} {year_word} "
            f"{action_word} покупку на {bill} у.е. с {device_text} "
            f"браузера {browser}. Регион, из которого совершалась покупка: {region}."
        )

    def get_formatted_message(self):
        return self.formatted_message


class Writer:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.file = None

    def write_to_txt(self, data: str):
        try:
            if self.file is None:
                self.file = open(self.filepath, 'w')

            self.file.write(data)

        except Exception as e:
            print(f'Ошибка записи файла {e}')
            self.close()


    def close(self):
        if self.file:
            self.file.close()
            self.file = None

    def __del__(self):
        self.close()


INPUT_CSV_FILE = "web_clients_correct.csv"
OUTPUT_TXT_FILE = "description.txt"

reader = Reader(INPUT_CSV_FILE)
writer = Writer(OUTPUT_TXT_FILE)
while True:
    customer = reader.get_customer()
    if customer is not None:
        formatter = Formatter()
        formatter.format_customer(customer)
        data_line = f"{formatter.get_formatted_message()}\n"
        writer.write_to_txt(data_line)
    else:
        break












