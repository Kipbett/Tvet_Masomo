from django.contrib import admin

from .models import Department, CustomUser, Course, Unit, Document
# Register your models here.
admin.site.register(Department)
admin.site.register(CustomUser)
admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Document)