from django.contrib import admin
from .models import Post,Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk','title', 'slug', 'author', 'publish', 'status', 'image') #display list details 
    list_filter = ('status', 'created', 'publish', 'author') # add_filter list to side bard 
    search_fields = ('title', 'body') # add search_feild to search among the items
    prepopulated_fields = {'slug': ('title',)} #autocomplete the slug with typing in title
    raw_id_fields = ('author',)
    date_hierarchy = 'publish' # addd date topbar to choose date 
    ordering = ['status', 'publish'] 

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post','active') #display list details 
    list_filter = ('active', 'created', 'updated') # add_filter list to side bard 
    search_fields = ('name', 'email','body') # add search_feild to search among the items

admin.site.register(Comment, CommentAdmin)