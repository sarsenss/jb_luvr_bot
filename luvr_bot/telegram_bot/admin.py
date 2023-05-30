from django.contrib import admin

from .models import Employee, EmployeeGeoPosition, Branch, JobRequest, JobRequestAssignment, Shift


class JobRequestAssignmentInline(admin.TabularInline):
    model = JobRequestAssignment


class ShiftInline(admin.TabularInline):
    model = Shift


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'chat_id', 'INN', 'full_name',)
    inlines = [JobRequestAssignmentInline]


class EmployeeGeoPositionAdmin(admin.ModelAdmin):
    list_display = ('employee', 'latitude', 'longitude', 'geo_positions_date',)


class BranchAdmin(admin.ModelAdmin):
    list_display = ('branch_name', 'latitude', 'longitude', 'address')


class JobRequestAdmin(admin.ModelAdmin):
    list_display = ('branch', 'employee_position', 'request_type', 'date_start', 'date_end', 'shift_time_start',
                    'shift_time_end', 'number_of_employees', 'request_comment', 'employee', 'status')
    inlines = [JobRequestAssignmentInline]


class JobRequestAssignmentAdmin(admin.ModelAdmin):
    list_display = ('job_request', 'employee', 'status', 'assignment_date')
    inlines = [ShiftInline]


class ShiftAdmin(admin.ModelAdmin):
    list_display = ('start_position', 'end_position', 'shift_date', 'assignment')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeGeoPosition, EmployeeGeoPositionAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(JobRequest, JobRequestAdmin)
admin.site.register(JobRequestAssignment, JobRequestAssignmentAdmin)
admin.site.register(Shift, ShiftAdmin)
# admin.site.register(CustomUser)
