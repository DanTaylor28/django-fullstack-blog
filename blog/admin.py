from django.contrib import admin
# importing the post class from modesl.property
from .models import Post, Comment
# tells admin field what panel we want to use summernote for ie content field
from django_summernote.admin import SummernoteModelAdmin


# This @ line of code now adds the Post and PostAdmin class to our admin
# site unlike the commented out code below which just adds the Post class.
# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    # the below code, automatically generates slug field using title field
    # and dictionary method
    prepopulated_fields = {'slug': ('title',)}
    # adds filter box to the right of admin page to organise posts
    list_filter = ('status', 'created_on')
    # displays blog posts more orderly and adds a search bar
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    # saying our content field which is currently django text field
    # wants to use summernote instead
    summernote_fields = ('content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ['name', 'email_address', 'body']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
