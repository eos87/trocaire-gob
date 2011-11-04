# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Output'
        db.create_table('contraparte_output', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('params', self.gf('django.db.models.fields.TextField')()),
            ('comment', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('file', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('contraparte', ['Output'])


    def backwards(self, orm):
        
        # Deleting model 'Output'
        db.delete_table('contraparte_output')


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
        'contraparte.actividad': {
            'Meta': {'object_name': 'Actividad'},
            'acuerdos': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'adultos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'aprendizaje': ('django.db.models.fields.IntegerField', [], {}),
            'autoridades': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comentarios': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'comunidad': ('smart_selects.db_fields.ChainedForeignKey', [], {'to': "orm['lugar.Comunidad']"}),
            'efectividad': ('django.db.models.fields.IntegerField', [], {}),
            'ejes_transversales': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['trocaire.EjeTransversal']"}),
            'empoderamiento': ('django.db.models.fields.IntegerField', [], {}),
            'estudiantes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            'foto1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'foto2': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'foto3': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'hombres': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jovenes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lideres': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'maestros': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'mes': ('django.db.models.fields.IntegerField', [], {}),
            'miembros': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'mujeres': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'municipio': ('smart_selects.db_fields.ChainedForeignKey', [], {'to': "orm['lugar.Municipio']"}),
            'ninos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'no_dato': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_dato1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nombre_actividad': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'organizacion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['trocaire.Organizacion']"}),
            'participacion': ('django.db.models.fields.IntegerField', [], {}),
            'persona_organiza': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contraparte.Organizador']"}),
            'pobladores': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'proyecto': ('smart_selects.db_fields.ChainedForeignKey', [], {'to': "orm['contraparte.Proyecto']"}),
            'relevancia': ('django.db.models.fields.IntegerField', [], {}),
            'resultado': ('smart_selects.db_fields.ChainedForeignKey', [], {'to': "orm['contraparte.Resultado']"}),
            'tema_actividad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['trocaire.Tema']"}),
            'tipo_actividad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['trocaire.TipoActividad']"}),
            'video': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'contraparte.organizador': {
            'Meta': {'object_name': 'Organizador'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'contraparte.output': {
            'Meta': {'object_name': 'Output'},
            'comment': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'file': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'params': ('django.db.models.fields.TextField', [], {}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
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
        'lugar.comunidad': {
            'Meta': {'object_name': 'Comunidad'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lugar.Municipio']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '40'})
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
        'trocaire.ejetransversal': {
            'Meta': {'object_name': 'EjeTransversal'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '150'})
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
        },
        'trocaire.tema': {
            'Meta': {'object_name': 'Tema'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'trocaire.tipoactividad': {
            'Meta': {'object_name': 'TipoActividad'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['contraparte']
