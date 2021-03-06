from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    content = models.TextField('Текст комментария')
    date_published = models.DateTimeField('Дата создания', auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='answers', verbose_name='Родительский комментарий', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', blank=False, null=False)

    def __str__(self):
        return f"{self.content} {self.date_published}"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['date_published']