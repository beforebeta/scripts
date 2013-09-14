# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Entity.blog_feed_url'
        db.add_column('main_entity', 'blog_feed_url',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Entity.blog_feed_url'
        db.delete_column('main_entity', 'blog_feed_url')


    models = {
        'main.acquisition': {
            'Meta': {'object_name': 'Acquisition'},
            'acquired_day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'acquired_month': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'acquired_year': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Entity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price_amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'price_currency_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'source_description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'source_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'term_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'main.entity': {
            'Meta': {'object_name': 'Entity'},
            'acquisitions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Acquisition']", 'symmetrical': 'False'}),
            'blog_feed_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'blog_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'category_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'competition': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Entity']", 'symmetrical': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'crunchbase_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'data': ('picklefield.fields.PickledObjectField', [], {}),
            'deadpooled_day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'deadpooled_month': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'deadpooled_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'deadpooled_year': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'founded_day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'founded_month': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'founded_year': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'funding_rounds': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'funding_rounds'", 'symmetrical': 'False', 'to': "orm['main.FundingRound']"}),
            'homepage_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Image']", 'symmetrical': 'False', 'blank': 'True'}),
            'investments': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'funding_round_investments'", 'symmetrical': 'False', 'to': "orm['main.FundingRound']"}),
            'ipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.IPO']", 'null': 'True', 'blank': 'True'}),
            'is_company': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_financial_org': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_person': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'number_of_employees': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'offices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Office']", 'symmetrical': 'False'}),
            'overview': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'permalink': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'relationships': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Relationship']", 'symmetrical': 'False'}),
            'screenshots': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'screenshots'", 'symmetrical': 'False', 'to': "orm['main.Image']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'total_money_raised': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'main.fundinground': {
            'Meta': {'object_name': 'FundingRound'},
            'funded_day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'funded_month': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'funded_year': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'entity_investments'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['main.Entity']"}),
            'investors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'investors'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['main.Entity']"}),
            'raised_amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'raised_currency_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'round_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'source_description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'source_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'main.image': {
            'Meta': {'object_name': 'Image'},
            'height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.ipo': {
            'Meta': {'object_name': 'IPO'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pub_month': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pub_year': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stock_symbol': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'valuation_amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'valuation_currency_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'main.office': {
            'Meta': {'object_name': 'Office'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'state_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'main.relationship': {
            'Meta': {'object_name': 'Relationship'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_past': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Entity']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'main.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['main']