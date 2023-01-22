#!/usr/bin/env python3

import mysql.connector
from mysql.connector import Error


class Mysql:
    def __init__(self,databaseInfo) -> None:
        try:
            self.connection = mysql.connector.connect(host=databaseInfo['host'],
                                                    database=databaseInfo['database'],
                                                    user=databaseInfo['user'],
                                                    password=databaseInfo['password'])
        except mysql.connector.Error as e:
            print('hey1')
            return False

    def command(self,command) -> list:
        try:
            query = command
            cursor = self.connection.cursor()
            cursor.execute(query)
            return True

        except mysql.connector.Error as e:
            print(e)
            return False
    