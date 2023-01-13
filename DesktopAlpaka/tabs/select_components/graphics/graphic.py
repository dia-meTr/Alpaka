import matplotlib.pyplot as plt
import pandas as pd


class Graphic:
    def __init__(self, cursor, table, names, heights):
        self.heights = heights
        self.names = names
        self.table = table
        self.cursor = cursor

    def get_data(self, filters, sorter):
        try:
            query = f"SELECT `{self.heights}`, `{self.names}` " \
                    f"FROM `{self.table}`" + filters + sorter

            print(query)
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            print(data)
            return data
        except Exception as es:
            print(es)

    def draw(self, filters, sorter):
        data = self.get_data(filters, sorter)
        data = self.clear_data(data)

        fig, ax = plt.subplots()

        ax.bar(data[1], data[0])

        ax.set_ylabel(self.heights)
        ax.set_xlabel(self.names)

        plt.show()

    def clear_data(self, data):
        df = pd.DataFrame(data)
        df = df.mask(df.eq('None')).dropna()

        return df


