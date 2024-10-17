from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
import sys
from django import forms
from django.utils.html import format_html

from acmimanagement.settings import from_email


def success_response_fe(data=None, msg='Operation Success', taxes=None):
    return {
        'success': True,
        'message': msg,
        'data': data,
        'taxes': taxes
    }


def failure_response_fe(errors=None, msg='Operation Failure'):
    return {
        'success': False,
        'message': msg,
        'errors': errors
    }


def success_response(status_code=None, data=None, msg='Operation Success!'):
    response = {
        'success': True,
        'message': msg,
        'data': data
    }
    if status_code:
        response["status_code"] = status_code
    return response


def failure_response(status_code=None, errors=None, msg='Operation Failure'):
    response = {
        'success': False,
        'message': msg,
        'errors': errors
    }
    if status_code:
        response["status_code"] = status_code
    return response


def delete_action(reverse, name):
    return format_html(
        '<button class="btn text-danger btn-sm pull-right" data-toggle="modal" data-target="#exampleModal" '
        'data-whatever="{}" data-name="{}"><i class="fa fa-trash"></i></button>',
        reverse, name)


def archive_action(reverse, name, modal_name='archiveModal'):
    return format_html(
        '<button class="btn text-blue btn-sm pull-right" data-toggle="modal" data-target="#{}" '
        'data-url="{}" data-name="{}"><i class="fa fa-archive"></i></button>',
        modal_name, reverse, name)


def undo_archive_action(reverse, name):
    return format_html(
        '<button class="btn text-blue btn-sm pull-right" data-toggle="modal" data-target="#UndoarchiveModal" '
        'data-url="{}" data-name="{}"><i class="fa fa-undo"></i></button>',
        reverse, name)


def detail_action(reverse, name):
    return format_html(
        '<button class="btn text-warning btn-sm pull-right" data-toggle="modal" data-target="#detailModal" '
        'data-url="{}" data-name="{}"><i class="fa fa-eye"></i></button>',
        reverse, name)


def _delete_table_entry(row):
    row.delete()
    return True
