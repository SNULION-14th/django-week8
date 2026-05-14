from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
class Source(models.Model):
  name = models.CharField(max_length=128)
  url = models.URLField(max_length=1024)
  crawl_interval_minutes = models.PositiveIntegerField(default=60)
  crawled_at = models.DateTimeField(null=True)
  created_at = models.DateTimeField(default=timezone.now)

  subscription_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subscription_sources', through='SourceSubscription')

  def __str__(self):
    return f'{self.name}: {self.url} ({self.id})'


class Notice(models.Model):
  source = models.ForeignKey("Source", on_delete=models.CASCADE)
  url = models.URLField(max_length=1024)
  content_hash = models.CharField(max_length=256)
  title = models.CharField(max_length=256)
  content = models.TextField()
  publisher = models.CharField(max_length=256)
  published_at = models.DateTimeField()
  updated_at = models.DateTimeField(null=True)
  created_at = models.DateTimeField(default=timezone.now)

  inbox_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='inbox_notices', through='InboxNotice')

  def __str__(self):
    return f'{self.title}({self.id})'


class SourceSubscription(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  source = models.ForeignKey("Source", on_delete=models.CASCADE)
  created_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f'User {self.user} -> Source {self.source} ({self.id})'


class InboxNotice(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  notice = models.ForeignKey("Notice", on_delete=models.CASCADE)
  relevance_score = models.FloatField()
  matched_keywords = models.TextField()
  reason = models.TextField()
  is_read = models.BooleanField(default=False)

  def __str__(self):
    return f'User {self.user} -> Notice {self.notice} {self.id}'
