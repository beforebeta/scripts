import datetime
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Application(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class TestStep(models.Model):
    testcase = models.ForeignKey('TestCase')
    sequence = models.IntegerField(default=1)
    description = models.TextField(null=True, blank=True)
    expected_result = models.TextField(null=True, blank=True)
    expected_result_screenshot = models.URLField(max_length=255, null=True, blank=True)

    date_added = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
    last_modified = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)

    def __str__(self):
        return "%s - Step %s" % (str(self.testcase), self.sequence)

class TestCase(models.Model):
    application = models.ForeignKey(Application)
    grouping = models.ForeignKey('TestGrouping')
    sequence = models.IntegerField(default=1)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    preconditions = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    date_added = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
    last_modified = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.application.name, self.title)

class TestGrouping(models.Model):
    application = models.ForeignKey(Application)
    title = models.CharField(max_length=255)

    date_added = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
    last_modified = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)

    def num_test_cases(self):
        return self.testcase_set.count()

    def __str__(self):
        return "%s - %s" % (self.application.name, self.title)

########################################################################################################################

TestStatus = (
    ('NT', 'Not Tested'),
    ('F', 'Fail'),
    ('P', 'Pass')
)

class TestStepRun(models.Model):
    teststep = models.ForeignKey(TestStep)
    testcase_run = models.ForeignKey('TestCaseRun')
    sequence = models.IntegerField(default=1)
    description = models.TextField(null=True, blank=True)
    expected_result = models.TextField(null=True, blank=True)
    expected_result_screenshot = models.URLField(max_length=255, null=True, blank=True)

    status = models.CharField(max_length=2, choices=TestStatus, default='NT')
    actual_result = models.TextField(null=True, blank=True)
    actual_result_screenshot = models.URLField(max_length=255, null=True, blank=True)

    date_added = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
    last_modified = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        self.sequence = self.teststep.sequence
        self.description = self.teststep.description
        self.expected_result = self.teststep.expected_result
        self.expected_result_screenshot = self.teststep.expected_result_screenshot
        super(TestStepRun, self).save(*args, **kwargs)

        if self.testcase_run:
            total_steps = self.testcase_run.teststeprun_set.all().count()
            if total_steps > 0:
                if self.testcase_run.teststeprun_set.filter(status="F").count() > 0:
                    self.testcase_run.overall_status = "Fail"
                else:
                    if self.testcase_run.teststeprun_set.filter(status="P").count() == total_steps:
                        self.testcase_run.overall_status = "Pass"
                    else:
                        self.testcase_run.overall_status = "Incomplete"
            else:
                self.testcase_run.overall_status = "Incomplete"
            self.testcase_run.save()

    def __str__(self):
        return "TestStepRun - %s" % str(self.sequence)

class TestCaseRun(models.Model):
    testcase = models.ForeignKey(TestCase)
    testgrouping_run = models.ForeignKey('TestGroupingRun')

    sequence = models.IntegerField(default=1)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    preconditions = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    tester_comments = models.TextField(null=True, blank=True)
    overall_status = models.CharField(max_length=50, null=True, blank=True, default="Incomplete")

    def save(self, *args, **kwargs):
        self.sequence = self.testcase.sequence
        self.title = self.testcase.title
        self.description = self.testcase.description
        self.preconditions = self.testcase.preconditions
        self.comments = self.testcase.comments
        super(TestCaseRun, self).save(*args, **kwargs)

        if self.testgrouping_run:
            total_cases = self.testgrouping_run.testcaserun_set.all().count()
            if total_cases > 0:
                if self.testgrouping_run.testcaserun_set.filter(overall_status="Fail").count() > 0:
                    self.testgrouping_run.overall_status = "Fail"
                else:
                    if self.testgrouping_run.testcaserun_set.filter(overall_status="Pass").count() == total_cases:
                        self.testgrouping_run.overall_status = "Pass"
                    else:
                        self.testgrouping_run.overall_status = "Incomplete"
            else:
                self.testgrouping_run.overall_status = "Incomplete"
            self.testgrouping_run.save()

    date_added = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
    last_modified = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)

BROWSERS = (
    ('M', 'Mozilla'),
    ('F', 'Firefox'),
    ('IE', 'Internet Explorer'),
    ('C', 'Chrome'),
    ('S', 'Safari'),
    ('O', 'Other')
)

class TestGroupingRun(models.Model):
    user = models.ForeignKey(User)
    testgrouping = models.ForeignKey(TestGrouping)
    title = models.CharField(max_length=255)
    browser = models.CharField(max_length=10, choices=BROWSERS)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.CharField(max_length=255, null=True, blank=True)

    overall_status = models.CharField(max_length=50, null=True, blank=True, default="Incomplete")

    date_added = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
    last_modified = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        self.title = self.testgrouping.title
        super(TestGroupingRun, self).save(*args, **kwargs)

    def total_cases(self):
        return self.testcaserun_set.all().count()

    def num_incomplete(self):
        return self.testcaserun_set.filter(overall_status='Incomplete').count()

    def num_pass(self):
        return self.testcaserun_set.filter(overall_status='Pass').count()

    def num_fail(self):
        return self.testcaserun_set.filter(overall_status='Fail').count()

#class TestCaseGrouping(models.Model):
#    sequence = models.IntegerField(default=1)
#    grouping = models.ForeignKey(TestGrouping)
#    case = models.ForeignKey(TestCase)
#
#TestResult = (
#    ('NT', 'Not Tested'),
#    ('F', 'Fail'),
#    ('P', 'Pass')
#)
#class TestCaseRun(models.Model):
#    case = models.ForeignKey(TestCase)
#    result = models.CharField(choices=TestResult, default='NT', max_length=2)
#
#    date_added = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
#    last_modified = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)
#
#class TestGroupingRun(models.Model):
#    grouping = models.ForeignKey(TestGrouping)
#    runs = models.ManyToManyField(TestCaseRun, through='TestCaseGroupingRun')
#    date_added = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
#    last_modified = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)
#
#class TestStepRun(models.Model):
#    case_run = models.ForeignKey(TestCaseRun)
#    sequence = models.IntegerField(default=1)
#    description = models.TextField(null=True, blank=True)
#    expected_result = models.TextField(null=True, blank=True)
#    expected_result_screenshot = models.CharField(max_length=255, null=True, blank=True)
#    actual_result = models.TextField(null=True, blank=True)
#    actual_result_screenshot = models.CharField(max_length=255, null=True, blank=True)
#
#    date_added = models.DateTimeField(default=datetime.datetime.now(), auto_now_add=True)
#    last_modified = models.DateTimeField(default=datetime.datetime.now(), auto_now=True, auto_now_add=True)
#
#class TestCaseGroupingRun(models.Model):
#    sequence = models.IntegerField(default=1)
#    grouping_run = models.ForeignKey(TestGroupingRun)
#    case_run = models.ForeignKey(TestCaseRun)
