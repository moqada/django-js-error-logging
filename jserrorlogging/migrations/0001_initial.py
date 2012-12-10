# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Log'
        db.create_table('jserrorlogging_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('browser', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('line', self.gf('django.db.models.fields.IntegerField')()),
            ('page', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('when', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('meta', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('jserrorlogging', ['Log'])

    def backwards(self, orm):
        # Deleting model 'Log'
        db.delete_table('jserrorlogging_log')

    models = {
        'jserrorlogging.log': {
            'Meta': {'object_name': 'Log'},
            'browser': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.IntegerField', [], {}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'page': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'when': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['jserrorlogging']