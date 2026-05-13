from django.db import models
from django.utils import timezone

# Create your models here.
class Source(models.Model):
  name = models.CharField(max_length=128)
  url = models.URLField(max_length=1024)
  crawl_interval_minutes = models.PositiveIntegerField()
  crawled_at = models.DateTimeField()
  created_at = models.DateTimeField(default=timezone.now())

  def __str__(self):
    return f'{self.name}: {self.url} ({self.id})'


class Notice(models.Model):
  source_id = models.ForeignKey("Source", on_delete=models.CASCADE)
  url = models.URLField(max_length=1024)
  hash = models.CharField(max_length=256)
  title = models.CharField(max_length=256)
  content = models.TextField()
  publisher = models.CharField(max_length=256)
  published_at = models.DateTimeField()
  updated_at = models.DateTimeField()
  created_at = models.DateTimeField(default=timezone.now())

  def __str__(self):
    return f'{self.title}({self.id})'


class SourceSubscription(models.Model):
  user_id = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
  source_id = models.ForeignKey("Source", on_delete=models.CASCADE)

  def __str__(self):
    return f'User {self.user_id} -> Source {self.source_id} ({self.id})'


class InboxNotice(models.Model):
  user_id = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
  notice_id = models.ForeignKey("Notice", on_delete=models.CASCADE)
  relevance_score = models.FloatField()
  matched_keywords = models.TextField()
  reason = models.TextField()
  is_read = models.BooleanField()

  def __str__(self):
    return f'User {self.user_id} -> Notice {self.notice_id} {self.id}'
