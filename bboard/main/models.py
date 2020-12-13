from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal
from django.db.models.signals import post_save

from .utilities import send_activation_notification, get_timestamp_path, send_new_comment_notification

user_registrated = Signal(providing_args=['instance'])


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name='Прошёл активацию?'
    )
    send_messages = models.BooleanField(
        default=True,
        verbose_name='Слать оповещения о новых комментариях?'
    )

    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


# Функция получатель
def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


# Подключение получателяк сигналу
user_registrated.connect(user_registrated_dispatcher)


class Rubric(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True,
        unique=True,
        verbose_name='Название'
    )
    order = models.IntegerField(
        default=0,
        db_index=True,
        verbose_name='Порядок'
    )
    super_rubric = models.ForeignKey(
        'SuperRubric',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Надрубрика'
    )


class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(Rubric):
    objects = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'


class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):
    objects = SubRubricManager()

    def __str__(self):
        return '%s - %s' % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'


class Bb(models.Model):
    """Модель объявления"""
    rubric = models.ForeignKey(
        SubRubric,
        on_delete=models.PROTECT,
        verbose_name='Рубрика'
    )
    title = models.CharField(
        max_length=100,
        verbose_name='Название товара'
    )
    content = models.TextField(
        verbose_name='Описание товара'
    )
    price = models.IntegerField(
        default=0,
        verbose_name='Цена товара'
    )
    contacts = models.TextField(
        verbose_name='Контакты'
    )
    image = models.ImageField(
        blank=True,
        upload_to=get_timestamp_path,
        verbose_name='Основная иллюстрация к объявлению'
    )
    author = models.ForeignKey(
        AdvUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь оставивший объявление'
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name='Выводить в списке?'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата и время публикации объявления'
    )

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-created_at']


class AdditionalImage(models.Model):
    """"Дополнительные изображения к объявлению"""
    bb = models.ForeignKey(
        Bb,
        on_delete=models.CASCADE,
        verbose_name='Объявление'
    )
    image = models.ImageField(
        upload_to=get_timestamp_path,
        verbose_name='Изображение'
    )

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'


class Comment(models.Model):
    """Модель комментария под объявлением"""
    bb = models.ForeignKey(
        Bb,
        on_delete=models.CASCADE,
        verbose_name='Объявление'
    )
    author = models.CharField(
        max_length=30,
        verbose_name='Автор'
    )
    content = models.TextField(
        verbose_name='Содержание'
    )
    is_activate = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name='Выводить на экран?'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Опубликован'
    )

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['created_at']


def post_save_dispatcher(sender, **kwargs):
    """Запускается пост-сигналом, отправляет письмо о новом комментарии"""
    author = kwargs['instance'].bb.author
    if kwargs['created'] and author.send_messages:
        send_new_comment_notification(kwargs['instance'])


post_save.connect(post_save_dispatcher, sender=Comment)
