class ReadOnlyFieldsMixin(object):
    readonly_fields = ()

    def __init__(self, *args, **kwargs):
        super(ReadOnlyFieldsMixin, self).__init__(*args, **kwargs)
        for a_field in self.readonly_fields:
            self.fields[a_field].required = False
            self.fields[a_field].disabled = True

    def clean(self):
        initial_values = self.get_initial()
        for a_field in self.readonly_fields:
            self.cleaned_data[a_field] = initial_values[a_field]
        return super(ReadOnlyFieldsMixin, self).clean()