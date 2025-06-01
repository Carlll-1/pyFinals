class Applicant:
    def __init__(self, applicant_id, name, applied_job, status="New"):
        self.applicant_id = applicant_id
        self.name = name
        self.applied_job = applied_job
        self.status = status  # e.g., New, Under Review, Shortlisted, Interview Scheduled, Hired, Rejected
        self.interview_schedule = None
        self.shortlisted = False
        self.notes = ""

    def update_status(self, new_status):
        self.status = new_status

    def schedule_interview(self, schedule):
        self.interview_schedule = schedule

    def toggle_shortlist(self):
        self.shortlisted = not self.shortlisted

    def add_notes(self, note):
        self.notes = note

    def __str__(self):
        return (f"Applicant[{self.applicant_id}]: {self.name}, Applied for: {self.applied_job}, "
                f"Status: {self.status}, Interview: {self.interview_schedule}, "
                f"Shortlisted: {'Yes' if self.shortlisted else 'No'}")
