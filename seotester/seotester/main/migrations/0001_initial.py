# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Crawl'
        db.create_table(u'main_crawl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('crawl_id', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('root_url', self.gf('django.db.models.fields.TextField')()),
            ('stats', self.gf('picklefield.fields.PickledObjectField')(default={})),
            ('started', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('ended', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='started', max_length=20)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 7, 0, 0), auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 7, 0, 0), auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Crawl'])

        # Adding model 'CrawlQueue'
        db.create_table(u'main_crawlqueue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('crawl', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Crawl'])),
            ('url', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'main', ['CrawlQueue'])

        # Adding model 'CrawledLink'
        db.create_table(u'main_crawledlink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('crawl', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Crawl'])),
            ('url', self.gf('django.db.models.fields.TextField')()),
            ('status_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('contents', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('history', self.gf('picklefield.fields.PickledObjectField')(default={})),
        ))
        db.send_create_signal(u'main', ['CrawledLink'])

        # Adding model 'Message'
        db.create_table(u'main_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('crawl', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Crawl'])),
            ('message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'main', ['Message'])


    def backwards(self, orm):
        # Deleting model 'Crawl'
        db.delete_table(u'main_crawl')

        # Deleting model 'CrawlQueue'
        db.delete_table(u'main_crawlqueue')

        # Deleting model 'CrawledLink'
        db.delete_table(u'main_crawledlink')

        # Deleting model 'Message'
        db.delete_table(u'main_message')


    models = {
        u'main.crawl': {
            'Meta': {'object_name': 'Crawl'},
            'crawl_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 7, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'ended': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 7, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'root_url': ('django.db.models.fields.TextField', [], {}),
            'started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'stats': ('picklefield.fields.PickledObjectField', [], {'default': '{}'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'started'", 'max_length': '20'})
        },
        u'main.crawledlink': {
            'Meta': {'object_name': 'CrawledLink'},
            'contents': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'crawl': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Crawl']"}),
            'history': ('picklefield.fields.PickledObjectField', [], {'default': '{}'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        u'main.crawlqueue': {
            'Meta': {'object_name': 'CrawlQueue'},
            'crawl': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Crawl']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        u'main.message': {
            'Meta': {'object_name': 'Message'},
            'crawl': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Crawl']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['main']