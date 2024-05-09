import os
import random
import heapq
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox

class Employee:
    def __init__(self, emp_id, first_name, last_name, department, salary):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.department = department
        self.salary = salary

    def __repr__(self):
        return f"Employee(ID: {self.emp_id}, Name: {self.first_name} {self.last_name}, Department: {self.department}, Salary: {self.salary})"

    def __lt__(self, other):
        if self.sort_by == 'id':
            return self.emp_id < other.emp_id
        elif self.sort_by == 'last_name':
            return self.last_name < other.last_name
        else:
            raise ValueError("Invalid sorting criterion")

def generate_employee_records(start_id, num_records):
    employees = []
    ids = list(range(start_id, start_id + num_records))
    random.shuffle(ids)
    for emp_id in ids:
        first_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))
        last_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))
        department = random.choice(['HR', 'Engineering', 'Marketing', 'Finance'])
        salary = random.randint(30000, 150000)
        employees.append(Employee(emp_id, first_name, last_name, department, salary))
    return employees

def write_employee_records_to_file(filename, employees):
    with open(filename, 'w') as file:
        for emp in employees:
            file.write(f"{emp.emp_id},{emp.first_name},{emp.last_name},{emp.department},{emp.salary}\n")

def read_employee_records_from_file(filename):
    employees = []
    with open(filename, 'r') as file:
        for line in file:
            emp_id, first_name, last_name, department, salary = line.strip().split(',')
            employees.append(Employee(int(emp_id), first_name, last_name, department, int(salary)))
    return employees

def merge_sorted_files(files, output_filename):
    output_file = open(output_filename, 'w')
    heap = []
    file_pointers = []
    for file in files:
        file_pointer = open(file, 'r')
        file_pointers.append(file_pointer)
        line = file_pointer.readline()
        if line:
            heapq.heappush(heap, (line.split(',')[0], line, file_pointer))
    while heap:
        _, line, file_pointer = heapq.heappop(heap)
        output_file.write(line)
        next_line = file_pointer.readline()
        if next_line:
            heapq.heappush(heap, (next_line.split(',')[0], next_line, file_pointer))
    for file_pointer in file_pointers:
        file_pointer.close()
    output_file.close()

def external_merge_sort(files, sort_by='id'):
    chunk_size = 1000
    chunks = [files[i:i+chunk_size] for i in range(0, len(files), chunk_size)]
    sorted_files = []
    for chunk in chunks:
        employees = []
        for file in chunk:
            employees.extend(read_employee_records_from_file(file))
        if sort_by == 'id':
            sorted_employees = sorted(employees, key=lambda x: x.emp_id)
        elif sort_by == 'last_name':
            sorted_employees = sorted(employees, key=lambda x: x.last_name)
        else:
            raise ValueError("Invalid sorting criterion")
        sorted_file = tempfile.NamedTemporaryFile(mode='w', delete=False, dir=os.getcwd()).name
        with open(sorted_file, 'w') as f:
            for emp in sorted_employees:
                f.write(f"{emp.emp_id},{emp.first_name},{emp.last_name},{emp.department},{emp.salary}\n")
        sorted_files.append(sorted_file)
    while len(sorted_files) > 1:
        new_sorted_files = []
        for i in range(0, len(sorted_files), 2):
            if i + 1 < len(sorted_files):
                output_filename = tempfile.NamedTemporaryFile(mode='w', delete=False, dir=os.getcwd()).name
                merge_sorted_files([sorted_files[i], sorted_files[i + 1]], output_filename)
                new_sorted_files.append(output_filename)
            else:
                new_sorted_files.append(sorted_files[i])
        sorted_files = new_sorted_files
    return sorted_files[0]

def generate_and_sort_files():
    num_files = 16
    records_per_file = 1000
    current_id = 1
    current_dir = os.getcwd()
    files = []
    for i in range(num_files):
        employees = generate_employee_records(current_id, records_per_file)
        filename = os.path.join(current_dir, f"employee_records_{i}.txt")
        write_employee_records_to_file(filename, employees)
        files.append(filename)
        current_id += records_per_file
    return files

def sort_files_and_show_result(sort_by='id'):
    files = generate_and_sort_files()
    sorted_file = external_merge_sort(files, sort_by)
    messagebox.showinfo("Sort Completed", f"Files sorted and merged. Result saved in {sorted_file}")

def select_sort_criteria():
    def on_sort():
        sort_by = var.get()
        sort_files_and_show_result(sort_by)

    root = tk.Tk()
    root.title("Sort Employee Records")
    tk.Label(root, text="Select sorting criteria:").pack()
    var = tk.StringVar(root, "id")
    tk.Radiobutton(root, text="Sort by ID", variable=var, value="id").pack(anchor=tk.W)
    tk.Radiobutton(root, text="Sort by Last Name", variable=var, value="last_name").pack(anchor=tk.W)
    tk.Button(root, text="Sort", command=on_sort).pack()
    root.mainloop()

if __name__ == "__main__":
    select_sort_criteria()
