# -*- coding: utf-8 -*-
import sqlite3

class LaterationDAL:

    # Private object
    __conn = None

    def __init__(self):
        self.__dbname = '/home/pi/IME/Multilateration/DB/lateration.db'

    def __del__(self):
        self.CloseDB()

    def ConnectDB(self):
        #sqlite3.connect(database[, timeout, detect_types, isolation_level,
        #check_same_thread, factory, cached_statements, uri])
        #Opens a connection to the SQLite database file database.  You can use
        #":memory:" to open a database connection to a database that resides in
        #RAM instead of on disk.
        self.__conn = sqlite3.connect(self.__dbname)
        print("Opened database successfully")
        self.__db = self.__conn.cursor()

    def SaveData(self, oFlight):
        # Insert a row of data
        self.__conn.execute("INSERT INTO GPS (DATE, LONGITUDE, LATITUDE, ADDRESS, NAME, RSSI, QUALITY, FREQUENCY, DISTANCIA, VALIDO) VALUES (?,?,?,?,?,?,?,?,?,?);",
                            (oFlight.datetime, repr(oFlight.longitude), repr(oFlight.latitude),oFlight.address, oFlight.name, oFlight.signal, oFlight.quality, oFlight.frequency, oFlight.distancy, oFlight.valido))
        # Save (commit) the changes
        self.__conn.commit()
        print("Records created successfully")

    def CloseDB(self):
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.__db.close()
