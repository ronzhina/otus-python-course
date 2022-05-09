import os

import django
import pytest
from django.test import TestCase
from django.urls import reverse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vacations.settings")
django.setup()

from myauth.models import Department, Position, Employee
from ..models import Claim


class ClaimsTest(TestCase):

    @classmethod
    @pytest.mark.django_db
    def setUpClass(cls):
        super().setUpClass()
        Department.objects.get_or_create(name='УР')
        Position.objects.get_or_create(name='программист')
        Position.objects.get_or_create(name='директор')
        cls.user = Employee.objects.create(username='test', name='Ivan', surname='Ivanov', patronymic='Ivanovich',
                                           department=Department.objects.get(name='УР'),
                                           position=Position.objects.get(name='программист'))
        cls.director = Employee.objects.create(username='director', name='Petr', surname='Petrov',
                                               patronymic='Petrovich',
                                               department=Department.objects.get(name='УР'),
                                               position=Position.objects.get(name='директор'))
        cls.user.set_password('OtusOtus')
        cls.user.save()

        cls.director.set_password('OtusOtus')
        cls.director.save()
        cls.claim_data = {
            'employee': Employee.objects.get(username='test').pk,
            'type': Claim.ClaimType.MAIN,
            'start_date': '2022-05-12',
            'end_date': '2022-05-12',
            'agreed_with': Employee.objects.get(username='director').pk,
        }

    def test_empty_claim_list(self):
        self.client.login(username='test', password='OtusOtus')
        response = self.client.get('/cabinet/', follow=True)

        assert response.context_data['page_header'] == 'Мои заявления'
        assert 'У вас пока нет заявлений.' in str(response.content.decode())

    def test_claim_creation(self):
        self.client.login(username='test', password='OtusOtus')
        response = self.client.post(reverse('claims:create'), data=self.claim_data, follow=True)
        assert response.status_code == 200
        assert response.context_data['page_header'] == 'Мои заявления'
        assert response.template_name == ['claims/claim_list.html']
        claim_id = response.context_data['claims'][0].pk
        assert str(response.context_data['claims'][
                       0]) == f'Заявление #{claim_id} от Ivanov I. I. (2022-05-12 – 2022-05-12) – На согласовании'
        assert response.context_data['claims'][0].get_type() == 'Основной'
        assert response.context_data['claims'][0].agreed_with.get_short_fio() == 'Petrov P. P.'

    def test_empty_claim_approve_list(self):
        self.client.login(username='test', password='OtusOtus')
        response = self.client.get('/approve/')
        assert len(response.context_data['claims']) == 0
        assert 'Все задания выполнены.' in str(response.content.decode())

    def test_claim_approve_list(self):
        self.client.login(username='test', password='OtusOtus')
        response = self.client.post(reverse('claims:create'), data=self.claim_data, follow=True)
        assert response.status_code == 200

        response = self.client.get('/approve/')
        assert len(response.context_data['claims']) == 0
        assert 'Все задания выполнены.' in str(response.content.decode())

        self.client.login(username='director', password='OtusOtus')
        response = self.client.get('/approve/')
        assert len(response.context_data['claims']) == 1
        claim_id = response.context_data['claims'][0].pk
        assert str(response.context_data['claims'][
                       0]) == f'Заявление #{claim_id} от Ivanov I. I. (2022-05-12 – 2022-05-12) – На согласовании'

    def test_accept_claim(self):
        self.client.login(username='test', password='OtusOtus')
        response = self.client.post(reverse('claims:create'), data=self.claim_data, follow=True)
        assert response.status_code == 200
        claim_id = response.context_data['claims'][0].pk

        self.client.login(username='director', password='OtusOtus')
        self.client.post(reverse('claims:accept_claim', args=[claim_id]))
        response = self.client.get('/approve/')
        assert str(response.context_data['claims'][
                       0]) == f'Заявление #{claim_id} от Ivanov I. I. (2022-05-12 – 2022-05-12) – Согласовано'

    def test_reject_claim(self):
        self.client.login(username='test', password='OtusOtus')
        response = self.client.post(reverse('claims:create'), data=self.claim_data, follow=True)
        assert response.status_code == 200
        claim_id = response.context_data['claims'][0].pk

        self.client.login(username='director', password='OtusOtus')
        self.client.post(reverse('claims:reject_claim', args=[claim_id]))
        response = self.client.get('/approve/')
        assert str(response.context_data['claims'][
                       0]) == f'Заявление #{claim_id} от Ivanov I. I. (2022-05-12 – 2022-05-12) – Отклонено'
