from app import mysql

class Courses(object):
    def __init__(self, course_code=None, course_name=None, course_college=None, new_code=None):
        self.code = course_code
        self.name = course_name
        self.college_code = course_college
        self.new_code = new_code

    @classmethod
    def get_all_courses(cls, search_by=None, search_term=None):
        try:
            # Get a cursor from the existing MySQL connection
            with mysql.connection.cursor() as curs:
                sql = "SELECT course_code, course_name, course_college FROM course_table"

                if search_term:
                    if search_by == 'course-name':
                        sql += " WHERE course_name LIKE %s"
                    elif search_by == 'course-code':
                        sql += " WHERE course_code LIKE %s"
                    elif search_by == 'course-college':
                        sql += " WHERE course_college LIKE %s"
                    
                    search_pattern = f"%{search_term}%"
                    curs.execute(sql, (search_pattern,))
                else:
                    curs.execute(sql)

                # Fetch all results
                course = [cls(course_code=row[0], course_name=row[1], course_college=row[2]) for row in curs.fetchall()]

            # Return a list of Colleges objects
            return course

        except Exception as e:
            print(f"Error fetching all courses: {e}")
            return []
        
    @classmethod
    def get_by_code(cls, course_code):
        try:
            with mysql.connection.cursor() as curs:
                sql = "SELECT * FROM course_table WHERE course_code = %s"
                curs.execute(sql, (course_code,))
                result = curs.fetchone()
            return cls(*result) if result else None
        except Exception as e:
            # Handle the exception
            print(f"Error fetching course by code: {e}")
            return None
        
    def add_course(self):
        try:
            conn = mysql.connection
            curs = conn.cursor()
            # Correct SQL statement
            sql = "INSERT INTO course_table (course_code, course_name, course_college) VALUES (%s, %s, %s)"
            values = (self.code, self.name, self.college_code)
            curs.execute(sql, values)
            conn.commit()
        except Exception as e:
            print(f"Error adding course: {e}")

    def delete_course(self):
        try:
            conn = mysql.connection
            with conn.cursor() as curs:  # Automatically closes the cursor after the block
                sql = "DELETE FROM course_table WHERE course_code = %s"
                curs.execute(sql, (self.code,))
                conn.commit()
        except Exception as e:
            print(f"Error deleting course: {e}")
