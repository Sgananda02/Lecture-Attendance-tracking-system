import mysql.connector
import pickle
import datetime

class MySQLdb:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return connection
        except mysql.connector.Error as error:
            print("Failed to connect to the database: {}".format(error))
            return None

    def execute_query(self, connection, query):
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as error:
            print("Failed to execute query: {}".format(error))
            return []

    def insert_data(self, connection, table_name, data):
        try:
            cursor = connection.cursor()
            placeholders = ', '.join(['%s'] * len(data))
            columns = ', '.join(data.keys())
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, tuple(data.values()))
            connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as error:
            print("Failed to insert data: {}".format(error))
            return False

    def check_student_exists(self, connection, student_number):
        try:
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM student_table WHERE Student_Number = %s", (student_number,))
            student = cursor.fetchone()

            cursor.close()

            return student is not None

        except mysql.connector.Error as error:
            print("Failed to check student existence: {}".format(error))
            return False

    def check_student_module(self, connection, student_id, module_id):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM enrollments WHERE Student_Number = %s AND Course_Code = %s", (student_id, module_id))
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0

        except mysql.connector.Error as error:
            print("Failed to check student module enrollment: {}".format(error))
            return False

    def load_face_recognition_data(self, connection, course_code):
        try:
            cursor = connection.cursor()

            cursor.execute("SELECT Student_Number FROM enrollments WHERE Course_Code = %s", (course_code,))
            enrolled_students = [row[0] for row in cursor.fetchall()]

            in_clause = ', '.join(['%s' for _ in enrolled_students])

            query = "SELECT Student_Number, Feature_Vector FROM features WHERE Student_Number IN ({})".format(in_clause)
            cursor.execute(query, enrolled_students)
            data = cursor.fetchall()
            cursor.close()

            labels, feature_vectors = [], []
            for row in data:
                labels.append(row[0])
                feature_vectors.append(pickle.loads(row[1]))

            return labels, feature_vectors,enrolled_students

        except Exception as error:
            print("Failed to load face recognition data:", error)
            return [], []

    def retrieve_class_info(self):
        try:
            connect = self.connect_to_database()
            cursor = connect.cursor()
            current_datetime = datetime.datetime.now()
            day_of_week = current_datetime.weekday()
            current_time = current_datetime.strftime("%H:%M:%S")

            cursor.execute(
                "SELECT schedule_id, Course_Code, Start_time, End_time FROM schedule "
                "WHERE day_of_week = %s AND %s BETWEEN Start_time AND End_time",
                (day_of_week, current_time),
            )

            rows = cursor.fetchall()

            cursor.close()

            for row in rows:
                schedule_id, module_name, start_time, end_time = row

            if rows:
                return schedule_id, module_name, start_time, end_time
            else:
                return None, None, None, None

        except Exception as error:
            print("Failed to retrieve class info from the database:", error)
            return None, None, None, None

    def check_existing_session(self, schedule_id, class_start_time, connection):
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT session_id FROM class_sessions "
                "WHERE schedule_id = %s AND Start_time = %s",
                (schedule_id, class_start_time)
            )
            existing_session = cursor.fetchone()
            cursor.close()

            if existing_session:
                return existing_session[0]
            else:
                return None

        except Exception as error:
            print("Failed to check for existing session:", error)
            return None
        
    def get_last_insert_id(self, cursor):
        try:
            cursor.execute("SELECT LAST_INSERT_ID()")
            result = cursor.fetchone()
            if result:
                last_insert_id = result[0]
                return last_insert_id
        except Exception as e:
            print(f"Error while fetching last insert ID: {e}")
            return None
        
    def retrieve_feature_vectors_and_labels(self, connection):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT Student_Number, Feature_Vector FROM features")
            data = cursor.fetchall()
            cursor.close()
            connection.close()

            labels, feature_vectors = [], []
            for row in data:
                labels.append(row[0])
                feature_vectors.append(pickle.loads(row[1]))

            return labels, feature_vectors

        except Exception as error:
            print("Failed to retrieve feature vectors and labels from the database:", error)
            return [], []

    def close_connection(self, connection):
        if connection.is_connected():
            connection.close()
