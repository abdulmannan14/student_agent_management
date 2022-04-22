from django.urls import path, reverse
from . import views as agent_views

urlpatterns = [
    path('agent/all', agent_views.all_agents, name='all-agent'),
    path('add', agent_views.add_agent, name='add-agent'),
    path('edit/<int:pk>', agent_views.edit_agent, name='edit-agent'),
    path('delete/<int:pk>', agent_views.delete_agent, name='delete-agent'),

]


def all_agent():
    return reverse("all-agent")


def add_agent():
    return reverse("add-agent")


def edit_agent(pk: int):
    return reverse("edit-agent", kwargs={"pk": pk})


def delete_agent(pk: int):
    return reverse("delete-agent", kwargs={"pk": pk})
