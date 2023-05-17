import datetime
from datetime import timedelta

from django.db import models


class Employee(models.Model):
    phone_number = models.CharField(max_length=250, verbose_name='номер телефона')
    chat_id = models.IntegerField(verbose_name='ID телеграм чата', blank=True, null=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.phone_number


class EmployeeGeoPosition(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='geo_positions', verbose_name='сотрудник')
    latitude = models.CharField(max_length=300, verbose_name='широта')
    longitude = models.CharField(max_length=300, verbose_name='долгота')
    geo_positions_date = models.DateField(auto_now=True, verbose_name='дата внесения гео позиций')

    class Meta:
        verbose_name = 'Геопозиция сотрудника'
        verbose_name_plural = 'Геопозиция сотрудников'

    def __str__(self):
        return f'{self.latitude} - {self.longitude}'


class Branch(models.Model):
    branch_name = models.CharField(max_length=250,  verbose_name='название филиала')
    latitude = models.CharField(max_length=300,  verbose_name='широта')
    longitude = models.CharField(max_length=300,  verbose_name='долгота')
    address = models.CharField(max_length=300, verbose_name='адрес', blank=True, null=True)

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    def __str__(self):
        return self.branch_name


class JobRequest(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='job_requests')
    employee_position = models.CharField(blank=True, null=True, max_length=300, verbose_name='должность')
    request_type = models.CharField(blank=True, null=True, max_length=250, verbose_name='тип заявки')
    #TODO set date_start and date_end as shift_date when importing
    date_start = models.DateField(blank=True, null=True, verbose_name='дата начала периода')
    date_end = models.DateField(blank=True, null=True, verbose_name='дата окончания периода')
    shift_time_start = models.TimeField(blank=True, null=True, verbose_name='время начала смены')
    shift_time_end = models.TimeField(blank=True, null=True, verbose_name='время окончания смены')
    number_of_employees = models.CharField(max_length=3, blank=True, null=True, verbose_name='количество сотрудников')
    request_comment = models.TextField(blank=True, null=True, verbose_name='комментарий')

    class Meta:
        verbose_name = 'Заявка на сотрудников'
        verbose_name_plural = 'Заявки на сотрудников'

    def __str__(self):
        return f'{self.request_type} - {self.branch}'

    def is_shift_includes_time(self, request_date_time, tolerance_minutes=30):
        dates = []
        delta = timedelta(days=1)
        start_date = self.date_start
        while start_date <= self.date_end:
            dates.append(start_date)
            start_date += delta

        for date in dates:
            shift_start = datetime.datetime.combine(date, self.shift_time_start) - timedelta(minutes=tolerance_minutes)
            shift_end = datetime.datetime.combine(date, self.shift_time_end) + timedelta(minutes=tolerance_minutes)
            if shift_start <= request_date_time <= shift_end:
                return True
        return False


class JobRequestAssignment(models.Model):
    job_request = models.ForeignKey(JobRequest, on_delete=models.CASCADE, related_name='assignments',
                                    verbose_name='заявка на сотрудника')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='assignments',
                                 verbose_name='сотрудник')
    start_position = models.ForeignKey(EmployeeGeoPosition, on_delete=models.CASCADE, blank=True, null=True,
                                       related_name='start_assignments', verbose_name='начало смены')
    end_position = models.ForeignKey(EmployeeGeoPosition, on_delete=models.CASCADE, blank=True, null=True,
                                     related_name='end_assignments', verbose_name='окончание смены')
    assignment_date = models.DateField(auto_now=True, verbose_name='дата назначения')

    class Meta:
        verbose_name = 'Назначение сотрудников'
        verbose_name_plural = 'Назначения сотрудников'
