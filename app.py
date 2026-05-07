import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

from resume_parser import extract_text
from utils import (
    extract_skills,
    match_jobs,
    resume_score,
    missing_skills,
    interview_questions,
    fake_resume_score
)
from pdf_generator import generate_pdf

# =========================
# MAIN WINDOW
# =========================
root = tk.Tk()
root.title("AI Resume Analyzer")
root.geometry("850x700")
root.configure(bg="#f4f6f8")

# Global variables
file_path_global = ""
analysis_data = {}

# =========================
# FUNCTIONS
# =========================

def upload_file():
    global file_path_global

    file_path_global = filedialog.askopenfilename(
        title="Select Resume",
        filetypes=[
            ("PDF Files", "*.pdf"),
            ("Word Files", "*.docx")
        ]
    )

    if file_path_global:
        label_file.config(
            text=f"Selected File:\n{file_path_global}"
        )


def analyze_resume():
    global analysis_data

    if not file_path_global:
        messagebox.showerror(
            "Error",
            "Please upload a resume first"
        )
        return

    try:
        # Extract text
        text = extract_text(file_path_global)

        # Analyze resume
        skills = extract_skills(text)

        job_scores = match_jobs(skills)

        top_job = list(job_scores.keys())[0]

        score = resume_score(skills)

        missing = missing_skills(top_job, skills)

        questions = interview_questions()

        fake_check = fake_resume_score(text, skills)

        # Store data
        analysis_data = {
            "score": score,
            "skills": skills,
            "job_scores": job_scores,
            "top_job": top_job,
            "missing": missing,
            "questions": questions
        }

        # Clear previous results
        result_text.delete("1.0", tk.END)

        # Display Results
        result_text.insert(
            tk.END,
            "========== RESUME ANALYSIS ==========\n\n"
        )

        result_text.insert(
            tk.END,
            f"Resume Score: {score}/100\n\n"
        )

        result_text.insert(
            tk.END,
            "Skills Found:\n"
        )

        result_text.insert(
            tk.END,
            ", ".join(skills) + "\n\n"
        )

        result_text.insert(
            tk.END,
            "Job Match Scores:\n"
        )

        for job, sc in job_scores.items():
            result_text.insert(
                tk.END,
                f"• {job}: {sc}%\n"
            )

        result_text.insert(
            tk.END,
            f"\nTop Recommended Role: {top_job}\n\n"
        )

        result_text.insert(
            tk.END,
            "Missing Skills:\n"
        )

        result_text.insert(
            tk.END,
            ", ".join(missing) + "\n\n"
        )

        result_text.insert(
            tk.END,
            "Fake Resume Check:\n"
        )

        result_text.insert(
            tk.END,
            f"{fake_check}\n\n"
        )

        result_text.insert(
            tk.END,
            "Interview Questions:\n"
        )

        for q in questions:
            result_text.insert(
                tk.END,
                f"• {q}\n"
            )

        messagebox.showinfo(
            "Success",
            "Resume analyzed successfully"
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


def generate_report():

    if not analysis_data:
        messagebox.showerror(
            "Error",
            "Please analyze the resume first"
        )
        return

    result = generate_pdf(analysis_data)

    messagebox.showinfo(
        "PDF Report",
        result
    )

# =========================
# HEADING
# =========================

heading = tk.Label(
    root,
    text="AI Resume Analyzer",
    font=("Arial", 24, "bold"),
    bg="#f4f6f8",
    fg="#1f2937"
)

heading.pack(pady=20)

# =========================
# BUTTON FRAME
# =========================

button_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

button_frame.pack(pady=10)

# Upload Button
btn_upload = tk.Button(
    button_frame,
    text="Upload Resume",
    font=("Arial", 12, "bold"),
    bg="#2563eb",
    fg="white",
    padx=15,
    pady=8,
    command=upload_file
)

btn_upload.grid(row=0, column=0, padx=10)

# Analyze Button
btn_analyze = tk.Button(
    button_frame,
    text="Analyze Resume",
    font=("Arial", 12, "bold"),
    bg="#16a34a",
    fg="white",
    padx=15,
    pady=8,
    command=analyze_resume
)

btn_analyze.grid(row=0, column=1, padx=10)

# PDF Button
btn_pdf = tk.Button(
    button_frame,
    text="Generate PDF",
    font=("Arial", 12, "bold"),
    bg="#dc2626",
    fg="white",
    padx=15,
    pady=8,
    command=generate_report
)

btn_pdf.grid(row=0, column=2, padx=10)

# =========================
# FILE LABEL
# =========================

label_file = tk.Label(
    root,
    text="No file selected",
    font=("Arial", 10),
    bg="#f4f6f8",
    fg="#374151",
    wraplength=700,
    justify="center"
)

label_file.pack(pady=10)

# =========================
# RESULT BOX
# =========================

result_text = ScrolledText(
    root,
    width=95,
    height=25,
    font=("Consolas", 10),
    bg="white",
    fg="black"
)

result_text.pack(pady=20)

# =========================
# RUN APPLICATION
# =========================

root.mainloop()