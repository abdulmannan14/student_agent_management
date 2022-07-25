from django.urls import path, reverse
from . import views as course_views

urlpatterns = [
    path('course/all', course_views.all_courses, name='all-course'),
    path('add', course_views.add_course, name='add-course'),
    path('edit/<int:pk>', course_views.edit_course, name='edit-course'),
    path('delete/<int:pk>', course_views.delete_course, name='delete-course'),
    path('course_quarters_get', course_views.get_course_quarters, name='get_course_quarters'),


]


def all_course():
    return reverse("all-course")

def add_course():
    return reverse("add-course")

def edit_course(pk: int):
    return reverse("edit-course", kwargs={"pk": pk})

def delete_course(pk: int):
    return reverse("delete-course", kwargs={"pk": pk})

