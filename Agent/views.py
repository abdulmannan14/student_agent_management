from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework.generics import get_object_or_404
import datetime
import Menu.models
from limoucloud_backend import utils as backend_utils
# from Restaurant import models as restaurant_models
from . import tables as agent_table, forms as agent_form, models as agent_models


# Create your views here.

def all_agents(request):
    agents = agent_models.AgentModel.objects.all()
    sort = request.GET.get('sort', None)
    if sort:
        agents = agents.order_by(sort)
    agents = agent_table.AgentTable(agents)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "Add Agent",
                "href": reverse("add-agent"),
                "icon": "fa fa-plus"
            },
        ],
        # 'vehicle_count': len(vehicles),
        "page_title": "All Agents",
        "table": agents,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['agent'],
        },

    }
    return render(request, "dashboard/list-entries.html", context)


def add_agent(request):
    if request.method == "POST":
        form = agent_form.AgentForm(request.POST)
        if form.is_valid():
            agent = form.save()
            messages.success(request, f"{agent.name} Added Successfully as Agent!")
            return redirect("all-agent")
    else:
        form = agent_form.AgentForm()
    context = {
        "page_title": "Add agent",
        "form1": form,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('all-agent'),
        'nav_conf': {
            'active_classes': ['vehicles'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


def edit_agent(request, pk):
    agent = get_object_or_404(agent_models.AgentModel, pk=pk)
    if request.method == "POST":
        form = agent_form.AgentForm(request.POST, instance=agent)
        if form.is_valid():
            agent = form.save()
            messages.success(request, f"Agent Updated Successfully")
            return redirect('all-agent')
    else:
        form = agent_form.AgentForm(instance=agent)
    context = {
        "form1": form,
        "page_title": "Edit Agent",
        "subtitle": "Here you can Edit the Agent",
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('all-agent'),
        'nav_conf': {
            'active_classes': ['agent'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


def delete_agent(request, pk):
    agent = get_object_or_404(agent_models.AgentModel, pk=pk)
    backend_utils._delete_table_entry(agent)
    messages.success(request, f"{agent.name} is Deleted Successfully!")
    return redirect('all-agent')
