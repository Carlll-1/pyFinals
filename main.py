import tkinter as tk
from tkinter import ttk, messagebox
from models.system import HRSystem

class HRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HR Recruitment Management System")
        self.root.geometry("1200x500")

        self.system = HRSystem()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        self.create_job_tab()
        self.create_applicant_tab()

    def create_job_tab(self):
        self.job_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.job_tab, text="Job Posts")

        self.job_tree = ttk.Treeview(self.job_tab, columns=("ID", "Title", "Department", "Status"), show="headings")
        for col in ("ID", "Title", "Department", "Status"):
            self.job_tree.heading(col, text=col)
        self.job_tree.pack(pady=10, fill='x')

        # Controls
        control_frame = tk.Frame(self.job_tab)
        control_frame.pack(pady=5)

        tk.Label(control_frame, text="Job Title").grid(row=0, column=0)
        self.entry_job_title = tk.Entry(control_frame)
        self.entry_job_title.grid(row=0, column=1)

        tk.Label(control_frame, text="Department").grid(row=0, column=2)
        self.entry_job_dept = tk.Entry(control_frame)
        self.entry_job_dept.grid(row=0, column=3)

        tk.Button(control_frame, text="Add Job", command=self.add_job).grid(row=0, column=4, padx=5)
        tk.Button(control_frame, text="Toggle Status", command=self.toggle_job_status).grid(row=1, column=0, pady=5)

        self.refresh_job_list()

    def create_applicant_tab(self):
        self.app_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.app_tab, text="Applicants")

        # Form Inputs
        form_frame = tk.Frame(self.app_tab)
        form_frame.pack(pady=5)

        tk.Label(form_frame, text="Applicant Name").grid(row=0, column=0)
        self.entry_app_name = tk.Entry(form_frame)
        self.entry_app_name.grid(row=0, column=1)

        tk.Label(form_frame, text="Job ID Applied For").grid(row=0, column=2)
        self.entry_app_job_id = tk.Entry(form_frame)
        self.entry_app_job_id.grid(row=0, column=3)

        tk.Button(form_frame, text="Add Applicant", command=self.add_applicant).grid(row=0, column=4, padx=5)

        # Applicant list
        self.app_tree = ttk.Treeview(self.app_tab, columns=("ID", "Name", "Job", "Status", "Shortlisted"), show="headings")
        for col in ("ID", "Name", "Job", "Status", "Shortlisted"):
            self.app_tree.heading(col, text=col)
        self.app_tree.pack(pady=10, fill='x')

        # Status Dropdown
        status_frame = tk.Frame(self.app_tab)
        status_frame.pack(pady=5)

        self.status_var = tk.StringVar(value="New")
        tk.Label(status_frame, text="Update Status:").grid(row=0, column=0)
        self.status_combo = ttk.Combobox(status_frame, textvariable=self.status_var,
                                         values=["New", "Under Review", "Shortlisted", "Interview Scheduled", "Hired", "Rejected"])
        self.status_combo.grid(row=0, column=1)

        tk.Button(status_frame, text="Update Status", command=self.update_status).grid(row=0, column=2, padx=5)

        # Interview Scheduler
        tk.Label(status_frame, text="Interview Schedule (e.g., June 5, 10:00 AM)").grid(row=1, column=0, pady=5)
        self.entry_interview = tk.Entry(status_frame)
        self.entry_interview.grid(row=1, column=1)

        tk.Button(status_frame, text="Schedule Interview", command=self.schedule_interview).grid(row=1, column=2, padx=5)

        # Shortlist toggle
        tk.Button(self.app_tab, text="Toggle Shortlist", command=self.toggle_shortlist).pack(pady=5)

        # Notes section
        notes_frame = tk.Frame(self.app_tab)
        notes_frame.pack(pady=5)

        tk.Label(notes_frame, text="Internal HR Notes").grid(row=0, column=0)
        self.entry_note = tk.Entry(notes_frame, width=50)
        self.entry_note.grid(row=0, column=1)
        tk.Button(notes_frame, text="Save Note", command=self.save_note).grid(row=0, column=2, padx=5)

        self.refresh_applicants()

    # Job tab methods
    def refresh_job_list(self):
        for i in self.job_tree.get_children():
            self.job_tree.delete(i)
        for job in self.system.jobs:
            self.job_tree.insert("", "end", values=(job.job_id, job.title, job.department, job.status))

    def add_job(self):
        title = self.entry_job_title.get().strip()
        dept = self.entry_job_dept.get().strip()
        if title and dept:
            self.system.add_job(title, dept)
            self.entry_job_title.delete(0, tk.END)
            self.entry_job_dept.delete(0, tk.END)
            self.refresh_job_list()
        else:
            messagebox.showwarning("Input Error", "Please enter both job title and department.")

    def toggle_job_status(self):
        selected = self.job_tree.selection()
        if selected:
            job_id = int(self.job_tree.item(selected[0])["values"][0])
            self.system.toggle_job_status(job_id)
            self.refresh_job_list()

    # Applicant tab methods
    def refresh_applicants(self):
        for i in self.app_tree.get_children():
            self.app_tree.delete(i)
        for app in self.system.applicants:
            self.app_tree.insert("", "end", values=(app.applicant_id, app.name, app.applied_job, app.status, "Yes" if app.shortlisted else "No"))

    def add_applicant(self):
        name = self.entry_app_name.get().strip()
        job_id_str = self.entry_app_job_id.get().strip()
        if name and job_id_str.isdigit():
            job_id = int(job_id_str)
            applicant = self.system.add_applicant(name, job_id)
            if applicant:
                self.entry_app_name.delete(0, tk.END)
                self.entry_app_job_id.delete(0, tk.END)
                self.refresh_applicants()
            else:
                messagebox.showerror("Job Not Found", f"No job with ID {job_id} found.")
        else:
            messagebox.showwarning("Input Error", "Please enter a valid name and job ID (number).")

    def update_status(self):
        selected = self.app_tree.selection()
        if selected:
            applicant_id = int(self.app_tree.item(selected[0])["values"][0])
            new_status = self.status_var.get()
            self.system.update_applicant_status(applicant_id, new_status)
            self.refresh_applicants()

    def schedule_interview(self):
        selected = self.app_tree.selection()
        if selected:
            applicant_id = int(self.app_tree.item(selected[0])["values"][0])
            schedule = self.entry_interview.get().strip()
            if schedule:
                self.system.schedule_applicant_interview(applicant_id, schedule)
                self.entry_interview.delete(0, tk.END)
                self.refresh_applicants()
            else:
                messagebox.showwarning("Input Error", "Please enter an interview schedule.")
        else:
            messagebox.showwarning("Selection Error", "Please select an applicant.")

    def toggle_shortlist(self):
        selected = self.app_tree.selection()
        if selected:
            applicant_id = int(self.app_tree.item(selected[0])["values"][0])
            self.system.toggle_applicant_shortlist(applicant_id)
            self.refresh_applicants()

    def save_note(self):
        selected = self.app_tree.selection()
        if selected:
            applicant_id = int(self.app_tree.item(selected[0])["values"][0])
            note = self.entry_note.get().strip()
            self.system.save_applicant_note(applicant_id, note)
            messagebox.showinfo("Note Saved", "Note saved successfully.")
        else:
            messagebox.showwarning("Selection Error", "Please select an applicant.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HRApp(root)
    root.mainloop()
