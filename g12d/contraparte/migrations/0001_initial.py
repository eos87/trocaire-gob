# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Proyecto'
        db.create_table('contraparte_proyecto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organizacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trocaire.Organizacion'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('codigo', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('inicio', self.gf('django.db.models.fields.DateField')()),
            ('finalizacion', self.gf('django.db.models.fields.DateField')()),
            ('monto_trocaire', self.gf('django.db.models.fields.IntegerField')()),
            ('monto_contrapartida', self.gf('django.db.models.fields.IntegerField')()),
            ('contacto', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('aporta_trocaire', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('contraparte', ['Proyecto'])

        # Adding M2M table for field municipios on 'Proyecto'
        db.create_table('contraparte_proyecto_municipios', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('proyecto', models.ForeignKey(orm['contraparte.proyecto'], null=False)),
            ('municipio', models.ForeignKey(orm['lugar.municipio'], null=False))
        ))
        db.create_unique('contraparte_proyecto_municipios', ['proyecto_id', 'municipio_id'])

        # Adding model 'Resultado'
        db.create_table('contraparte_resultado', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre_corto', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('descripcion', self.gf('django.db.models.fields.TextField')()),
            ('aporta_a', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trocaire.ResultadoPrograma'])),
            ('proyecto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contraparte.Proyecto'])),
        ))
        db.send_create_signal('contraparte', ['Resultado'])


    def backwards(self, orm):
        
        # Deleting model 'Proyecto'
        db.delete_table('contraparte_proyecto')

        # Removing M2M table for field municipios on 'Proyecto'
        db.delete_table('contraparte_proyecto_municipios')

        # Deleting model 'Resultado'
        db.delete_table('contraparte_resultado')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'contraparte.proyecto': {
            'Meta': {'object_name': 'Proyecto'},
            'aporta_trocaire': ('django.db.models.fields.IntegerField', [], {}),
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'contacto': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'finalizacion': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateField', [], {}),
            'monto_contrapartida': ('django.db.models.fields.IntegerField', [], {}),
            'monto_trocaire': ('django.db.models.fields.IntegerField', [], {}),
            'municipios': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lugar.Municipio']", 'symmetrical': 'False'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'organizacion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['trocaire.Organizacion']"})
        },
        'contraparte.resultado': {
            'Meta': {'object_name': 'Resultado'},
            'aporta_a': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['trocaire.ResultadoPrograma']"}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre_corto': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'proyecto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contraparte.Proyecto']"})
        },
        'lugar.departamento': {
            'Meta': {'object_name': 'Departamento'},
            'extension': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'db_index': 'True'})
        },
        'lugar.municipio': {
            'Meta': {'ordering': "['departamento__nombre']", 'object_name': 'Municipio'},
            'departamento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lugar.Departamento']"}),
            'extension': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'latitud': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'longitud': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'db_index': 'True'})
        },
        'trocaire.organizacion': {
            'Meta': {'object_name': 'Organizacion'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'contacto': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'direccion': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'blank': 'True'}),
            'historia': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'nombre_corto': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'telefono': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '12', 'blank': 'True'}),
            'web': ('django.db.models.fields.URLField', [], {'default': "'www.example.com'", 'max_length': '200', 'blank': 'True'})
        },
        'trocaire.resultadoprograma': {
            'Meta': {'object_name': 'ResultadoPrograma'},
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre_corto': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['contraparte']
