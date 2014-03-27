# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'TestGroupingRun.browser'
        db.alter_column(u'main_testgroupingrun', 'browser', self.gf('django.db.models.fields.CharField')(default='C', max_length=10))

    def backwards(self, orm):

        # Changing field 'TestGroupingRun.browser'
        db.alter_column(u'main_testgroupingrun', 'browser', self.gf('django.db.models.fields.CharField')(max_length=10, null=True))

    models = {
        u'main.application': {
            'Meta': {'object_name': 'Application'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.testcase': {
            'Meta': {'object_name': 'TestCase'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Application']"}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 27, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'grouping': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.TestGrouping']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 27, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'preconditions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.testcaserun': {
            'Meta': {'object_name': 'TestCaseRun'},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 27, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 27, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'overall_status': ('django.db.models.fields.CharField', [], {'default': "'Incomplete'", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'preconditions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.TestCase']"}),
            'tester_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'testgrouping_run': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.TestGroupingRun']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.testgrouping': {
            'Meta': {'object_name': 'TestGrouping'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Application']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 27, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 27, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.testgroupingrun': {
            'Meta': {'object_name': 'TestGroupingRun'},
            'browser': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 27, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 27, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'testgrouping': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.TestGrouping']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.teststep': {
            'Meta': {'object_name': 'TestStep'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 27, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expected_result': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expected_result_screenshot': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 27, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.TestCase']"})
        },
        u'main.teststeprun': {
            'Meta': {'object_name': 'TestStepRun'},
            'actual_result': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'actual_result_screenshot': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 27, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expected_result': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expected_result_screenshot': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 27, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NT'", 'max_length': '2'}),
            'testcase_run': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.TestCaseRun']"}),
            'teststep': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.TestStep']"})
        }
    }

    complete_apps = ['main']