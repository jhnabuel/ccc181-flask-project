from app import mysql

class Colleges(object):
    def __init__(self, code=None, name=None, new_code=None):
        self.code = code
        self.name = name
        self.new_code = new_code

    @classmethod
    def get_all_colleges(cls, search_by=None, search_term=None):
        try:
            # Get a cursor from the existing MySQL connection
            with mysql.connection.cursor() as curs:
                sql = "SELECT college_code, college_name FROM college_table"

                if search_term:
                    if search_by == 'college-name':
                        sql += " WHERE college_name LIKE %s"
                    elif search_by == 'college-code':
                        sql += " WHERE college_code LIKE %s"

                    search_pattern = f"%{search_term}%"
                    curs.execute(sql, (search_pattern,))
                else:
                    curs.execute(sql)

                # Fetch all results
                colleges = curs.fetchall()

            # Return a list of Colleges objects
            return colleges

        except Exception as e:
            print(f"Error fetching all colleges: {e}")
            return []
