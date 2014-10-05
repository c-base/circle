# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Group'
        db.create_table(u'circleapp_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'circleapp', ['Group'])

        # Adding model 'Member'
        db.create_table(u'circleapp_member', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nick', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'circleapp', ['Member'])

        # Adding M2M table for field groups on 'Member'
        m2m_table_name = db.shorten_name(u'circleapp_member_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('member', models.ForeignKey(orm[u'circleapp.member'], null=False)),
            ('group', models.ForeignKey(orm[u'circleapp.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['member_id', 'group_id'])

        # Adding model 'Circle'
        db.create_table(u'circleapp_circle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('circle_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('aliens', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'circleapp', ['Circle'])

        # Adding M2M table for field circle_member_present on 'Circle'
        m2m_table_name = db.shorten_name(u'circleapp_circle_circle_member_present')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('circle', models.ForeignKey(orm[u'circleapp.circle'], null=False)),
            ('member', models.ForeignKey(orm[u'circleapp.member'], null=False))
        ))
        db.create_unique(m2m_table_name, ['circle_id', 'member_id'])

        # Adding M2M table for field circle_member_excused on 'Circle'
        m2m_table_name = db.shorten_name(u'circleapp_circle_circle_member_excused')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('circle', models.ForeignKey(orm[u'circleapp.circle'], null=False)),
            ('member', models.ForeignKey(orm[u'circleapp.member'], null=False))
        ))
        db.create_unique(m2m_table_name, ['circle_id', 'member_id'])

        # Adding M2M table for field member_present on 'Circle'
        m2m_table_name = db.shorten_name(u'circleapp_circle_member_present')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('circle', models.ForeignKey(orm[u'circleapp.circle'], null=False)),
            ('member', models.ForeignKey(orm[u'circleapp.member'], null=False))
        ))
        db.create_unique(m2m_table_name, ['circle_id', 'member_id'])

        # Adding M2M table for field board_present on 'Circle'
        m2m_table_name = db.shorten_name(u'circleapp_circle_board_present')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('circle', models.ForeignKey(orm[u'circleapp.circle'], null=False)),
            ('member', models.ForeignKey(orm[u'circleapp.member'], null=False))
        ))
        db.create_unique(m2m_table_name, ['circle_id', 'member_id'])

        # Adding model 'Topic'
        db.create_table(u'circleapp_topic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('circle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['circleapp.Circle'])),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'circleapp', ['Topic'])

        # Adding model 'Decision'
        db.create_table(u'circleapp_decision', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['circleapp.Topic'])),
            ('pro', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('con', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('abst', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'circleapp', ['Decision'])

        # Adding model 'Opinion'
        db.create_table(u'circleapp_opinion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['circleapp.Topic'])),
            ('result', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'circleapp', ['Opinion'])


    def backwards(self, orm):
        # Deleting model 'Group'
        db.delete_table(u'circleapp_group')

        # Deleting model 'Member'
        db.delete_table(u'circleapp_member')

        # Removing M2M table for field groups on 'Member'
        db.delete_table(db.shorten_name(u'circleapp_member_groups'))

        # Deleting model 'Circle'
        db.delete_table(u'circleapp_circle')

        # Removing M2M table for field circle_member_present on 'Circle'
        db.delete_table(db.shorten_name(u'circleapp_circle_circle_member_present'))

        # Removing M2M table for field circle_member_excused on 'Circle'
        db.delete_table(db.shorten_name(u'circleapp_circle_circle_member_excused'))

        # Removing M2M table for field member_present on 'Circle'
        db.delete_table(db.shorten_name(u'circleapp_circle_member_present'))

        # Removing M2M table for field board_present on 'Circle'
        db.delete_table(db.shorten_name(u'circleapp_circle_board_present'))

        # Deleting model 'Topic'
        db.delete_table(u'circleapp_topic')

        # Deleting model 'Decision'
        db.delete_table(u'circleapp_decision')

        # Deleting model 'Opinion'
        db.delete_table(u'circleapp_opinion')


    models = {
        u'circleapp.circle': {
            'Meta': {'object_name': 'Circle'},
            'aliens': ('django.db.models.fields.TextField', [], {}),
            'board_present': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'board_present'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['circleapp.Member']"}),
            'circle_date': ('django.db.models.fields.DateTimeField', [], {}),
            'circle_member_excused': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'circle_member_excused'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['circleapp.Member']"}),
            'circle_member_present': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'circle_member_present'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['circleapp.Member']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member_present': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'member_present'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['circleapp.Member']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
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