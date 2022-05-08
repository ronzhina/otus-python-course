import os

import django
from django.test import TestCase
from django.urls import reverse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vacations.settings")
django.setup()

from myauth.models import Department, Position, Employee
from ..models import Claim


class ClaimsAccessTest(TestCase):

    @classmethod
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

    def test_home_page_anonymous(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert response.template_name == ['claims/home.html']
        assert 'Добро пожаловать в сервис Отпуска!' in str(response.content.decode())
        assert response.context_data['user'].is_anonymous
        assert 'Войти' in str(response.content.decode())

    def test_home_page_user(self):
        self.client.login(username='test', password='OtusOtus')
        response = self.client.get('/')
        assert response.status_code == 200
        assert response.template_name == ['claims/home.html']
        assert 'Добро пожаловать в сервис Отпуска!' in str(response.content.decode())
        assert response.context_data['user'].is_anonymous is False
        assert response.context_data['user'].username == 'test'
        assert 'Выйти' in str(response.content.decode())

    def test_claim_list_anonymous(self):
        response = self.client.get('/cabinet/', follow=True)
        assert response.redirect_chain == [('/myauth/login?next=/cabinet/', 302),
                                           ('/myauth/login/?next=%2Fcabinet%2F', 301)]
        assert response.status_code == 200
        assert response.template_name == ['registration/login.html']
        assert 'Вход сотрудника' in str(response.content.decode())

    def test_claim_list_user(self):
        self.client.login(username='test', password='OtusOtus')
        response = self.client.get('/cabinet/', follow=True)
        assert response.context_data['page_header'] == 'Мои заявления'
        assert response.template_name == ['claims/claim_list.html']
        assert 'У вас пока нет заявлений.' in str(response.content.decode())

    def test_claim_creation_anonymous(self):
        response = self.client.get(reverse('claims:create'), follow=True)
        assert response.redirect_chain == [('/myauth/login?next=/claim/create/', 302),
                                           ('/myauth/login/?next=%2Fclaim%2Fcreate%2F', 301)]
        assert response.status_code == 200
        assert response.template_name == ['registration/login.html']
        assert 'Вход сотрудника' in str(response.content.decode())

    def test_claim_creation_user(self):
        self.client.login(username='test', password='OtusOtus')
        response = self.client.get(reverse('claims:create'))
        assert response.status_code == 200
        assert response.context_data['page_header'] == 'Новое заявление'
        assert response.template_name == ['claims/claim_form.html']

    def test_claim_approve_anonymous(self):
        response = self.client.get('/approve/', follow=True)
        assert response.redirect_chain == [('/myauth/login?next=/approve/', 302),
                                           ('/myauth/login/?next=%2Fapprove%2F', 301)]
        assert response.status_code == 200
        assert response.template_name == ['registration/login.html']
        assert 'Вход сотрудника' in str(response.content.decode())

    def test_claim_approve_list_user(self):
        self.client.login(username='test', password='OtusOtus')
        response = self.client.post(reverse('claims:create'), data=self.claim_data, follow=True)
        assert response.status_code == 200

        response = self.client.get('/approve/')
        assert len(response.context_data['claims']) == 0

    def test_claim_approve_list_director(self):
        self.client.login(username='test', password='OtusOtus')
        response = self.client.post(reverse('claims:create'), data=self.claim_data, follow=True)
        assert response.status_code == 200

        self.client.login(username='director', password='OtusOtus')
        response = self.client.get('/approve/')
        assert len(response.context_data['claims']) == 1

    def test_claim_updating_anonymous(self):
        self.client.login(username='test', password='OtusOtus')
        response = self.client.post(reverse('claims:create'), data=self.claim_data, follow=True)
        claim_id = response.context_data['claims'][0].pk
        self.client.get(reverse('myauth:logout'))

        response = self.client.get(reverse('claims:update', args=[claim_id]), follow=True)

        assert response.redirect_chain == [(f'/myauth/login?next=/claim/update/{claim_id}/', 302),
                                           (f'/myauth/login/?next=%2Fclaim%2Fupdate%2F{claim_id}%2F', 301)]
        assert response.status_code == 200
        assert response.template_name == ['registration/login.html']
        assert 'Вход сотрудника' in str(response.content.decode())

    def test_claim_updating_user(self):
        self.client.login(username='test', password='OtusOtus')
        response = self.client.post(reverse('claims:create'), data=self.claim_data, follow=True)
        claim_id = response.context_data['claims'][0].pk
        response = self.client.get(reverse('claims:update', args=[claim_id]), follow=True)
        assert response.status_code == 200
        assert response.context_data['page_header'] == 'Редактирование заявления'
        assert response.template_name == ['claims/claim_form.html']

    def test_claim_reading_anonymous(self):
        self.client.login(username='test', password='OtusOtus')
        response = self.client.post(reverse('claims:create'), data=self.claim_data, follow=True)
        claim_id = response.context_data['claims'][0].pk
        self.client.get(reverse('myauth:logout'))

        response = self.client.get(reverse('claims:detail', args=[claim_id]), follow=True)

        assert response.redirect_chain == [('/myauth/login?next=/claim/detail/3/', 302),
                                           ('/myauth/login/?next=%2Fclaim%2Fdetail%2F3%2F', 301)]
        assert response.status_code == 200
        assert response.template_name == ['registration/login.html']
        assert 'Вход сотрудника' in str(response.content.decode())

    def test_claim_reading_user(self):
        self.client.login(username='test', password='OtusOtus')
        response = self.client.post(reverse('claims:create'), data=self.claim_data, follow=True)
        claim_id = response.context_data['claims'][0].pk
        response = self.client.get(reverse('claims:detail', args=[claim_id]), follow=True)
        assert response.status_code == 200
        assert response.context_data['page_header'] == 'Заявление'
        assert response.template_name == ['claims/claim_detail.html']
