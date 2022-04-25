from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Claim(models.Model):
    class ClaimType(models.TextChoices):
        MAIN = 'MN', _('Основной')
        ADDITIONAL = 'AD', _('Дополнительный')
        CHILD = 'CH', _('По уходу за ребёнком')
        NOTPAID = 'NP', _('Не оплачиваемый')
        STUDY = 'ST', _('На учёбу')

    class ClaimStatus(models.TextChoices):
        ON_APPROVAL = 'OA', _('На согласовании')
        REJECTED = 'RE', _('Отклонено')
        ACCEPTED = 'AC', _('Согласовано')

    type = models.CharField(
        max_length=2,
        choices=ClaimType.choices,
        default=ClaimType.MAIN,
    )

    start_date = models.DateField()
    end_date = models.DateField()
    is_pay_now = models.BooleanField()
    comment = models.TextField(blank=True)
    employee = models.ForeignKey('claims.Employee', related_name='employee', on_delete=models.CASCADE)
    agreed_with = models.ForeignKey('claims.Employee', related_name='manager', on_delete=models.CASCADE)

    status = models.CharField(
        max_length=2,
        choices=ClaimStatus.choices,
        default=ClaimStatus.ON_APPROVAL.label,
    )

    def __str__(self):
        return f"Заявление #{self.id} от {self.employee.get_short_fio()} " \
               f"({self.start_date} – {self.start_date}) " \
               f"– {self.ClaimStatus(self.status).label}"


class Department(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name}'


class Position(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f'{self.name}'


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    patronymic = models.CharField(max_length=32)

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} {self.surname} {self.patronymic} – {self.position}'

    def get_short_fio(self):
        return f'{self.surname} {self.name[0]}. {self.patronymic[0]}.'
