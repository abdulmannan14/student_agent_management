from django.urls import path, reverse
from . import views as agent_views

urlpatterns = [
    path('agent/all', agent_views.all_agents, name='all-agent'),
    path('add', agent_views.add_agent, name='add-agent'),
    path('edit/<int:pk>', agent_views.edit_agent, name='edit-agent'),
    path('delete/<int:pk>', agent_views.delete_agent, name='delete-agent'),
    path('archive/<int:pk>', agent_views.archive_agent, name='archive-agent'),
    path('unarchive/<int:pk>', agent_views.unarchive_agent, name='unarchive-agent'),
    # ====================COMMISSION URLS==================
    path('add/commission/<int:pk>', agent_views.add_commission, name='add-commission'),
    path('edit/commission/<int:pk>', agent_views.edit_commission, name='edit-agent-commission'),
    path('delete/commission/<int:pk>', agent_views.delete_commission, name='delete-agent-commission'),
    #     ============================JS URLS======================================
    path('agent/detials', agent_views.get_student_agent_details, name='get-student-agent-details'),
    #     ===========================AGENT STUDENTS AND HISTORY URLS==================================
    path('agent/student/<int:pk>', agent_views.agent_students, name='agent-students'),
    path('agent/student/courses/<int:pk>', agent_views.agent_students_courses, name='agent-student-courses'),
    path('commission/history/<int:pk>', agent_views.commission_history, name='commission-history'),
    path('send/mail/<int:pk>/', agent_views.send_mail, name='send-mail-agent'),
    path('archived-agent', agent_views.archived_agent, name='archived-agent'),
    path('export-agent-report/<int:pk>', agent_views.export_individual_agent_details, name='export-agent-report'),
    path('export-agent-all-student/<int:pk>', agent_views.export_agent_all_student,
         name='export-agent-all-student'),
    path('export-agents', agent_views.export_agents_details, name='export-agents'),
]


def all_agent():
    return reverse("all-agent")


def add_agent():
    return reverse("add-agent")


def edit_agent(pk: int):
    return reverse("edit-agent", kwargs={"pk": pk})


def edit_agent_commission(pk: int):
    return reverse("edit-agent-commission", kwargs={"pk": pk})


def delete_agent_commission(pk: int):
    return reverse("delete-agent-commission", kwargs={"pk": pk})


def delete_agent(pk: int):
    return reverse("delete-agent", kwargs={"pk": pk})


def agent_students(pk: int):
    return reverse("agent-students", kwargs={"pk": pk})


def commission_history(pk: int):
    return reverse("commission-history", kwargs={"pk": pk})


def send_mail_agent(pk: int):
    return reverse("send-mail-agent", kwargs={"pk": pk})


def archive_agent(pk: int):
    return reverse("archive-agent", kwargs={"pk": pk})


def unarchive_agent(pk: int):
    return reverse("unarchive-agent", kwargs={"pk": pk})


def agentstudentcourses(pk: int):
    return reverse("agent-student-courses", kwargs={"pk": pk})
