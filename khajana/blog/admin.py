from django.contrib import admin
from .models import Post,Comment,City,Subtitle
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(City)
admin.site.register(Subtitle)