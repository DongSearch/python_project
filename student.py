import datetime
import json

class Student() :
    def __init__(self,info):
        self.id = info.get('id') if info.get('id') is not None else None
        self.name = info.get('name') if info.get('name') is not None else None
        self.major = info.get('major')if info.get('major') is not None else None
        self.year = info.get('year')if info.get('year') is not None else None
        self.address = info.get('address') if info.get('address') is not None else None
        self.attendance_dict ={}
        self.grade_list = []
        self.final_score = 0
    
    def add_attendance(self,date = None,status=None,note=None):
        a = Attendance(status,note)
        d = date
        try :
            d = datetime.datetime.fromisoformat(date)  
        except:
            print("please, put the date in form of 'YYYY-MM-DD' ")
            return
        status = None
        status_list = ["present","absent","late","early","excused"]
        if a.status in status_list :
            status = a.status
        else : 
            print("wrong format of status")
            return

        self.attendance_dict.update({d : (status,note)})

            



        
        
class Attendance() :
    def __init__(self,status = None, note = None):
        self.current_date = datetime.datetime.now()
        self.status = status
        self.note = note
    
    # convert json -> dict
    @staticmethod
    def to_dict(a) :
        return json.loads(a)
    

    # convert dict -> json
    @staticmethod
    def to_json(a) :
        return json.dumps(a)

info = {
    'id' : 3213,
    'name' : "hi",
    'address' : "hello"
}
s = Student(info)
s.add_attendance("2025-11-12","late")
