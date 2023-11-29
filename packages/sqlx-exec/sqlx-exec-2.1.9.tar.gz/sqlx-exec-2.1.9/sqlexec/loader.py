import csv


class Loader:

    def __init__(self, data, description):
        self.data = data
        self.description = description

    def csv(self, file_name: str, delimiter=',', header=True):
        """
        Save csv
        :param file_name
        :param delimiter
        :param header bool, include header or not
        """
        with open(file_name, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=delimiter)
            if header and self.description:
                description = list(map(lambda x: x[0], self.description))
                writer.writerow(description)

            writer.writerows(self.data)

    def df(self):
        """
        transform to DataFrame of pandas.
        :return DataFrame of pandas
        """
        import pandas as pd
        if self.description:
            description = list(map(lambda x: x[0], self.description))
            return pd.DataFrame(data=self.data, columns=description)

        return pd.DataFrame(data=self.data)

