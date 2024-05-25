from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(VerificationCode)
admin.site.register(VideoTest)
admin.site.register(Video)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Comment)