from django.contrib import admin
from .models import Comment


# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    exclude = ('temp_haineux', 'temp_offensif', 'temp_non_offensif')

admin.site.register(Comment, CommentAdmin)
