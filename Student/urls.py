from django.urls import path, reverse
from . import views as student_views

urlpatterns = [
    path("", student_views.user_login, name="login"),
    path("logout", student_views.user_logout, name="logout"),
    path("change-password", student_views.user_change_password, name="change-pass"),
    path("index", student_views.index, name="student-index"),
    path('students/all', student_views.all_students, name='all-students'),
    path('add', student_views.add_student, name='add-student'),
    path('edit/<int:pk>', student_views.edit_student, name='edit-student'),
    path('history/<int:pk>', student_views.history_student, name='history-student'),
    path('delete/<int:pk>', student_views.delete_student, name='delete-student'),

    # JS URLS
    path('get_student_commission', student_views.get_student_commission, name='get-student-commission'),
    path('get_student_fee_details', student_views.get_student_fee_details, name='get-student-fee-details'),
    # FEE Related
    path('add/fee', student_views.add_fee, name='add-fee'),
    path('edit/fee/<int:pk>', student_views.edit_fee, name='edit-student-fee'),
    path('delete/fee/<int:pk>', student_views.delete_fee, name='delete-student-fee'),
    #     =====================STUDENT REPORT=============================================
    path('student/report', student_views.student_report, name='student-report'),
    # ==================================STUDENT FEE REFUND==================================
    path('refunded-student', student_views.refunded_student, name='refunded-student'),
    # path('student/fee-refund/<int:pk>', student_views.student_fee_refund, name='student-fee-refund'),
    path('student/fee-refund/<int:pk>', student_views.student_fee_refund, name='student-fee-refund'),
    # ===========================SEND MAIL TO STUDENT=================================================
    path('student/send/warning/mail/<int:pk>', student_views.send_mail_to_student, name='send-mail-to-student'),

]


def all_student():
    return reverse("all-students")


def add_student():
    return reverse("add-student")


def edit_student(pk: int):
    return reverse("edit-student", kwargs={"pk": pk})


def edit_student_fee(pk: int):
    return reverse("edit-student-fee", kwargs={"pk": pk})


def delete_student_fee(pk: int):
    return reverse("delete-student-fee", kwargs={"pk": pk})


def history_student(pk: int):
    return reverse("history-student", kwargs={"pk": pk})


def delete_student(pk: int):
    return reverse("delete-student", kwargs={"pk": pk})


def user_login():
    return reverse("login")


def student_fee_refund(pk: int):
    return reverse('student-fee-refund', kwargs={'pk': pk})


def send_mail_student(pk: int):
    return reverse('send-mail-to-student', kwargs={'pk': pk})
