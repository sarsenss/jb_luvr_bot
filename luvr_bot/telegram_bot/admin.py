from django.contrib import admin

from .models import Employee, EmployeeGeoPosition, Branch, JobRequest, JobRequestAssignment


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'chat_id')


class EmployeeGeoPositionAdmin(admin.ModelAdmin):
    list_display = ('employee', 'latitude', 'longitude',)


class BranchAdmin(admin.ModelAdmin):
    list_display = ('branch_name', 'latitude', 'longitude', 'address')


class JobRequestAdmin(admin.ModelAdmin):
    list_display = ('branch', 'employee_position', 'request_type', 'date_start', 'date_end', 'shift_date', 'shift_time_start',
                    'shift_time_end', 'number_of_employees', 'request_comment',)


class JobRequestAssignmentAdmin(admin.ModelAdmin):
    list_display = ('job_request', 'employee', 'start_position', 'end_position')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeGeoPosition, EmployeeGeoPositionAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(JobRequest, JobRequestAdmin)
admin.site.register(JobRequestAssignment, JobRequestAssignmentAdmin)
