# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Alien'
        db.create_table(u'circle_alien', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('compatibility', self.gf('django.db.models.fields.CharField')(default='dunno', max_length=8)),
        ))
        db.send_create_signal(u'circle', ['Alien'])

        # Adding index on 'Member', fields ['crew_name']
        db.create_index(u'circle_member', ['crew_name'])

        # Adding index on 'Member', fields ['email']
        db.create_index(u'circle_member', ['email'])


    def backwards(self, orm):
        # Removing index on 'Member', fields ['email']
        db.delete_index(u'circle_member', ['email'])

        # Removing index on 'Member', fields ['crew_name']
        db.delete_index(u'circle_member', ['crew_name'])

        # Deleting model 'Alien'
        db.delete_table(u'circle_alien')


    models = {
        u'circle.alien': {
            'Meta': {'object_name': 'Alien'},
            'compatibility': ('django.db.models.fields.CharField', [], {'default': "'dunno'", 'max_length': '8'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        u'circle.member': {
            'Meta': {'object_name': 'Member'},
            'crew_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256', 'db_index': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['circle']