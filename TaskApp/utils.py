from .models import Task, FinishedTask, Employee
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings






def send_email_to_employee(email, new_email):
    """
    Sends a customized welcome email to the client upon signup.
    """
    from_email = settings.EMAIL_HOST_USER

    subject = "Welcome to ETMD Pvt Ltd."
    message = f"""
    Dear {email},

    I trust this message finds you in good health. It is my distinct pleasure to welcome you to ETMD Pvt Ltd, an esteemed platform dedicated to excellence.

    Your participation is highly valued, and we are delighted to have you as part of our team.

    Your new email address for communication is: {new_email}

    ETMD Pvt Ltd, under the leadership of ETMD, Director, is committed to fostering a transformative and enriching experience. We firmly believe that your presence will contribute significantly to the vibrancy of our community.

    For any inquiries or assistance, please do not hesitate to reach out to ETMD directly at {from_email}.

    We appreciate your consideration of our invitation and eagerly anticipate the prospect of welcoming you into the ETMD Pvt Ltd community.

    Best regards,

    ETMD
    Director, ETMD Pvt Ltd
    {from_email}
    """
    send_mail(subject, message, from_email, [email], fail_silently=False)


def send_task_assignment_email(title, description, email):
    subject = f"New Task Assigned : {title}"
    message = f"""
        Hello {email},

        You have been assigned to new task.

        Title:{title}

        Description:{description}

        Please log in to the system to view more details.
        """
    send_mail(subject,message,None,[email],fail_silently=False)




