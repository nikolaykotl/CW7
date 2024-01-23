
from django.db import models

from config import settings
from users.models import NULLABLE


# Create your models here.


class Habit(models.Model):

    name = models.CharField(max_length=120, verbose_name='название')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name='пользователь')
    related_habit = models.ForeignKey('self',
                                      on_delete=models.CASCADE,
                                      verbose_name='связанная привычка',
                                      **NULLABLE)
    action = models.CharField(max_length=120, verbose_name='действие')
    start_time = models.DateTimeField(auto_now=True,
                                      verbose_name='время начала выполнения',
                                      **NULLABLE)
    place = models.CharField(max_length=75, verbose_name='место')
    is_pleasant = models.BooleanField(default=False,
                                      verbose_name='признак приятной привычки',
                                      **NULLABLE)
    periodicity = models.IntegerField(verbose_name='периодичность', **NULLABLE)
    award = models.CharField(max_length=75, verbose_name='вознаграждение',
                             **NULLABLE)
    time_to_complete = models.IntegerField(verbose_name='время на выполнение',
                                           default=120)
    is_public = models.BooleanField(default=False,
                                    verbose_name='признак публичности',
                                    **NULLABLE)

    def __srt__(self):
        return f'{self.name}: Я буду {self.action}' \
               f' {self.time_to_complete} в {self.place}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
