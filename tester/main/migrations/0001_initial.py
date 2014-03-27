# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Application'
        db.create_table(u'main_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'main', ['Application'])

        # Adding model 'TestStep'
        db.create_table(u'main_teststep', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('testcase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.TestCase'])),
            ('sequence', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('expected_result', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('expected_result_screenshot', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 27, 0, 0), auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 27, 0, 0), auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['TestStep'])

        # Adding model 'TestCase'
        db.create_table(u'main_testcase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Application'])),
            ('grouping', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.TestGrouping'])),
            ('sequence', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('preconditions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 27, 0, 0), auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 27, 0, 0), auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['TestCase'])

        # Adding model 'TestGrouping'
        db.create_table(u'main_testgrouping', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Application'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 27, 0, 0), auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 27, 0, 0), auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['TestGrouping'])


    def backwards(self, orm):
        # Deleting model 'Application'
        db.delete_table(u'main_application')

        # Deleting model 'TestStep'
        db.delete_table(u'main_teststep')

        # Deleting model 'TestCase'
        db.delete_table(u'main_testcase')

        # Deleting model 'TestGrouping'
        db.delete_table(u'main_testgrouping')


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
        u'main.testgrouping': {
            'Meta': {'object_name': 'TestGrouping'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Application']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 27, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 27, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.teststep': {
            'Meta': {'object_name': 'TestStep'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 27, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expected_result': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expected_result_screenshot': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 27, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.TestCase']"})
        }
    }

    complete_apps = ['main']