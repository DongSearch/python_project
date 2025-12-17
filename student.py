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
        self.grade_list = {}
        self.final_score = 0
    
    def add_attendance(self,date = None,status=None,note=None):
        try :
            d = datetime.datetime.fromisoformat(date)  
        except:
            print("please, put the date in form of 'YYYY-MM-DD' ")
            return
        status_list = ["present","absent","late","early","excused"]
        if status not in status_list :
            print("wrong format of status")
            return
        key = d.date().isoformat()
        a = Attendance(date=d,status=status, note= note)
        self.attendance_dict[key] = a
    
    def get_attendance(self, date = None) :
        try:
            d = datetime.datetime.fromisoformat(date)
        except :
            raise ValueError("please, put the date in from 'YYY-MM-DD")
        
        key = d.date().isoformat()
        if key not in self.attendance_dict.keys() :
            raise ValueError("we can't find the attendance record")
        
        return self.attendance_dict[key]
    
    def delete_attendance(self,date = None):
        if date is None :
            raise ValueError("date should be provided")
        del self.attendance_dict[date]
    
    def to_dict(self) :
        s = {}
        s["id"] = self.id
        s["name"] = self.name
        s["major"] = self.major
        s["year"] = self.year
        s["address"] = self.address
        s["attendance"] = {}
        s["grade"] = {}
        s["final_score"] = self.final_score

        for k, v in self.attendance_dict.items():
            s["attendance"][k] = v.to_dict()
        for k, v in self.grade_list.items():
            s["grade"][k] = v.to_dict()
        return s
    

    def add_grade(self,grade:dict): 
        grade = Grade(grade)
        if grade.key in self.grade_list.keys():
            raise ValueError("this grade is already registered")
        self.grade_list[grade.key] = grade
        self._recalculate_final_score()
    
    def update_grade(self,key, **kwargs):
        if key not in self.grade_list.keys():
            raise ValueError("we can't find the grade")
        grade = self.grade_list[key]

        for k, v in kwargs.items(): 
            if hasattr(grade, k):
                setattr(grade, k, v)
        if grade.score < 0 or grade.score > grade.max_score :
            raise ValueError("score should be between 0 and max_score") 
        
        if not(grade.weight >=0 and grade.weight <=1) :
            raise ValueError("weight should be between 0 and 1")
                        
        self._recalculate_final_score()

        
    def delete_grade(self,key):
        if key not in self.grade_list.keys():
            raise ValueError("we can't find the grade")
        del self.grade_list[key]
        self._recalculate_final_score()
        
    def get_grade(self,key):
        return self.grade_list.get(key)
    
    def _recalculate_final_score(self):
        score = 0.0
        for grade in self.grade_list.values():
            score += (grade.score / grade.max_score) * grade.weight *100
        self.final_score = score


                    
        
class Attendance() :
    def __init__(self,date = None, status = None, note = None):
        self.date = date
        self.current_date = datetime.datetime.now()
        self.status = status
        self.note = note
    
    # convert json -> dict
    def to_dict(self) :
        return {"date" : self.date.date().isoformat(),
                "status" : self.status,
                "note" : self.note,
                "created": self.current_date.isoformat()
                }
    

    # convert dict -> json
    @staticmethod
    def to_json(a) :
        return json.dumps(a.to_dict(), ensure_ascii=False, indent=4)


class StudentManager:
    def __init__(self):
        self.students = {}

    def add_student(self,info):
        s = Student(info)
        if s.id not in self.students.keys():
            self.students[s.id] = s
        else :
            print("already registered, but it updates with new data")
            self.students[s.id] = s

    def get_student(self, student_id):
        return self.students.get(student_id)
    
    def save(self, name):
        d = {str(k) : v.to_dict() for k,v in self.students.items()}
        with open(name, "w",encoding="utf-8") as f :
            json.dump(d,f,ensure_ascii=False, indent = 4)
    
    def load(self,name, path=".") :
        file_path = path +'\\' + name
        with open(file_path,'r',encoding='utf-8') as json_file :
            data = json.load(json_file)

        for id,student_data in data.items():
            student = Student(student_data)

            for k, v in student_data["attendance"].items():
                d = datetime.datetime.fromisoformat(v["date"])
                a = Attendance(date=d, status=v["status"],note=v["note"])
                a.current_date = datetime.datetime.fromisoformat(v["created"])
                student.attendance_dict[k] = a
            
            for k, v in student_data["grade"].items():
                student.grade_list[k] = Grade(v)
            student._recalculate_final_score()   

            
            self.students[int(id)] = student




    def del_student(self,id) :
        if id in self.students.keys() :
            del self.students[id]
        else :
            print("we can't find the student")
    
    def get_all_students(self) :
        summary = {}
        for k, v in self.students.items() :
            summary[k] = {"id" : v.id, "name": v.name, "final_score": v.final_score}
        return summary


class Grade() :
    def __init__(self,info:dict):
        self.key = info.get("key")
        self.type = info.get("type")
        self.id = info.get("id")
        self.score = info.get("score")
        self.max_score = info.get("max_score")
        self.weight = info.get("weight")
        self.date = info.get("date")
        self.note = info.get("note")

        if self.score is None or self.max_score is None:
            raise ValueError("score and max_score should be provided")

        if self.score < 0 or self.score > self.max_score :
            raise ValueError("score should be between 0 and max_score") 
        
        if not(self.weight >=0 and self.weight <=1) :
            raise ValueError("weight should be between 0 and 1")
    
    def to_dict(self) :
        return {
            "key": self.key,
            "type" : self.type,
            "id" : self.id,
            "score" : self.score,
            "max_score" : self.max_score,
            "weight" : self.weight,
            "date" : self.date,
            "note" : self.note

        }
    
