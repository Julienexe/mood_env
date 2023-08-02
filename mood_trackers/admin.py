from django.contrib import admin
from .models import Journal, Mood, User, Topic, Article

admin.site.register(Journal)
admin.site.register(Mood)
admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Article)
# Register your models here.
