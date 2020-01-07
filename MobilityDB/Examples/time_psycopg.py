import psycopg2
from MobilityDB.psycopg import register
from MobilityDB.MainTypes import TFloat, TFloatInst, TFloatI, TFloatSeq, TFloatS
from . import psycopg_connect

connection = None

try:
	# Set the connection parameters to PostgreSQL
	connection = psycopg_connect()
	connection.autocommit = True

	# Register MobilityDB data types
	register(connection)

	cursor = connection.cursor()

	######################
	# TimestampSet
	######################

	select_query = "select * from tbl_timestampset order by k limit 10"

	cursor.execute(select_query)
	print("\n****************************************************************")
	print("Selecting rows from tbl_timestampset table using cursor.fetchall\n")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("timestampset =", row[1])
		if not row[1]:
			print("")
		else:
			print("timespan =", row[1].timespan(), "\n")

	drop_table_query = '''DROP TABLE IF EXISTS tbl_timestampset_temp;'''
	cursor.execute(drop_table_query)
	connection.commit()
	print("Table deleted successfully in PostgreSQL")

	create_table_query = '''CREATE TABLE tbl_timestampset_temp
	(
	  k integer PRIMARY KEY,
	  ts timestampset
	); '''
	cursor.execute(create_table_query)
	connection.commit()
	print("Table created successfully in PostgreSQL")

	postgres_insert_query = ''' INSERT INTO tbl_timestampset_temp (k, ts) VALUES (%s, %s) '''
	result = cursor.executemany(postgres_insert_query, rows)
	connection.commit()
	count = cursor.rowcount
	print(count, "record(s) inserted successfully into tbl_timestampset_temp table")

	######################
	# Period
	######################

	select_query = "select * from tbl_period order by k limit 10"

	cursor.execute(select_query)
	print("\n****************************************************************")
	print("Selecting rows from tbl_period table using cursor.fetchall\n")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("period =", row[1])
		if not row[1]:
			print("")
		else:
			print("timespan =", row[1].timespan(), "\n")

	drop_table_query = '''DROP TABLE IF EXISTS tbl_period_temp;'''
	cursor.execute(drop_table_query)
	connection.commit()
	print("Table deleted successfully in PostgreSQL")

	create_table_query = '''CREATE TABLE tbl_period_temp
	(
	  k integer PRIMARY KEY,
	  p period
	); '''
	cursor.execute(create_table_query)
	connection.commit()
	print("Table created successfully in PostgreSQL")

	postgres_insert_query = ''' INSERT INTO tbl_period_temp (k, p) VALUES (%s, %s) '''
	result = cursor.executemany(postgres_insert_query, rows)
	connection.commit()
	count = cursor.rowcount
	print(count, "record(s) inserted successfully into tbl_period_temp table")

	######################
	# PeriodSet
	######################

	select_query = "select * from tbl_periodset order by k limit 10"

	cursor.execute(select_query)
	print("\n****************************************************************")
	print("Selecting rows from tbl_periodset table using cursor.fetchall\n")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("periodset =", row[1])
		if not row[1]:
			print("")
		else:
			print("timespan =", row[1].timespan(), "\n")


	drop_table_query = '''DROP TABLE IF EXISTS tbl_periodset_temp;'''
	cursor.execute(drop_table_query)
	connection.commit()
	print("Table deleted successfully in PostgreSQL")

	create_table_query = '''CREATE TABLE tbl_periodset_temp
	(
	  k integer PRIMARY KEY,
	  ps periodset
	); '''
	cursor.execute(create_table_query)
	connection.commit()
	print("Table created successfully in PostgreSQL")

	postgres_insert_query = ''' INSERT INTO tbl_periodset_temp (k, ps) VALUES (%s, %s) '''
	result = cursor.executemany(postgres_insert_query, rows)
	connection.commit()
	count = cursor.rowcount
	print(count, "record(s) inserted successfully into tbl_periodset_temp table")

	print("\n****************************************************************")

except (Exception, psycopg2.Error) as error:
	print("Error while connecting to PostgreSQL", error)

finally:

	if connection:
		connection.close()