# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CrawledLink.url_255'
        db.add_column(u'main_crawledlink', 'url_255',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True),
                      keep_default=False)

        # Adding field 'Crawl.root_url_255'
        db.add_column(u'main_crawl', 'root_url_255',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CrawledLink.url_255'
        db.delete_column(u'main_crawledlink', 'url_255')

        # Deleting field 'Crawl.root_url_255'
        db.delete_column(u'main_crawl', 'root_url_255')


    models = {
        u'main.crawl': {
            'Meta': {'object_name': 'Crawl'},
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
            'history': ('picklefield.fields.PickledObjectField', [], {'default': '{}'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'url': ('django.db.models.fields.TextField', [], {}),
            'url_255': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
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