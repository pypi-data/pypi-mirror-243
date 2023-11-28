import csv


class CsvWriter:

    def __init__(self, data, description):
        self.data = data
        self.description = description

    def save(self, file_name: str, delimiter=',', header=True):
        """
        Save csv
        :param file_name
        :param delimiter
        :param header bool, include header or not
        """
        with open(file_name, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=delimiter)
            if header:
                description = list(map(lambda x: x[0], self.description))
                writer.writerow(description)

            writer.writerows(self.data)
