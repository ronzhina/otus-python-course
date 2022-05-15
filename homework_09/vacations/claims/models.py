from django.db import models
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
        verbose_name='Тип отпуска'
    )

    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата конца')
    is_pay_now = models.BooleanField(verbose_name='Выплатить отпускные сейчас')
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    employee = models.ForeignKey('myauth.Employee', related_name='employee', on_delete=models.CASCADE,
                                 verbose_name='Сотрудник')
    agreed_with = models.ForeignKey('myauth.Employee', related_name='manager', on_delete=models.CASCADE,
                                    verbose_name='Руководитель')

    status = models.CharField(
        max_length=2,
        choices=ClaimStatus.choices,
        default=ClaimStatus.ON_APPROVAL,
        blank=True,
        verbose_name='Статус'
    )

    def __str__(self):
        return f"Заявление #{self.pk} от {self.employee.get_short_fio()} " \
               f"({self.start_date} – {self.start_date}) " \
               f"– {self.ClaimStatus(self.status).label}"

    def get_status(self):
        return self.ClaimStatus(self.status).label

    def get_type(self):
        return self.ClaimType(self.type).label
