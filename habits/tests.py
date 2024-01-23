from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class HabitTestCases(APITestCase):
    """Тест кейс на создание новой привычки"""
    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.create(email='test@test.test', is_active=True)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)

        self.habit_01 = Habit.objects.create(
            name="Test1",
            user=self.user,
            action="Test1",
            start_time="2024-01-01T08:10:00",
            place="Test1",
            is_pleasant="True",
            periodicity=2,
            time_to_complete=120
        )
        self.habit_02 = Habit.objects.create(
            name="Test2",
            user=self.user,
            action="Test2",
            start_time="2024-01-02T08:10:00",
            place="Test2",
            is_pleasant="True",
            periodicity=2,
            time_to_complete=120,
            is_public=True
        )

        self.habit_03 = Habit.objects.create(
            name="Test3",
            user=self.user,
            action="Test3",
            start_time="2023-01-03T08:10:00",
            place="Test3",
            is_pleasant="True",
            time_to_complete=120,
            periodicity=2
        )

    def test_create_habit(self):
        """Тест создание привычки"""
        data = {
            "name": "Test",
            "user": self.user.id,
            "action": "Test",
            "start_time": "2024-01-01T05:10:00",
            "place": "Test",
            "is_pleasant": "True",
            "periodicity": 2,
            "time_to_complete": 120,
            "is_public": True,
        }

        response = self.client.post(reverse('habits:create_habit'),
                                    data=data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Habit.objects.all().exists()
        )

    def test_habit_list(self):
        """Тест на чтение списка привычек"""
        responce = self.client.get(
            reverse('habits:list_habit'),
        )

        self.assertEqual(
            responce.status_code,
            status.HTTP_200_OK
        )

    def test_single_habits_list(self):
        """Тест на чтение одной привычки"""
        responce = self.client.get(
            reverse('habits:detail_habit', args=[self.habit_02.id]),
        )

        self.assertEqual(
            responce.status_code,
            status.HTTP_200_OK
        )

    def test_update_single_habits(self):
        """Тест Обновление одной привычки"""

        self.client = APIClient()
        self.user = User.objects.create(
            email='test1@test.test',
            password='test',
        )
        self.client.force_authenticate(user=self.user)
        self.user.set_password('test')
        self.user.save()

        self.habit_update = Habit.objects.create(
            name="Test1",
            user=self.user,
            action="Test1",
            start_time="2023-01-01T08:10:00",
            place="Test1",
            is_pleasant="True",
            time_to_complete=120,
            periodicity=2
        )
        data = {
            "name": "Test update",
            "action": "Test update",
            "start_time": "2024-01-02T08:10:00",
            "place": "Test update",
            "time_to_complete": 34,
            "periodicity": 4
        }
        response = self.client.patch(
            reverse('habits:update_habit', args=[self.habit_update.id]),
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_habit_delete(self):
        """Тест удаление одной привычки"""

        response = self.client.delete(
            reverse('habits:delete_habit', args=[self.habit_01.id])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class HabitValidatorCreateTestCase(APITestCase):
    """Тесты проверки Валидаторов"""
    def setUp(self) -> None:

        self.client = APIClient()
        self.user = User.objects.create(email='test@test.test', is_active=True)
        self.user.set_password('test_password')
        self.client.force_authenticate(user=self.user)
        self.user.save()

        self.habit_02 = Habit.objects.create(
            name="Test2",
            user=self.user,
            action="Test2",
            start_time="2024-01-02T08:10:00",
            place="Test2",
            is_pleasant="True",
            time_to_complete=120,
            is_public=True,
            periodicity=2
        )
        self.habit_no_pleasant = Habit.objects.create(
            name="Test2",
            user=self.user,
            action="Test2",
            start_time="2024-01-02T08:10:00",
            place="Test2",
            time_to_complete=120,
            is_public=True,
            periodicity=2
        )

    def test_Related_or_Award_HabitValidator(self):
        """Тест на ограничение: Исключить одновременный выбор
         связанной привычки и указания вознаграждения"""
        data = {
            "name": "Test",
            "user": self.user.id,
            "action": "Test",
            "start_time": "2024-01-02T08:00:00",
            "place": "Test",
            "time_to_complete": 100,
            "periodicity": 4,
            "award": "test",
            "related_habit": self.habit_02.id
        }

        responce = self.client.post(
            reverse('habits:create_habit'),
            data=data
        )

        self.assertEqual(
            responce.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_time_to_complete_HabitValidator(self):
        """Тест на ограничение: время выполнения
         должно быть не больше 120 секунд."""
        data = {
            "name": "Test",
            "user": self.user.id,
            "action": "Test",
            "start_time": "2024-01-02T08:00:00",
            "place": "Test",
            "is_pleasant": "True",
            "time_to_complete": 121,
            "periodicity": 4
        }
        responce = self.client.post(
            reverse('habits:create_habit'),
            data=data
        )

        self.assertEqual(
            responce.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_Related_is_pleasant_HabitValidator(self):
        """Тест на ограничение: В связанные привычки могут
         попадать только привычки с признаком приятной привычки"""
        data = {
            "name": "Test",
            "user": self.user.id,
            "action": "Test",
            "start_time": "2024-01-02T08:00:00",
            "place": "Test",
            "time_to_complete": 100,
            "periodicity": 4,
            "award": "test",
            "related_habit": self.habit_no_pleasant.id
        }
        responce = self.client.post(
            reverse('habits:create_habit'),
            data=data
        )

        self.assertEqual(
            responce.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_Pleasant_HabitValidator(self):
        """Тест на ограничение: У приятной привычки не может
         быть вознаграждения или связанной привычки"""
        data = {
            "name": "Test",
            "user": self.user.id,
            "action": "Test",
            "start_time": "2024-01-01T08:00:00",
            "place": "Test",
            "time_to_complete": 100,
            "periodicity": 4,
            "award": "test",
            "is_pleasant": "True"
        }
        responce = self.client.post(
            reverse('habits:create_habit'),
            data=data
        )

        self.assertEqual(
            responce.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_Periodicity_HabitValidator(self):
        """Тест на ограничение: Нельзя выполнять
         привычку реже, чем 1 раз в 7 дней"""
        data = {
            "name": "Test",
            "user": self.user.id,
            "action": "Test",
            "start_time": "2024-01-01T08:00:00",
            "place": "Test",
            "time_to_complete": 100,
            "periodicity": 10,
            "award": "test"
        }
        responce = self.client.post(
            reverse('habits:create_habit'),
            data=data
        )

        self.assertEqual(
            responce.status_code,
            status.HTTP_400_BAD_REQUEST
        )
