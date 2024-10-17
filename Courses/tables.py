"""this file has the tables of vehicles that are using in company and employees views"""
import django_tables2 as tables
from django.utils.html import format_html
from . import models as course_models, urls as course_urls
from acmimanagement.utils import delete_action
from acmimanagement import utils as backend_utils
from Agent import models as agent_models


class CourseTable(tables.Table):
    actions = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = course_models.Course
        fields = ['name', 'description', 'weeks','months', 'quarters']

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{delete}".format(
            update=course_urls.edit_course(record.pk),
            delete=delete_action(course_urls.delete_course(record.pk), record.name),
        )
        )
