from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post, Comment, Tag

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content_size','status','created_at', 'updated_at']

    actions = ['make_published', 'make_draft', 'make_withdraw']
    
    def content_size(self, post):
        return mark_safe('<strong>{}</strong>글자'.format(len(post.content)))
    content_size.short_description = '글자수'


    def make_published(self, request, queryset):
        updated_count = queryset.update(status='p')     # QuerySet.update
        self.message_user(request, '{}건의 포스팅을 published 상태로 변경'.format(updated_count)) # django message framework 활용
    make_published.short_description = '지정 포스팅을 Published로 변경합니다.'


    def make_draft(self, request, queryset):
        updated_count = queryset.update(status='d')  # QuerySet.update
        self.message_user(request, '{}건의 포스팅을 Draft 상태로 변경'.format(updated_count))  # django message framework 활용
    make_draft.short_description = '지정 포스팅을 Draft로 변경합니다.'


    def make_withdraw(self, request, queryset):
        updated_count = queryset.update(status='w')  # QuerySet.update
        self.message_user(request, '{}건의 포스팅을 Withdraw 상태로 변경'.format(updated_count))  # django message framework 활용

    make_withdraw.short_description = '지정 포스팅을 Withdraw로 변경합니다.'

    def __str__(self):
        return self.title

@admin.register(Comment)
class CommnetAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_id', 'message', 'created_at', 'updated_at']
    def __str__(self):
        return self.message

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

    def __str__(self):
        return self.name

