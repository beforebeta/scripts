# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Company'
        db.delete_table('main_company')

        # Adding model 'Image'
        db.create_table('main_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('width', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('height', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('main', ['Image'])

        # Adding model 'Acquisition'
        db.create_table('main_acquisition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('price_amount', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('price_currency_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('term_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('source_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('source_description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('acquired_year', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('acquired_month', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('acquired_day', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Entity'])),
        ))
        db.send_create_signal('main', ['Acquisition'])

        # Adding model 'IPO'
        db.create_table('main_ipo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('valuation_amount', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('valuation_currency_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('pub_year', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pub_month', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pub_day', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('stock_symbol', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('main', ['IPO'])

        # Adding model 'Relationship'
        db.create_table('main_relationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_past', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Entity'])),
        ))
        db.send_create_signal('main', ['Relationship'])

        # Adding model 'Entity'
        db.create_table('main_entity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_company', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_financial_org', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_person', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('permalink', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('crunchbase_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('homepage_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('blog_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('twitter_username', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('category_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('number_of_employees', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('founded_year', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('founded_month', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('founded_day', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('deadpooled_year', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('deadpooled_month', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('deadpooled_day', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('deadpooled_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('email_address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('overview', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('total_money_raised', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('ipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.IPO'])),
            ('data', self.gf('picklefield.fields.PickledObjectField')()),
        ))
        db.send_create_signal('main', ['Entity'])

        # Adding M2M table for field images on 'Entity'
        db.create_table('main_entity_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entity', models.ForeignKey(orm['main.entity'], null=False)),
            ('image', models.ForeignKey(orm['main.image'], null=False))
        ))
        db.create_unique('main_entity_images', ['entity_id', 'image_id'])

        # Adding M2M table for field tags on 'Entity'
        db.create_table('main_entity_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entity', models.ForeignKey(orm['main.entity'], null=False)),
            ('tag', models.ForeignKey(orm['main.tag'], null=False))
        ))
        db.create_unique('main_entity_tags', ['entity_id', 'tag_id'])

        # Adding M2M table for field relationships on 'Entity'
        db.create_table('main_entity_relationships', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entity', models.ForeignKey(orm['main.entity'], null=False)),
            ('relationship', models.ForeignKey(orm['main.relationship'], null=False))
        ))
        db.create_unique('main_entity_relationships', ['entity_id', 'relationship_id'])

        # Adding M2M table for field competition on 'Entity'
        db.create_table('main_entity_competition', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_entity', models.ForeignKey(orm['main.entity'], null=False)),
            ('to_entity', models.ForeignKey(orm['main.entity'], null=False))
        ))
        db.create_unique('main_entity_competition', ['from_entity_id', 'to_entity_id'])

        # Adding M2M table for field funding_rounds on 'Entity'
        db.create_table('main_entity_funding_rounds', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entity', models.ForeignKey(orm['main.entity'], null=False)),
            ('fundinground', models.ForeignKey(orm['main.fundinground'], null=False))
        ))
        db.create_unique('main_entity_funding_rounds', ['entity_id', 'fundinground_id'])

        # Adding M2M table for field investments on 'Entity'
        db.create_table('main_entity_investments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entity', models.ForeignKey(orm['main.entity'], null=False)),
            ('fundinground', models.ForeignKey(orm['main.fundinground'], null=False))
        ))
        db.create_unique('main_entity_investments', ['entity_id', 'fundinground_id'])

        # Adding M2M table for field acquisitions on 'Entity'
        db.create_table('main_entity_acquisitions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entity', models.ForeignKey(orm['main.entity'], null=False)),
            ('acquisition', models.ForeignKey(orm['main.acquisition'], null=False))
        ))
        db.create_unique('main_entity_acquisitions', ['entity_id', 'acquisition_id'])

        # Adding M2M table for field offices on 'Entity'
        db.create_table('main_entity_offices', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entity', models.ForeignKey(orm['main.entity'], null=False)),
            ('office', models.ForeignKey(orm['main.office'], null=False))
        ))
        db.create_unique('main_entity_offices', ['entity_id', 'office_id'])

        # Adding M2M table for field screenshots on 'Entity'
        db.create_table('main_entity_screenshots', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entity', models.ForeignKey(orm['main.entity'], null=False)),
            ('image', models.ForeignKey(orm['main.image'], null=False))
        ))
        db.create_unique('main_entity_screenshots', ['entity_id', 'image_id'])

        # Adding model 'FundingRound'
        db.create_table('main_fundinground', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('round_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('source_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('source_description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('raised_amount', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('raised_currency_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('funded_year', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('funded_month', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('funded_day', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('main', ['FundingRound'])

        # Adding M2M table for field investors on 'FundingRound'
        db.create_table('main_fundinground_investors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('fundinground', models.ForeignKey(orm['main.fundinground'], null=False)),
            ('entity', models.ForeignKey(orm['main.entity'], null=False))
        ))
        db.create_unique('main_fundinground_investors', ['fundinground_id', 'entity_id'])

        # Adding M2M table for field investments on 'FundingRound'
        db.create_table('main_fundinground_investments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('fundinground', models.ForeignKey(orm['main.fundinground'], null=False)),
            ('entity', models.ForeignKey(orm['main.entity'], null=False))
        ))
        db.create_unique('main_fundinground_investments', ['fundinground_id', 'entity_id'])

        # Adding model 'Office'
        db.create_table('main_office', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('state_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('main', ['Office'])

        # Adding model 'Tag'
        db.create_table('main_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('main', ['Tag'])


    def backwards(self, orm):
        # Adding model 'Company'
        db.create_table('main_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('main', ['Company'])

        # Deleting model 'Image'
        db.delete_table('main_image')

        # Deleting model 'Acquisition'
        db.delete_table('main_acquisition')

        # Deleting model 'IPO'
        db.delete_table('main_ipo')

        # Deleting model 'Relationship'
        db.delete_table('main_relationship')

        # Deleting model 'Entity'
        db.delete_table('main_entity')

        # Removing M2M table for field images on 'Entity'
        db.delete_table('main_entity_images')

        # Removing M2M table for field tags on 'Entity'
        db.delete_table('main_entity_tags')

        # Removing M2M table for field relationships on 'Entity'
        db.delete_table('main_entity_relationships')

        # Removing M2M table for field competition on 'Entity'
        db.delete_table('main_entity_competition')

        # Removing M2M table for field funding_rounds on 'Entity'
        db.delete_table('main_entity_funding_rounds')

        # Removing M2M table for field investments on 'Entity'
        db.delete_table('main_entity_investments')

        # Removing M2M table for field acquisitions on 'Entity'
        db.delete_table('main_entity_acquisitions')

        # Removing M2M table for field offices on 'Entity'
        db.delete_table('main_entity_offices')

        # Removing M2M table for field screenshots on 'Entity'
        db.delete_table('main_entity_screenshots')

        # Deleting model 'FundingRound'
        db.delete_table('main_fundinground')

        # Removing M2M table for field investors on 'FundingRound'
        db.delete_table('main_fundinground_investors')

        # Removing M2M table for field investments on 'FundingRound'
        db.delete_table('main_fundinground_investments')

        # Deleting model 'Office'
        db.delete_table('main_office')

        # Deleting model 'Tag'
        db.delete_table('main_tag')


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
            'ipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.IPO']"}),
            'is_company': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_financial_org': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_person': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'number_of_employees': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'offices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Office']", 'symmetrical': 'False'}),
            'overview': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'permalink': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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