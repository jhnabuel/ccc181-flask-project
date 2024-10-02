from app import mysql

class Courses(object):
    def __init__(self, course_code=None, course_name=None, new_code=None, course_college=None):
        self.code = course_code
        self.name = course_name
        self.new_code = new_code
        self.college_code = course_college

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