class Job:
    def __init__(self, job_id, title, department, status="Active"):
        self.job_id = job_id
        self.title = title
        self.department = department
        self.status = status  # "Active" or "Inactive"

    def toggle_status(self):
        self.status = "Inactive" if self.status == "Active" else "Active"

    def __str__(self):
        return f"Job[{self.job_id}]: {self.title} ({self.department}) - {self.status}"
