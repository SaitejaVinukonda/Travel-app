from django.contrib import admin
from .models import Bus
from .models import Tour

# Register your models 
admin.site.register(Bus)
admin.site.register(Tour)

