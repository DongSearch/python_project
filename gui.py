import tkinter as tk
from tkinter import messagebox, ttk
import json
import student


class StudentApp :
    def __init__(self,root):
        self.manager = student.StudentManager()
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        left = tk.Frame(self.root)
        left.pack (side=tk.LEFT, fill=tk.Y, padx = 10, pady = 10)

        tk.Button(left, text="Add Student", width = 20, command=self.add_student).pack(pady = 5)
        tk.Button(left, text="Detail", width=20, command = self.detail).pack(pady=5)
        tk.Button(left, text="Save Data", width=20, command=self.save_data).pack(pady=5)
        tk.Button(left, text="Load Data", width=20, command=self.load_data).pack(pady=5)    

        right = tk.Frame(self.root)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        columns = ("ID", "Name", "Final Score")
        self.tree = ttk.Treeview(right, columns=columns, show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")  
        self.tree.heading("Final Score", text="Final Score")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def refresh_list(self):
        self.tree.delete(*self.tree.get_children())
        for sid, info in self.manager.get_all_students().items():
            self.tree.insert("", tk.END, values=(sid, info["name"], info["final_score"]))

    def add_student(self):
        win = tk.Toplevel(self.root)
        win.title("Add Student")
        labels = ["ID", "Name", "Major", "Year", "Address"]
        entries = {}

        for i , label in enumerate(labels) :
            tk.Label(win, text=label).grid(row=i, column=0, pady=5)
            e = tk.Entry(win)
            e.grid(row=i,column=1)
            entries[label] = e

        def submit():
            try : 
                info = {
                    "id" : int(entries["ID"].get()),
                    "name" : entries["Name"].get(),
                    "major" : entries["Major"].get() or None,
                    "year" : entries["Year"].get() or None,
                    "address" : entries["Address"].get() or None
                }
                self.manager.add_student(info)
                self.refresh_list()
                win.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Add", command=submit).grid(row=6,column=0, columnspan=2,pady=10)

    def detail(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No student selected")
            return
        sid = int(self.tree.item(selected[0])['values'][0])
        student = self.manager.get_student(sid)

        win = tk.Toplevel(self.root)
        win.title("Student Detail")
        top = tk.Frame(win)
        top.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        tk.Label(top, text = " Student Detail ", font=("Arial", 16)).pack()
        bottom = tk.Frame(win)
        bottom.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(bottom , text = " Attendance Records ", font=("Arial", 14)).pack()
        self.att = ttk.Treeview(bottom, columns=("Date", "Status", "Note"), show ="headings")
        self.att.heading("Date" , text= "Date")
        self.att.heading("Status" , text= "Status")
        self.att.heading("Note" , text= "Note")    
        self.att.pack(fill=tk.BOTH, expand=True)
        self.att.delete(*self.att.get_children())
        for v in student.attendance_dict.values():
            self.att.insert("", tk.END, values=(v.date.isoformat(), v.status, v.note))
        button_frame2 = tk.Frame(bottom)
        button_frame2.pack(side=tk.TOP,padx=10,pady=10)
        tk.Button(button_frame2, text="Add", command=lambda: self.add_attendance(student),width= 20).pack(side=tk.LEFT,pady=5)
        tk.Button(button_frame2, text="Delete", command=lambda: self.delete_attendance(student),width= 20).pack(side=tk.LEFT,pady=5,padx=10)


        bottom2 = tk.Frame(win)
        bottom2.pack(side= tk.TOP,fill=tk.BOTH,expand=True, padx=10,pady=10)
        tk.Label(bottom2,text =" Grade" ,font=("Arial",14)).pack()
        self.grade = ttk.Treeview(bottom2, columns=("Key","Type","Score","Date","Note"), show="headings")
        self.grade.heading("Key", text="Key")
        self.grade.heading("Type", text="Type")
        self.grade.heading("Score", text="Score")
        self.grade.heading("Date", text="Date")
        self.grade.heading("Note", text="Note")
        self.grade.pack(fill=tk.BOTH, expand=True)
        self.grade.delete(*self.grade.get_children())
        for k, v in student.grade_list.items():
            self.grade.insert("", tk.END, values=(k,v.type, v.score, v.date.isoformat(), v.note))
        button_frame = tk.Frame(bottom2)
        button_frame.pack(side=tk.TOP,padx=10,pady=10)
        tk.Button(button_frame, text="Add", command=lambda: self.add_grade(student),width= 20).pack(side=tk.LEFT,pady=5)
        tk.Button(button_frame, text="Delete", command=lambda: self.delete_grade(student),width= 20).pack(side=tk.LEFT,pady=5,padx=10)

    def add_grade(self,student):
        grade_win = tk.Toplevel(self.root)
        grade_win.title("Add Grade")
        tk.Label(grade_win,text="key").grid(row=0,column=0,pady=5)
        k = tk.Entry(grade_win,width=30)
        k.grid(row=0,column=1,pady=5)
        tk.Label(grade_win,text="type").grid(row=1,column=0,pady=5)
        t = ttk.Combobox(grade_win, values=["assignment","exam","etc"],width=27)
        t.grid(row=1,column=1,pady=5)
        tk.Label(grade_win,text="score").grid(row=2,column=0,pady=5)
        s = tk.Entry(grade_win,width=30)
        s.grid(row=2,column=1,pady=5)
        tk.Label(grade_win,text="max_score").grid(row=3,column=0,pady=5)
        ms = tk.Entry(grade_win,width=30)
        ms.grid(row=3,column=1,pady=5)
        tk.Label(grade_win,text="weight").grid(row=4,column=0,pady=5)
        w = tk.Entry(grade_win,width=30)
        w.grid(row=4,column=1,pady=5)
        tk.Label(grade_win,text="date").grid(row=5,column=0,pady=5)
        d = tk.Entry(grade_win,width=30)
        d.grid(row=5,column=1,pady=5)
        tk.Label(grade_win,text="note").grid(row=6,column=0,pady=5)
        n = tk.Entry(grade_win,width=30)
        n.grid(row=6,column=1,pady=5)    
        def submit_grade():
                key = k.get()
                g_t = t.get()
                g_s = s.get()
                g_ms = ms.get()
                g_w = w.get()
                g_d = d.get()
                g_n = n.get() or None
                try :
                    student.add_grade({"key" : key, "type" : g_t, "score": g_s,
                                      "max_score" : g_ms, "weight" :g_w, "date":g_d,"note":g_n})
                    v = student.grade_list[key]
                    self.grade.insert("",tk.END,values=(key,v.type,v.score,v.date.isoformat(),v.note))
                    grade_win.destroy()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
        tk.Button(grade_win,text="Submit", command=submit_grade).grid(row=7,column=0,columnspan=2,pady=10)

    def delete_grade(self,student):
        selected = self.grade.selection()
        if not selected :
            messagebox.showwarning("warning", "No grade selected")
            return
        key = self.grade.item(selected[0])['values'][0]
        try:
            student.delete_grade(key=key)
            self.grade.delete(selected[0])
        except ValueError as e:
            messagebox.showerror("Error", str(e))



    def delete_attendance(self, student):
        selected = self.att.selection()
        if not selected :
            messagebox.showwarning("warning", "No attendance record selected")
            return    
        date = self.att.item(selected[0])['values'][0]
        try :
            student.delete_attendance(date=date)
            self.att.delete(selected[0])
        except ValueError as e: 
            messagebox.showerror("Error", str(e))
    
        




    def add_attendance(self, student):
        att_win = tk.Toplevel(self.root)
        att_win.title("Add Attendance")
        tk.Label(att_win, text="Date (YYYY-MM-DD):").grid(row=0, column=0, pady=5)
        e_date = tk.Entry(att_win, width=30)
        e_date.grid(row=0, column=1, pady=5)
        tk.Label(att_win, text="Status:").grid(row=1, column=0, pady=5)
        c_status = ttk.Combobox(att_win, values =["present","absent","late","early","excused"], width=27)
        c_status.grid(row=1, column=1, pady=5)
        tk.Label(att_win, text="Note:").grid(row=2, column=0, pady=5)   
        e_note = tk.Entry(att_win, width=30)
        e_note.grid(row=2, column=1, pady=5)
        def submit_att():
            date = e_date.get()
            status = c_status.get()
            note = e_note.get()
            try :
                student.add_attendance(date=date, status=status, note=note)
                v = student.attendance_dict[date]
                self.att.insert("", tk.END, values=(v.date.isoformat(), v.status, v.note))
                att_win.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        tk.Button(att_win, text="Submit", command=submit_att).grid(row=3, column=0, columnspan=2, pady=10)
        


        


        




    def save_data(self):
        self.manager.save("students_data.json")
        messagebox.showinfo("Info", "Data saved successfully")
    
    def load_data(self):
        self.manager.load("students_data.json")
        self.refresh_list()
        messagebox.showinfo("Info", "Data loaded successfully")

        


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()