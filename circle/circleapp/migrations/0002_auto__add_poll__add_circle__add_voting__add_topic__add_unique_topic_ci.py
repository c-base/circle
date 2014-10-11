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

        # Adding model 'Circle'
        db.create_table(u'circleapp_circle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(unique=True, db_index=True)),
            ('opened', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('closed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('moderator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='moderated_circles', to=orm['circle.Member'])),
        ))
        db.send_create_signal(u'circleapp', ['Circle'])

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

        # Adding M2M table for field attending_regular_members on 'Circle'
        m2m_table_name = db.shorten_name(u'circleapp_circle_attending_regular_members')
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

        # Adding M2M table for field transcript_writers on 'Circle'
        m2m_table_name = db.shorten_name(u'circleapp_circle_transcript_writers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('circle', models.ForeignKey(orm[u'circleapp.circle'], null=False)),
            ('member', models.ForeignKey(orm[u'circle.member'], null=False))
        ))
        db.create_unique(m2m_table_name, ['circle_id', 'member_id'])

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

        # Adding model 'Topic'
        db.create_table(u'circleapp_topic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('circle', self.gf('django.db.models.fields.related.ForeignKey')(related_name='topics', to=orm['circleapp.Circle'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('applicant', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('sponsor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='topic_sponsorship', to=orm['circle.Member'])),
            ('etherpad', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('opened', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('closed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'circleapp', ['Topic'])

        # Adding unique constraint on 'Topic', fields ['circle', 'headline']
        db.create_unique(u'circleapp_topic', ['circle_id', 'headline'])


    def backwards(self, orm):
        # Removing unique constraint on 'Topic', fields ['circle', 'headline']
        db.delete_unique(u'circleapp_topic', ['circle_id', 'headline'])

        # Deleting model 'Poll'
        db.delete_table(u'circleapp_poll')

        # Deleting model 'Circle'
        db.delete_table(u'circleapp_circle')

        # Removing M2M table for field attending_circle_members on 'Circle'
        db.delete_table(db.shorten_name(u'circleapp_circle_attending_circle_members'))

        # Removing M2M table for field attending_board_members on 'Circle'
        db.delete_table(db.shorten_name(u'circleapp_circle_attending_board_members'))

        # Removing M2M table for field attending_regular_members on 'Circle'
        db.delete_table(db.shorten_name(u'circleapp_circle_attending_regular_members'))

        # Removing M2M table for field attending_aliens on 'Circle'
        db.delete_table(db.shorten_name(u'circleapp_circle_attending_aliens'))

        # Removing M2M table for field transcript_writers on 'Circle'
        db.delete_table(db.shorten_name(u'circleapp_circle_transcript_writers'))

        # Deleting model 'Voting'
        db.delete_table(u'circleapp_voting')

        # Deleting model 'Topic'
        db.delete_table(u'circleapp_topic')


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
            'date': ('django.db.models.fields.DateField', [], {'unique': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'moderated_circles'", 'to': u"orm['circle.Member']"}),
            'opened': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transcript_writers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'transcript_circles'", 'symmetrical': 'False', 'to': u"orm['circle.Member']"})
        },
        u'circleapp.poll': {
            'Meta': {'object_name': 'Poll'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outcome': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'proposal': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'db_index': 'True'}),
            'topic': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'polls'", 'unique': 'True', 'to': u"orm['circleapp.Topic']"})
        },
        u'circleapp.topic': {
            'Meta': {'ordering': "['order', 'headline']", 'unique_together': "(['circle', 'headline'],)", 'object_name': 'Topic'},
            'applicant': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'circle': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topics'", 'to': u"orm['circleapp.Circle']"}),
            'closed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'etherpad': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opened': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sponsor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topic_sponsorship'", 'to': u"orm['circle.Member']"})
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