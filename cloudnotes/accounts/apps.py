from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        try:
            from bson import ObjectId
            from django.db.models.fields import AutoField, BigAutoField, SmallAutoField
            _orig_get_prep_value = AutoField.get_prep_value
            def _patched_get_prep_value(self, value):
                if isinstance(value, ObjectId) or (isinstance(value, str) and len(value) == 24):
                    return value
                try:
                    return _orig_get_prep_value(self, value)
                except (TypeError, ValueError):
                    return value
            AutoField.get_prep_value = _patched_get_prep_value
            BigAutoField.get_prep_value = _patched_get_prep_value
            SmallAutoField.get_prep_value = _patched_get_prep_value

            from django.contrib.auth.models import User
            from django_mongodb_backend.fields import ObjectIdAutoField
            pk_field = ObjectIdAutoField(primary_key=True)
            pk_field.model = User
            pk_field.name = 'id'
            pk_field.attname = 'id'
            pk_field.db_column = '_id'
            pk_field.column = '_id'
            pk_field.concrete = True
            pk_field.is_relation = False
            pk_field.editable = False

            User._meta.local_fields = [pk_field if f.name == 'id' else f for f in User._meta.local_fields]
            User._meta.fields = [pk_field if f.name == 'id' else f for f in User._meta.fields]
            User._meta.pk = pk_field
            User._meta.auto_field = pk_field
            User._meta._expire_cache()
        except Exception:
            pass
