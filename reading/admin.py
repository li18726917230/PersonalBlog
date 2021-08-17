from django.contrib import admin
from .models import Read


# Register your models here.
@admin.register(Read)
class ReadAdmin(admin.ModelAdmin):
    list_display = ('read_num','create_time')
