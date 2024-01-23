from rest_framework.serializers import ValidationError


class Related_or_Award_HabitValidator:
    """Исключить одновременный выбор связанной
     привычки и указания вознаграждения"""
    def __call__(self, attrs):
        related_habit = attrs.get('related_habit')
        award = attrs.get('award')

        if related_habit and award:
            raise ValidationError('Вы должны указать либо связанную привычку,'
                                  ' либо признак приятной привычки, '
                                  'или указать принак приятной привычки')


class Time_to_Complete_HabitValidator:
    """Время выполнения должно быть не больше 120 секунд."""
    def __call__(self, attrs):
        time_to_complete = attrs.get('time_to_complete')
        if time_to_complete > 120:
            raise ValidationError('Время на выполнение не более 2х минут')


class Related_is_pleasant_HabitValidator:
    """В связанные привычки могут попадать только
     привычки с признаком приятной привычки"""
    def __call__(self, attrs):
        related_habit = attrs.get('related_habit')
        if related_habit and not related_habit.is_pleasant:
            raise ValidationError('В связанные привычки могут попадать только'
                                  ' привычки с признаком приятной привычки')
        return attrs


class Pleasant_HabitValidator:
    """У приятной привычки не может быть
     вознаграждения или связанной привычки."""
    def __call__(self, attrs):
        is_pleasant = attrs.get('is_pleasant')
        related_habit = attrs.get('related_habit')
        award = attrs.get('award')
        if is_pleasant:
            if related_habit or award:
                raise ValidationError(
                    'У приятной привычки не может быть'
                    ' вознаграждения или связанной привычки.')


class Periodicity_HabitValidator:
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней"""
    def __call__(self, attrs):
        periodicity = attrs.get('periodicity')
        if periodicity > 7:
            raise ValidationError('Нельзя выполнять привычку реже,'
                                  ' чем 1 раз в 7 дней')
