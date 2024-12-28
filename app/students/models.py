from app import mysql
import cloudinary.uploader
class Students(object):
    def __init__(self, id_number=None, first_name=None, last_name=None, year_level=None, gender=None, student_course=None, image_url=None,):
        self.id_number = id_number
        self.first_name = first_name
        self.last_name = last_name
        self.year_level = year_level
        self.gender = gender
        self.student_course = student_course
        self.image_url = image_url

    @classmethod
    def get_all_students(cls, search_by=None, search_term=None, offset=0, limit=10):
        try:
            # Get a cursor from the existing MySQL connection
            with mysql.connection.cursor() as curs:
                sql = """
                    SELECT 
                        s.student_id, 
                        s.student_firstname, 
                        s.student_lastname, 
                        s.student_year, 
                        s.student_gender, 
                        CONCAT(c.course_code, ' (', cl.college_name, ')') AS student_course, 
                        s.image_url 
                    FROM student_table AS s
                    LEFT JOIN course_table AS c
                    ON s.student_course = c.course_code
                    LEFT JOIN college_table AS cl
                    ON c.course_college = cl.college_code
                    
                    """
                params = []

                if search_term:
                    search_pattern = f"%{search_term}%"
                    if search_by == 'student-id':
                        sql += " WHERE s.student_id LIKE %s"
                        params.append(search_pattern)
                    elif search_by == 'student-firstname':
                        sql += " WHERE s.student_firstname LIKE %s"
                        params.append(search_pattern)
                    elif search_by == 'student-lastname':
                        sql += " WHERE s.student_lastname LIKE %s"
                        params.append(search_pattern)
                    elif search_by == 'student-year':
                        sql += " WHERE s.student_year LIKE %s"
                        params.append(search_pattern)
                    elif search_by == 'course-and-college':
                        sql += " WHERE (c.course_code LIKE %s OR cl.college_name LIKE %s)"
                        params.append(search_pattern)
                        params.append(search_pattern)
            
                    # Apply LIMIT and OFFSET
                sql += " LIMIT %s OFFSET %s"
                params.append(limit)
                params.append(offset)

                # Execute the query with the parameters
                curs.execute(sql, tuple(params))

                student = [cls(id_number=row[0], first_name=row[1], last_name=row[2], year_level=row[3], 
                               gender=row[4], student_course=row[5], image_url=row[6]) for row in curs.fetchall()]

                
            # Return a list of students objects
            return student

        except Exception as e:
            print(f"Error fetching all students: {e}")
            return []
    
    @classmethod
    def get_total_students(cls, search_by=None, search_term=None):
        try:
            with mysql.connection.cursor() as curs:
                sql = """
                    SELECT COUNT(*) 
                    FROM student_table AS s
                    LEFT JOIN course_table AS c
                    ON s.student_course = c.course_code
                    LEFT JOIN college_table AS cl
                    ON c.course_college = cl.college_code
                """

                if search_term:
                    search_pattern = f"%{search_term}%"
                    if search_by == 'student-id':
                        sql += " WHERE s.student_id LIKE %s"
                    elif search_by == 'student-firstname':
                        sql += " WHERE s.student_firstname LIKE %s"
                    elif search_by == 'student-lastname':
                        sql += " WHERE s.student_lastname LIKE %s"
                    elif search_by == 'student-year':
                        sql += " WHERE s.student_year LIKE %s"
                    elif search_by == 'course-and-college':
                        sql += " WHERE (c.course_code LIKE %s OR cl.college_name LIKE %s)"
                    curs.execute(sql, (search_pattern, search_pattern) if search_by == 'course-and-college' else (search_pattern,))
                else:
                    curs.execute(sql)

                result = curs.fetchone()
                return result[0] if result else 0

        except Exception as e:
            print(f"Error fetching total number of students: {e}")
            return 0





    @classmethod
    def get_by_id(cls, student_id):
        try:
            # Get a cursor from the existing MySQL connection
            with mysql.connection.cursor() as curs:
                # Query to fetch a student by ID
                sql = "SELECT * FROM student_table WHERE student_id = %s"
                curs.execute(sql, (student_id,))
                
                # Fetch one result
                result = curs.fetchone()

            # Return an instance of Students if a result is found, otherwise None
            return cls(*result) if result else None

        except Exception as e:
            # Handle exceptions by printing the error and returning None
            print(f"Error fetching student by ID: {e}")
            return None
    
    def add_student(self):
        try:
            # Get a cursor from the existing MySQL connection
            with mysql.connection.cursor() as curs:
                # SQL query to insert student data into the table
                sql = """
                INSERT INTO student_table (image_url, student_id, student_firstname, student_lastname, student_year, student_gender, student_course)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                
                # Execute the SQL query with the object's data
                curs.execute(sql, (
                    self.image_url,
                    self.id_number,
                    self.first_name,
                    self.last_name,
                    self.year_level,
                    self.gender,
                    self.student_course
                ))
                
                # Commit the transaction to make changes persistent
                mysql.connection.commit()

                print("Student added successfully!")


        except Exception as e:
            # Handle other exceptions
            print(f"Error adding student: {e}")
            raise
    
    def delete_student(self):
        try:
            conn = mysql.connection
            with conn.cursor() as curs:  # Automatically closes the cursor after the block
                sql = "DELETE FROM student_table WHERE student_id = %s"
                curs.execute(sql, (self.id_number,))  # Use the correct attribute for the student ID
                conn.commit()
        except Exception as e:
            print(f"Error deleting student: {e}")

    def edit_student(self):
        try:
            conn = mysql.connection
            with conn.cursor() as curs:
                sql = """
                    UPDATE student_table 
                    SET student_firstname=%s, student_lastname=%s, student_year=%s, student_gender=%s, student_course=%s,
                    image_url=%s
                    WHERE student_id=%s
                """
                values = (self.first_name, self.last_name, self.year_level, self.gender, self.student_course, 
                          self.image_url, self.id_number)
                print("Executing SQL:", sql)
                print("With values:", values)
                curs.execute(sql, values)
                conn.commit()
        except Exception as e:
            print(f"Error editing student: {e}")

