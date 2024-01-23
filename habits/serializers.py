from rest_framework import serializers
from habits.models import Habit
from habits.validators import Related_or_Award_HabitValidator, \
    Time_to_Complete_HabitValidator, \
    Related_is_pleasant_HabitValidator, \
    Pleasant_HabitValidator, Periodicity_HabitValidator


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [Related_or_Award_HabitValidator(),
                      Time_to_Complete_HabitValidator(),
                      Related_is_pleasant_HabitValidator(),
                      Pleasant_HabitValidator(),
                      Periodicity_HabitValidator()]
