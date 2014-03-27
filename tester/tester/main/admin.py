from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from suit_ckeditor.widgets import CKEditorWidget
from tester.main.models import TestStep, TestCase, Application, TestGrouping, TestCaseRun, TestStepRun, TestGroupingRun
from nested_inlines.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name']

class TestStepForm(ModelForm):
    class Meta:
        widgets = {
            'description': CKEditorWidget(editor_options={'startupFocus': False}),
        }

class TestStepAdmin(admin.ModelAdmin):
    form = TestStepForm


#class TestStepInline(admin.TabularInline):
#    model = TestStep

class TestCaseForm(ModelForm):
    class Meta:
        _ck_editor_toolbar = [
            #{'name': 'basicstyles', 'groups': ['basicstyles', 'cleanup']},
            #{'name': 'paragraph', 'groups': ['list', 'indent', 'blocks', 'align']},
            #{'name': 'document', 'groups': ['mode']}, '/',
            #{'name': 'styles'}, {'name': 'colors'},
            {'name': 'insert_custom', 'items': ['Image', 'Flash', 'Table', 'HorizontalRule']},
            #{'name': 'about'}
        ]
        _ck_editor_config = {'autoGrow_onStartup': True,
                             'autoGrow_minHeight': 100,
                             'autoGrow_maxHeight': 250,
                             'extraPlugins': 'autogrow',
                             'toolbarGroups': _ck_editor_toolbar}
        widgets = {
            'description': CKEditorWidget(editor_options=_ck_editor_config),
            'preconditions': CKEditorWidget(editor_options=_ck_editor_config),
            'comments': CKEditorWidget(editor_options=_ck_editor_config),
        }

class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['title']
    #inlines = [
    #    TestStepInline,
    #]
    form = TestCaseForm

class TestStepInline(NestedTabularInline):
    model = TestStep

class TestCaseInline(NestedStackedInline):
    model = TestCase
    inlines = [TestStepInline]
    #form = TestCaseForm

class TestGroupingAdmin(NestedModelAdmin):
    list_display = ['title', 'num_test_cases']
    inlines = [
        TestCaseInline,
    ]
    actions = ['testgrouping_test']

    def testgrouping_test(self, request, queryset):
        grouping = queryset[0]
        grouping_run = TestGroupingRun(testgrouping=grouping)
        grouping_run.user = request.user
        grouping_run.user_agent = request.META["HTTP_USER_AGENT"]
        grouping_run.ip_address = request.META["REMOTE_ADDR"]
        grouping_run.save()

        for testcase in grouping.testcase_set.all():
            case_run = TestCaseRun(testcase=testcase, testgrouping_run=grouping_run)
            case_run.save()

            for teststep in testcase.teststep_set.all():
                step_run = TestStepRun(teststep=teststep, testcase_run=case_run)
                step_run.save()

        return HttpResponseRedirect('/admin/main/testgroupingrun/%s/' % str(grouping_run.id))
    testgrouping_test.short_description = "Execute TestGrouping"

admin.site.register(Application, ApplicationAdmin)
admin.site.register(TestStep, TestStepAdmin)
admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(TestGrouping, TestGroupingAdmin)















class TestStepRunInline(NestedStackedInline):
    model = TestStepRun
    readonly_fields = ('teststep', 'sequence','description', 'expected_result', 'expected_result_screenshot',)
    extra=0

class TestCaseRunInline(NestedStackedInline):
    model = TestCaseRun
    inlines = [TestStepRunInline]
    readonly_fields = ('testcase', 'sequence', 'title', 'description', 'preconditions', 'comments', 'overall_status')
    extra=0

class TestGroupingRunAdmin(NestedModelAdmin):
    list_display = ['title', 'date_added', 'user', 'overall_status', 'total_cases', 'num_incomplete', 'num_pass', 'num_fail']
    inlines = [
        TestCaseRunInline,
    ]
    date_hierarchy = 'last_modified'
    verbose_name = "Text Execution Run"
    readonly_fields = ('overall_status',)

admin.site.register(TestGroupingRun, TestGroupingRunAdmin)
