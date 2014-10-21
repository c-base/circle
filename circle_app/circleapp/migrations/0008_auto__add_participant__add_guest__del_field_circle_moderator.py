# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Participant'
        db.create_table(u'circleapp_participant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('circle', self.gf('django.db.models.fields.related.ForeignKey')(related_name='participants', to=orm['circleapp.Circle'])),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(related_name='participations', to=orm['circle.Member'])),
            ('role', self.gf('django.db.models.fields.CharField')(default='participant', max_length=16)),
            ('check_in', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('check_out', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'circleapp', ['Participant'])

        # Adding model 'Guest'
        db.create_table(u'circleapp_guest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('circle', self.gf('django.db.models.fields.related.ForeignKey')(related_name='guests', to=orm['circleapp.Circle'])),
            ('alien', self.gf('django.db.models.fields.related.ForeignKey')(related_name='participations', to=orm['circle.Alien'])),
            ('check_in', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('check_out', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'circleapp', ['Guest'])

        # Deleting field 'Circle.moderator'
        db.delete_column(u'circleapp_circle', 'moderator_id')

        # Removing M2M table for field transcript_writers on 'Circle'
        db.delete_table(db.shorten_name(u'circleapp_circle_transcript_writers'))

        # Removing M2M table for field attending_regular_members on 'Circle'
        db.delete_table(db.shorten_name(u'circleapp_circle_attending_regular_members'))

        # Removing M2M table for field attending_circle_members on 'Circle'
        db.delete_table(db.shorten_name(u'circleapp_circle_attending_circle_members'))

        # Removing M2M table for field attending_board_members on 'Circle'
        db.delete_table(db.shorten_name(u'circleapp_circle_attending_board_members'))

        # Removing M2M table for field attending_aliens on 'Circle'
        db.delete_table(db.shorten_name(u'circleapp_circle_attending_aliens'))


    def backwards(self, orm):
        # Deleting model 'Participant'
        db.delete_table(u'circleapp_participant')

        # Deleting model 'Guest'
        db.delete_table(u'circleapp_guest')

        # Adding field 'Circle.moderator'
        db.add_column(u'circleapp_circle', 'moderator',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='moderated_circles', null=True, to=orm['circle.Member'], blank=True),
                      keep_default=False)

        # Adding M2M table for field transcript_writers on 'Circle'
        m2m_table_name = db.shorten_name(u'circleapp_circle_transcript_writers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('circle', models.ForeignKey(orm[u'circleapp.circle'], null=False)),
            ('member', models.ForeignKey(orm[u'circle.member'], null=False))
        ))
        db.create_unique(m2m_table_name, ['circle_id', 'member_id'])

        # Adding M2M table for field attending_regular_members on 'Circle'
        m2m_table_name = db.shorten_name(u'circleapp_circle_attending_regular_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('circle', models.ForeignKey(orm[u'circleapp.circle'], null=False)),
            ('member', models.ForeignKey(orm[u'circle.member'], null=False))
        ))
        db.create_unique(m2m_table_name, ['circle_id', 'member_id'])

        # Adding M2M table for field attending_circle_members on 'Circle'
        m2m_table_name = db.shorten_name(u'circleapp_circle_attending_circle_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('circle', models.ForeignKey(orm[u'circleapp.circle'], null=False)),
            ('member', models.ForeignKey(orm[u'circle.member'], null=False))
        ))
        db.create_unique(m2m_table_name, ['circle_id', 'member_id'])

        # Adding M2M table for field attending_board_members on 'Circle'
        m2m_table_name = db.shorten_name(u'circleapp_circle_attending_board_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('circle', models.ForeignKey(orm[u'circleapp.circle'], null=False)),
            ('member', models.ForeignKey(orm[u'circle.member'], null=False))
        ))
        db.create_unique(m2m_table_name, ['circle_id', 'member_id'])

        # Adding M2M table for field attending_aliens on 'Circle'
        m2m_table_name = db.shorten_name(u'circleapp_circle_attending_aliens')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('circle', models.ForeignKey(orm[u'circleapp.circle'], null=False)),
            ('alien', models.ForeignKey(orm[u'circle.alien'], null=False))
        ))
        db.create_unique(m2m_table_name, ['circle_id', 'alien_id'])


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
            'check_in': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'check_out': ('django.db.models.fields.DateTimeField', [], {}),
            'circle': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'guests'", 'to': u"orm['circleapp.Circle']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'circleapp.participant': {
            'Meta': {'object_name': 'Participant'},
            'check_in': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'check_out': ('django.db.models.fields.DateTimeField', [], {}),
            'circle': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participants'", 'to': u"orm['circleapp.Circle']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participations'", 'to': u"orm['circle.Member']"}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'participant'", 'max_length': '16'})
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