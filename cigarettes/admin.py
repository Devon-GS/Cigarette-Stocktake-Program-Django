from django.contrib import admin
from .models import Cigarette

class CigaretteAdmin(admin.ModelAdmin):
    ordering = ['product_name']

admin.site.register(Cigarette, CigaretteAdmin)