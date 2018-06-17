# blog/models.py

import re
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User



def lnglat_validator(value):
    if not re.match(r'^([+-]?\d+\.?\d*),([+-]?\d+\.?\d*)$', value):
        raise ValidationError('Invalid LngLat Type')


class Post(models.Model):

    STATUS_CHOICES = (
        ('d', 'draft'),
        ('p', 'published'),
        ('w', 'withdraw')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    author = models.CharField(max_length=20, verbose_name='작성자')
    title = models.CharField(max_length=100, verbose_name='제목',
                             help_text='포스팅 제목을 입력해 주세요. 100자 내외')    # 길이 제한이 있는 문자열
    content = models.TextField(verbose_name='내용')                # 길이 제한이 없는 문자열

    photo = models.ImageField(blank=True)

    tags = models.CharField(max_length=100, blank=True)
    langlat = models.CharField(max_length=50, blank=True,
                               validators=[lnglat_validator],
                               help_text='위도/경도 포맷으로 입력'
                               )

    tag_set = models.ManyToManyField('Tag', blank=True)     # Model Class를 문자열로도 지정 가능함. '' 같은 앱에 있는 Class와 Relation을 맺는다는 의미.
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:     # 기본 정렬을 id 역순으로 정렬
        ordering = ['-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])

class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name