# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Topic.applicant'
        db.delete_column(u'circleapp_topic', 'applicant')

        # Adding field 'Topic.applicant_member'
        db.add_column(u'circleapp_topic', 'applicant_member',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='topic_applications', null=True, to=orm['circle.Member']),
                      keep_default=False)

        # Adding field 'Topic.applicant_alien'
        db.add_column(u'circleapp_topic', 'applicant_alien',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='topic_applications', null=True, to=orm['circle.Alien']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Topic.applicant'
        db.add_column(u'circleapp_topic', 'applicant',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64),
                      keep_default=False)

        # Deleting field 'Topic.applicant_member'
        db.delete_column(u'circleapp_topic', 'applicant_member_id')

        # Deleting field 'Topic.applicant_alien'
        db.delete_column(u'circleapp_topic', 'applicant_alien_id')


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
        },
        u'circleapp.circle': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Circle'},
            'closed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opened': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'circleapp.guest': {
            'Meta': {'object_name': 'Guest'},
            'alien': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participations'", 'to': u"orm['circle.Alien']"}),
            'check_in': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'check_out': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'circle': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'guests'", 'to': u"orm['circleapp.Circle']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'circleapp.participant': {
            'Meta': {'object_name': 'Participant'},
            'check_in': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'check_out': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'circle': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participants'", 'to': u"orm['circleapp.Circle']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participations'", 'to': u"orm['circle.Member']"}),
            'role': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        u'circleapp.poll': {
            'Meta': {'object_name': 'Poll'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outcome': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'proposal': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'db_index': 'True'}),
            'topic': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'polls'", 'unique': 'True', 'to': u"orm['circleapp.Topic']"})
        },
        u'circleapp.topic': {
            'Meta': {'ordering': "['-created', 'headline']", 'unique_together': "(['circle', 'headline'],)", 'object_name': 'Topic'},
            'applicant_alien': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'topic_applications'", 'null': 'True', 'to': u"orm['circle.Alien']"}),
            'applicant_member': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'topic_applications'", 'null': 'True', 'to': u"orm['circle.Member']"}),
            'circle': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topics'", 'to': u"orm['circleapp.Circle']"}),
            'closed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opened': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sponsor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'topic_sponsorships'", 'null': 'True', 'to': u"orm['circle.Member']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'})
        },
        u'circleapp.voting': {
            'Meta': {'object_name': 'Voting'},
            'abstentions': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.IntegerField', [], {}),
            'positive': ('django.db.models.fields.IntegerField', [], {}),
            'proposal': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'db_index': 'True'}),
            'topic': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'voting'", 'unique': 'True', 'to': u"orm['circleapp.Topic']"})
        }
    }

    complete_apps = ['circleapp']