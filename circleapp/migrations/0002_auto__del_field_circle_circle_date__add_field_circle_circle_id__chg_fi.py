# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Circle.circle_date'
        db.delete_column(u'circleapp_circle', 'circle_date')

        # Adding field 'Circle.circle_id'
        db.add_column(u'circleapp_circle', 'circle_id',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2014, 10, 4, 0, 0), max_length=10),
                      keep_default=False)


        # Changing field 'Circle.start'
        db.alter_column(u'circleapp_circle', 'start', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Circle.end'
        db.alter_column(u'circleapp_circle', 'end', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):
        # Adding field 'Circle.circle_date'
        db.add_column(u'circleapp_circle', 'circle_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 10, 4, 0, 0)),
                      keep_default=False)

        # Deleting field 'Circle.circle_id'
        db.delete_column(u'circleapp_circle', 'circle_id')


        # Changing field 'Circle.start'
        db.alter_column(u'circleapp_circle', 'start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 10, 4, 0, 0)))

        # Changing field 'Circle.end'
        db.alter_column(u'circleapp_circle', 'end', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 10, 4, 0, 0)))

    models = {
        u'circleapp.circle': {
            'Meta': {'object_name': 'Circle'},
            'aliens': ('django.db.models.fields.TextField', [], {}),
            'board_present': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'board_present'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['circleapp.Member']"}),
            'circle_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'circle_member_excused': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'circle_member_excused'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['circleapp.Member']"}),
            'circle_member_present': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'circle_member_present'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['circleapp.Member']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member_present': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'member_present'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['circleapp.Member']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'circleapp.decision': {
            'Meta': {'object_name': 'Decision'},
            'abst': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'con': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pro': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['circleapp.Topic']"})
        },
        u'circleapp.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'circleapp.member': {
            'Meta': {'object_name': 'Member'},
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['circleapp.Group']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nick': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'circleapp.opinion': {
            'Meta': {'object_name': 'Opinion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['circleapp.Topic']"})
        },
        u'circleapp.topic': {
            'Meta': {'object_name': 'Topic'},
            'circle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['circleapp.Circle']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['circleapp']