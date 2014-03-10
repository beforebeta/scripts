# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BackLink'
        db.create_table(u'main_backlink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('crawl', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Crawl'])),
            ('url', self.gf('django.db.models.fields.TextField')()),
            ('backlink_url', self.gf('django.db.models.fields.TextField')()),
            ('url_255', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('backlink_url_255', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 7, 0, 0), auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 7, 0, 0), auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['BackLink'])

        # Adding unique constraint on 'BackLink', fields ['crawl', 'url_255', 'backlink_url_255']
        db.create_unique(u'main_backlink', ['crawl_id', 'url_255', 'backlink_url_255'])


    def backwards(self, orm):
        # Removing unique constraint on 'BackLink', fields ['crawl', 'url_255', 'backlink_url_255']
        db.delete_unique(u'main_backlink', ['crawl_id', 'url_255', 'backlink_url_255'])

        # Deleting model 'BackLink'
        db.delete_table(u'main_backlink')


    models = {
        u'main.backlink': {
            'Meta': {'unique_together': "(('crawl', 'url_255', 'backlink_url_255'),)", 'object_name': 'BackLink'},
            'backlink_url': ('django.db.models.fields.TextField', [], {}),
            'backlink_url_255': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'crawl': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Crawl']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 7, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 7, 0, 0)', 'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {}),
            'url_255': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
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