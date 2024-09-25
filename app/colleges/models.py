from app import mysql

class Colleges(object):
    def __init__(self, code=None, name=None, new_code=None):
        self.code = code
        self.name = name
        self.new_code = new_code

    @classmethod
    def get_all_colleges(cls):
        try:
            # Get a cursor from the existing MySQL connection
            with mysql.connection.cursor() as curs:
                sql = "SELECT college_code, college_name FROM college_table"
                curs.execute(sql)

                # Fetch all results
                colleges = curs.fetchall()

            # Return a list of Colleges objects
            return colleges

        except Exception as e:
            print(f"Error fetching all colleges: {e}")
            return []
