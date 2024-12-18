from django.urls import path, reverse
from . import views as agent_views

urlpatterns = [
    path('agent/all', agent_views.all_agents, name='all-agent'),
    path('add', agent_views.add_agent, name='add-agent'),
    path('edit/<int:pk>', agent_views.edit_agent, name='edit-agent'),
    path('delete/<int:pk>', agent_views.delete_agent, name='delete-agent'),
    # ====================COMMISSION URLS==================
    path('add/commission', agent_views.add_commission, name='add-commission'),
    path('edit/commission/<int:pk>', agent_views.edit_commission, name='edit-agent-commission'),
    path('delete/commission/<int:pk>', agent_views.delete_commission, name='delete-agent-commission'),
    #     ============================JS URLS======================================
    path('agent/detials', agent_views.get_student_agent_details, name='get-student-agent-details'),
    #     ===========================AGENT STUDENTS AND HISTORY URLS==================================
    path('agent/student/<int:pk>', agent_views.agent_students, name='agent-students'),
    path('commission/history/<int:pk>', agent_views.commission_history, name='commission-history'),
    path('send/mail/<int:pk>/', agent_views.send_mail, name='send-mail-agent'),

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
