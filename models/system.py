from models.job import Job
from models.applicant import Applicant

class HRSystem:
    def __init__(self):
        self.jobs = []
        self.applicants = []
        self.job_counter = 1
        self.applicant_counter = 1

    # Job Management
    def add_job(self, title, department):
        job = Job(self.job_counter, title, department)
        self.jobs.append(job)
        self.job_counter += 1
        return job

    def toggle_job_status(self, job_id):
        job = self.find_job_by_id(job_id)
        if job:
            job.toggle_status()
            return True
        return False

    def find_job_by_id(self, job_id):
        for job in self.jobs:
            if job.job_id == job_id:
                return job
        return None

    # Applicant Management
    def add_applicant(self, name, applied_job_id):
        job = self.find_job_by_id(applied_job_id)
        if job:
            applicant = Applicant(self.applicant_counter, name, job.title)
            self.applicants.append(applicant)
            self.applicant_counter += 1
            return applicant
        return None

    def update_applicant_status(self, applicant_id, new_status):
        applicant = self.find_applicant_by_id(applicant_id)
        if applicant:
            applicant.update_status(new_status)
            return True
        return False

    def schedule_applicant_interview(self, applicant_id, schedule):
        applicant = self.find_applicant_by_id(applicant_id)
        if applicant:
            applicant.schedule_interview(schedule)
            return True
        return False

    def toggle_applicant_shortlist(self, applicant_id):
        applicant = self.find_applicant_by_id(applicant_id)
        if applicant:
            applicant.toggle_shortlist()
            return True
        return False

    def save_applicant_note(self, applicant_id, note):
        applicant = self.find_applicant_by_id(applicant_id)
        if applicant:
            applicant.add_notes(note)
            return True
        return False

    def find_applicant_by_id(self, applicant_id):
        for app in self.applicants:
            if app.applicant_id == applicant_id:
                return app
        return None
