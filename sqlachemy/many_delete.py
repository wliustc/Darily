from sqlalchemy.orm import sessionmaker

from many_create import engine
from many_create import School
from many_create import Student

Session = sessionmaker(engine)
db_session = Session()

school = db_session.query(School).filter(School.name == "蹲").first()
stu = db_session.query(Student).filter(Student.school_id == school.id).delete()
db_session.commit()
db_session.close()
