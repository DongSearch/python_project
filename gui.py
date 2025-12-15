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
        text = tk.Text(win, wrap=tk.WORD)
        text.pack()
        text.insert(tk.END, json.dumps(student.to_dict(), indent=4, ensure_ascii=False) )
        text.config(state=tk.DISABLED)

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