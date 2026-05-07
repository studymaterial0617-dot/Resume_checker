from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os


def generate_pdf(analysis_data):

    try:
        # Save in current project folder
        output_path = "resume_analysis.pdf"

        c = canvas.Canvas(output_path, pagesize=letter)

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "Resume Analysis Report")

        c.setFont("Helvetica", 10)

        y = 720

        c.drawString(
            50,
            y,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        y -= 20

        c.drawString(
            50,
            y,
            f"Resume Score: {analysis_data['score']}/100"
        )

        y -= 20

        c.drawString(
            50,
            y,
            f"Top Job Match: {analysis_data['top_job']}"
        )

        y -= 20

        c.drawString(
            50,
            y,
            f"Skills Found: {', '.join(analysis_data['skills'])}"
        )

        y -= 30

        c.setFont("Helvetica-Bold", 12)

        c.drawString(50, y, "Job Match Scores:")

        y -= 20

        c.setFont("Helvetica", 10)

        for job, score in analysis_data['job_scores'].items():

            c.drawString(
                70,
                y,
                f"{job}: {score}%"
            )

            y -= 15

        c.save()

        return f"PDF saved successfully as: {output_path}"

    except Exception as e:

        return f"Error generating PDF: {str(e)}"