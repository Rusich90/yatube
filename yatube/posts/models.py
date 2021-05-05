from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Текст', help_text='Введите текст')
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name="posts",
                              verbose_name='Группа',
                              help_text='Выберите группу для поста (необязательно)',
                              blank=True,
                              null=True)
    image = models.ImageField(
        upload_to='posts/',
        verbose_name='Изображение',
        help_text='Загрузите изображение (необязательно)',
        blank=True,
        null=True)

    def __str__(self):
        # выводим текст поста
        return self.text

    class Meta:
        ordering = ['-pub_date']


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст', help_text='Введите текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created = models.DateTimeField("date comment", auto_now_add=True, db_index=True)

    def __str__(self):
        # выводим текст поста
        return self.text
    class Meta:
        ordering = ['-created']


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    class Meta:
        unique_together = ['user', 'following']
