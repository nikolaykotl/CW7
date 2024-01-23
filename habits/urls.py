from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitListAPIView, HabitCreateAPIView, \
    HabitPublicListAPIView, HabitRetrieveAPIView, \
    HabitUpdateAPIView, HabitDestroyAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('habit/', HabitListAPIView.as_view(),
         name='list_habit'),
    path('habit/create/', HabitCreateAPIView.as_view(),
         name='create_habit'),
    path('habit/public/', HabitPublicListAPIView.as_view(),
         name='public_habit'),
    path('habit/<int:pk>/', HabitRetrieveAPIView.as_view(),
         name='detail_habit'),
    path('habit/update/<int:pk>/', HabitUpdateAPIView.as_view(),
         name='update_habit'),
    path('habit/delete/<int:pk>/', HabitDestroyAPIView.as_view(),
         name='delete_habit')
]
