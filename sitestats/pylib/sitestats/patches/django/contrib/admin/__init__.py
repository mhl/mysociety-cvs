import django.contrib.admin.options
from django.conf import settings
from django.forms.models import inlineformset_factory

def get_formset(self, request, obj=None, **kwargs):
    """Returns a BaseInlineFormSet class for use in admin add/change views."""
    if self.declared_fieldsets:
        fields = flatten_fieldsets(self.declared_fieldsets)
    else:
        fields = None
    if self.exclude is None:
        exclude = []
    else:
        exclude = list(self.exclude)
    defaults = {
        "form": self.form,
        "formset": self.formset,
        "fk_name": self.fk_name,
        "fields": fields,
        "exclude": exclude + kwargs.get("exclude", []),
        "formfield_callback": self.formfield_for_dbfield,
        "extra": self.extra,
        "max_num": self.max_num,
        "can_delete": self.can_delete,
    }
    defaults.update(kwargs)
    return inlineformset_factory(self.parent_model, self.model, **defaults)

django.contrib.admin.options.InlineModelAdmin.can_delete = True    
django.contrib.admin.options.InlineModelAdmin.get_formset = get_formset