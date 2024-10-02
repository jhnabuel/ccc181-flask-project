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
                colleges = [cls(code=row[0], name=row[1]) for row in curs.fetchall()]

            # Return a list of Colleges objects
            return colleges

        except Exception as e:
            print(f"Error fetching all colleges: {e}")
            return []
        
    @classmethod
    def get_by_code(cls, college_code):
        try:
            with mysql.connection.cursor() as curs:
                sql = "SELECT * FROM college_table WHERE college_code = %s"
                curs.execute(sql, (college_code,))
                result = curs.fetchone()
            return cls(*result) if result else None
        except Exception as e:
            # Handle the exception (e.g., log the error)
            print(f"Error fetching college by code: {e}")
            return None


    def add_college(self):
        try:
            conn = mysql.connection
            curs = conn.cursor()
            # Correct SQL statement
            sql = "INSERT INTO college_table (college_code, college_name) VALUES (%s, %s)"
            values = (self.code, self.name)
            curs.execute(sql, values)
            conn.commit()
        except Exception as e:
            print(f"Error adding college: {e}")
    
    def delete_college(self):
        try:
            conn = mysql.connection
            curs = conn.cursor()
            sql = "DELETE FROM college_table WHERE college_code = %s"
            curs.execute(sql, (self.code,))
            conn.commit()
            curs.close()
        except Exception as e:
            print(f"Error deleting college: {e}")

    def edit_college(self, original_code):
        try:
            conn = mysql.connection
            curs = conn.cursor()
            sql = "UPDATE college_table SET college_name=%s, college_code=%s WHERE college_code=%s"
            values = (self.name, self.new_code, original_code)  # Use original code as the WHERE condition
            print(self.new_code)
            print(self.name)
            print(original_code)
            curs.execute(sql, values)
            conn.commit()
            curs.close()
        except Exception as e:
            print(f"Error editing college: {e}")
            raise
