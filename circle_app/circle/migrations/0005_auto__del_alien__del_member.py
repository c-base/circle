# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Alien'
        db.delete_table(u'circle_alien')

        # Deleting model 'Member'
        db.delete_table(u'circle_member')

        # Removing M2M table for field groups on 'Member'
        db.delete_table(db.shorten_name(u'circle_member_groups'))


    def backwards(self, orm):
        # Adding model 'Alien'
        db.create_table(u'circle_alien', (
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('compatibility', self.gf('django.db.models.fields.CharField')(default='dunno', max_length=8)),
            ('email', self.gf('django.db.models.fields.EmailField')(blank=True, max_length=75, unique=True, db_index=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'circle', ['Alien'])

        # Adding model 'Member'
        db.create_table(u'circle_member', (
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('crew_name', self.gf('django.db.models.fields.CharField')(max_length=256, unique=True, db_index=True)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(blank=True, max_length=75, unique=True, db_index=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'circle', ['Member'])

        # Adding M2M table for field groups on 'Member'
        m2m_table_name = db.shorten_name(u'circle_member_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('member', models.ForeignKey(orm[u'circle.member'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['member_id', 'group_id'])


    models = {
        
    }

    complete_apps = ['circle']