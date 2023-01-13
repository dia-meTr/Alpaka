"""This is module for Graphic class"""

import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd


def clear_data(data):
    """This is function for making data clearer"""
    data = pd.DataFrame(data)
    data = data.mask(data.eq('None')).dropna()

    return data


class Graphic:
    """This is class for graphic drawing"""
    def __init__(self, cursor, table, names, heights):
        self.heights = heights
        self.names = names
        self.table = table
        self.cursor = cursor

    def get_data(self, filters, sorter):
        """This is methode for getting needed data from BD"""

        query = f"SELECT `{self.heights}`, `{self.names}` " \
                f"FROM `{self.table}`" + filters + sorter

        print(query)
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        print(data)
        return data

    def draw(self, filters, sorter):
        """This is methode for graphic drawing"""
        try:
            data = self.get_data(filters, sorter)
            data = clear_data(data)
        except mysql.connector.errors.DatabaseError as ex:
            print(ex)

        fig = plt.figure()
        axes = fig.add_subplot(111)

        axes.bar(data[1], data[0])

        axes.set_ylabel(self.heights)
        axes.set_xlabel(self.names)

        plt.show()
