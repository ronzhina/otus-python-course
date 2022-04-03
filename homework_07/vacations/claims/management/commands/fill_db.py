from django.core.management.base import BaseCommand

from claims.models import Department, Employee, Position


class Command(BaseCommand):

    def handle(self, *args, **options):
        departments = ['Управление разработкой', 'Поддержка сервисов', 'Отдел продаж', 'Совет директоров']
        for department in departments:
            Department.objects.get_or_create(name=department)
        positions = ['программист', 'инженер', 'менеджер по продажам', 'директор']
        for position in positions:
            Position.objects.get_or_create(name=position)

        names = ['Иван', 'Петр', 'Илья', 'Никита']
        surnames = ['Петров', 'Кузнецов', 'Сидоров', 'Иванов']
        patronymics = ['Антонович', 'Сергеевич', 'Иванович', 'Петрович']

        for index in range(0, len(names)):
            Employee.objects.get_or_create(name=names[index],
                                           surname=surnames[index],
                                           patronymic=patronymics[index],
                                           department=Department.objects.get(name=departments[index]),
                                           position=Position.objects.get(name=positions[index]))
