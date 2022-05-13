from django.contrib.auth.models import AbstractUser
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name}'


class Position(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f'{self.name}'


class Employee(AbstractUser):
    name = models.CharField(max_length=32, verbose_name='Имя')
    surname = models.CharField(max_length=32, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=32, verbose_name='Отчество')

    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Подразделение')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='Должность')

    def __str__(self):
        return f'{self.name} {self.patronymic} {self.surname} – {self.position}'

    def get_short_fio(self):
        return f'{self.surname} {self.name[0]}. {self.patronymic[0]}.'

    def get_full_fio(self):
        return f'{self.surname} {self.name} {self.patronymic}'
