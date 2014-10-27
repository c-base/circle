# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Poll'
        db.create_table(u'circleapp_poll', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('topic', self.gf('django.db.models.fields.related.OneToOneField')(related_name='polls', unique=True, to=orm['circleapp.Topic'])),
            ('proposal', self.gf('django.db.models.fields.CharField')(max_length=1024, db_index=True)),
            ('outcome', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal(u'circleapp', ['Poll'])

        # Adding model 'Participant'
        db.create_table(u'circleapp_participant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('circle', self.gf('django.db.models.fields.related.ForeignKey')(related_name='participants', to=orm['circleapp.Circle'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='participations', to=orm['auth.User'])),
            ('check_in', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('check_out', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('role', self.gf('django.db.models.fields.CharField')(default='', max_length=16, null=True, blank=True)),
        ))
        db.send_create_signal(u'circleapp', ['Participant'])

        # Adding model 'Topic'
        db.create_table(u'circleapp_topic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('circle', self.gf('django.db.models.fields.related.ForeignKey')(related_name='topics', to=orm['circleapp.Circle'])),
            ('applicant', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='topic_applications', null=True, to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('sponsor', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='topic_sponsorships', null=True, to=orm['auth.User'])),
            ('opened', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('closed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36, db_index=True)),
            ('transcript_protocol', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
        ))
        db.send_create_signal(u'circleapp', ['Topic'])

        # Adding unique constraint on 'Topic', fields ['circle', 'headline']
        db.create_unique(u'circleapp_topic', ['circle_id', 'headline'])

        # Adding model 'Circle'
        db.create_table(u'circleapp_circle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(db_index=True, unique=True, null=True, blank=True)),
            ('opened', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('closed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'circleapp', ['Circle'])

        # Adding model 'Voting'
        db.create_table(u'circleapp_voting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('topic', self.gf('django.db.models.fields.related.OneToOneField')(related_name='voting', unique=True, to=orm['circleapp.Topic'])),
            ('proposal', self.gf('django.db.models.fields.CharField')(max_length=1024, db_index=True)),
            ('positive', self.gf('django.db.models.fields.IntegerField')()),
            ('negative', self.gf('django.db.models.fields.IntegerField')()),
            ('abstentions', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'circleapp', ['Voting'])

        # Adding model 'TopicRelation'
        db.create_table(u'circleapp_topicrelation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('topic_from', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relation_from', to=orm['circleapp.Topic'])),
            ('topic_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relation_to', to=orm['circleapp.Topic'])),
            ('relation', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'circleapp', ['TopicRelation'])

        # Adding unique constraint on 'TopicRelation', fields ['topic_from', 'topic_to', 'relation']
        db.create_unique(u'circleapp_topicrelation', ['topic_from_id', 'topic_to_id', 'relation'])


    def backwards(self, orm):
        # Removing unique constraint on 'TopicRelation', fields ['topic_from', 'topic_to', 'relation']
        db.delete_unique(u'circleapp_topicrelation', ['topic_from_id', 'topic_to_id', 'relation'])

        # Removing unique constraint on 'Topic', fields ['circle', 'headline']
        db.delete_unique(u'circleapp_topic', ['circle_id', 'headline'])

        # Deleting model 'Poll'
        db.delete_table(u'circleapp_poll')

        # Deleting model 'Participant'
        db.delete_table(u'circleapp_participant')

        # Deleting model 'Topic'
        db.delete_table(u'circleapp_topic')

        # Deleting model 'Circle'
        db.delete_table(u'circleapp_circle')

        # Deleting model 'Voting'
        db.delete_table(u'circleapp_voting')

        # Deleting model 'TopicRelation'
        db.delete_table(u'circleapp_topicrelation')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'circleapp.circle': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Circle'},
            'closed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opened': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'circleapp.participant': {
            'Meta': {'object_name': 'Participant'},
            'check_in': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'check_out': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'circle': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participants'", 'to': u"orm['circleapp.Circle']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participations'", 'to': u"orm['auth.User']"})
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
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'topic_applications'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'circle': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topics'", 'to': u"orm['circleapp.Circle']"}),
            'closed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opened': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sponsor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'topic_sponsorships'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'transcript_protocol': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'db_index': 'True'})
        },
        u'circleapp.topicrelation': {
            'Meta': {'unique_together': "(['topic_from', 'topic_to', 'relation'],)", 'object_name': 'TopicRelation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'topic_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_from'", 'to': u"orm['circleapp.Topic']"}),
            'topic_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relation_to'", 'to': u"orm['circleapp.Topic']"})
        },
        u'circleapp.voting': {
            'Meta': {'object_name': 'Voting'},
            'abstentions': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.IntegerField', [], {}),
            'positive': ('django.db.models.fields.IntegerField', [], {}),
            'proposal': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'db_index': 'True'}),
            'topic': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'voting'", 'unique': 'True', 'to': u"orm['circleapp.Topic']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['circleapp']