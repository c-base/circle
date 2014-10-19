# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Topic.etherpad'
        db.delete_column(u'circleapp_topic', 'etherpad')


    def backwards(self, orm):
        # Adding field 'Topic.etherpad'
        db.add_column(u'circleapp_topic', 'etherpad',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=256),
                      keep_default=False)


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
            'Meta': {'ordering': "['date']", 'object_name': 'Circle'},
            'attending_aliens': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'circles_where_alien'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['circle.Alien']"}),
            'attending_board_members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'circles_where_board_member'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['circle.Member']"}),
            'attending_circle_members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'circles_where_circle_member'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['circle.Member']"}),
            'attending_regular_members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'circles_where_regular_member'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['circle.Member']"}),
            'closed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'moderated_circles'", 'null': 'True', 'to': u"orm['circle.Member']"}),
            'opened': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transcript_writers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'transcript_circles'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['circle.Member']"})
        },
        u'circleapp.poll': {
            'Meta': {'object_name': 'Poll'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outcome': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'proposal': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'db_index': 'True'}),
            'topic': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'polls'", 'unique': 'True', 'to': u"orm['circleapp.Topic']"})
        },
        u'circleapp.topic': {
            'Meta': {'ordering': "['created', 'headline']", 'unique_together': "(['circle', 'headline'],)", 'object_name': 'Topic'},
            'applicant': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'circle': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topics'", 'to': u"orm['circleapp.Circle']"}),
            'closed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opened': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sponsor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'topic_sponsorship'", 'null': 'True', 'to': u"orm['circle.Member']"}),
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