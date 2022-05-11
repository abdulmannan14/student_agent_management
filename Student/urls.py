from django.urls import path, reverse
from . import views as student_views

urlpatterns = [
    path("", student_views.index, name="student-index"),
    path('students/all', student_views.all_students, name='all-students'),
    path('add', student_views.add_student, name='add-student'),
    path('edit/<int:pk>', student_views.edit_student, name='edit-student'),
    path('history/<int:pk>', student_views.history_student, name='history-student'),
    path('delete/<int:pk>', student_views.delete_student, name='delete-student'),

    # JS URLS
    path('get_agent_commission', student_views.get_agent_commission, name='get-agent-commission'),
    path('get_student_fee_details', student_views.get_student_fee_details, name='get-student-fee-details'),
    # FEE Related
    path('add/fee', student_views.add_fee, name='add-fee'),
    #     =====================STUDENT REPORT=============================================
    path('student/report', student_views.student_report, name='student-report'),
]


def all_student():
    return reverse("all-students")


def add_student():
    return reverse("add-student")


def edit_student(pk: int):
    return reverse("edit-student", kwargs={"pk": pk})


def history_student(pk: int):
    return reverse("history-student", kwargs={"pk": pk})


def delete_student(pk: int):
    return reverse("delete-student", kwargs={"pk": pk})