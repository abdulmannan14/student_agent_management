from django.contrib import admin
from django.apps import apps
from import_export.admin import ImportExportModelAdmin


def set_admin(_class, search_fields: tuple, ordering: tuple, list_display: tuple):
    class_name = _class.__name__ + 'Admin'
    Meta = type('Meta', (object,), {'model': _class})

    AdminClass = type(class_name,
                      (ImportExportModelAdmin,),
                      {
                          'Meta': Meta,
                          'search_fields': search_fields,
                          'ordering': ordering,
                          'list_display': list_display
                          # "sayHello": lambda self: "Hi, I am " + self.name
                      }
                      )
    admin.site.register(_class, AdminClass)
    return AdminClass


def set_app_models_to_admin(app_name: str):
    classes = []
    app = apps.get_app_config(app_name)
    for model_name, model in app.models.items():
        fields = []
        for field in model._meta.fields:
            fields.append(field.name)
        fields = tuple(fields)
        admin_class = set_admin(model, fields, fields, fields)
        classes.append(admin_class)
    return classes


from django.conf import settings

for app in settings.MY_APPS:
    set_app_models_to_admin(app)
