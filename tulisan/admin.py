from django.contrib import admin
from .models import Karya
from .models import Profile
admin.site.register(Profile)
# Ini baris paling penting agar menu "Karyas" muncul
admin.site.register(Karya)