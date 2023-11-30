"""
  Dave Skura
  
"""
from sqlitedave_package.sqlitedave import sqlite_db


class var:
	def __init__(self):
		self.db=sqlite_db()

	def set_global_variable(self,variable_name,variable_value):
		dsql = "DELETE FROM z_global WHERE name ='" + variable_name + "'"
		isql = "INSERT INTO z_global(name,value) VALUES ('" + variable_name + "','" + variable_value + "')"
		try:
			self.db.execute(dsql)
		except:
			print('z_global does not exist, creating it')
			self.create_var_table()

		self.db.execute(isql)

	def get_global_variable(self,variable_name):
		sql = "SELECT value FROM z_global WHERE name ='" + variable_name + "'"
		try:
			value = self.db.queryone(sql)
		except:
			print('z_global does not exist, creating it')
			self.create_var_table()
			value = self.db.queryone(sql)
		return value

	def create_var_table(self):
		csql = """
		CREATE TABLE z_global (
			name text PRIMARY KEY,
			value text
		);
		"""
		self.db.execute(csql)
