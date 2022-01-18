from django.contrib import admin
from .models import Lead, User, Agent

# Register your models here.
admin.site.register(User)
admin.site.register(Agent)
admin.site.register(Lead)