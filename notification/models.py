from django.db import models
from django.conf import settings
# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    type = models.CharField(max_length=100, choices=[('remainder','Remainder'), ('alert', 'Alert'), ('update', 'Update')])

    def __str__(self):
        return f"{self.user.username} - {self.type}"