from django.db import models
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to = 'images')

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('detail', kwargs={'id': self.id})

# proxy model -> https://docs.djangoproject.com/en/3.2/topics/db/models/#proxy-models
class RecentPosts(Post): # model is plural because its a proxy model, it makes more sense in plural
    class Meta:
        proxy = True
        ordering = ['-date']
