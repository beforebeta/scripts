# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CrawledLink.date_added'
        db.add_column(u'main_crawledlink', 'date_added',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 7, 0, 0), auto_now_add=True, blank=True),
                      keep_default=False)

        # Adding field 'CrawledLink.last_modified'
        db.add_column(u'main_crawledlink', 'last_modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 7, 0, 0), auto_now=True, auto_now_add=True, blank=True),
                      keep_default=False)

        # Adding field 'CrawlQueue.date_added'
        db.add_column(u'main_crawlqueue', 'date_added',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 7, 0, 0), auto_now_add=True, blank=True),
                      keep_default=False)

        # Adding field 'CrawlQueue.last_modified'
        db.add_column(u'main_crawlqueue', 'last_modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 7, 0, 0), auto_now=True, auto_now_add=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CrawledLink.date_added'
        db.delete_column(u'main_crawledlink', 'date_added')

        # Deleting field 'CrawledLink.last_modified'
        db.delete_column(u'main_crawledlink', 'last_modified')

        # Deleting field 'CrawlQueue.date_added'
        db.delete_column(u'main_crawlqueue', 'date_added')

        # Deleting field 'CrawlQueue.last_modified'
        db.delete_column(u'main_crawlqueue', 'last_modified')


    models = {
        u'main.crawl': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Crawl'},
            'crawl_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 7, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'ended': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 7, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'root_url': ('django.db.models.fields.TextField', [], {}),
            'root_url_255': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'stats': ('picklefield.fields.PickledObjectField', [], {'default': '{}'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'started'", 'max_length': '20'})
        },
        u'main.crawledlink': {
            'Meta': {'object_name': 'CrawledLink'},
            'contents': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'crawl': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Crawl']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 7, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'history': ('picklefield.fields.PickledObjectField', [], {'default': '{}'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 7, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'status_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'url': ('django.db.models.fields.TextField', [], {}),
            'url_255': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        u'main.crawlqueue': {
            'Meta': {'object_name': 'CrawlQueue'},
            'crawl': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Crawl']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 7, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 7, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        u'main.message': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Message'},
            'crawl': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Crawl']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 7, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 7, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'info'", 'max_length': '50'})
        }
    }

    complete_apps = ['main']