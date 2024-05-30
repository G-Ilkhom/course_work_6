from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    views_count = models.IntegerField(default=0)
    publication_date = models.DateTimeField(auto_now_add=True)
    publication_sign = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
