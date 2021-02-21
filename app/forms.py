from django import forms
import app.validators
import app.mixins

class LedgerShareForm(forms.Form):
    shared_user = forms.CharField(label='User or Email', max_length=256, \
                                validators=[app.validators.validate_user])
    
class InquireForm(app.mixins.ReadOnlyFieldsMixin, forms.Form):
    to_user = forms.EmailField(label="To")
    from_user = forms.EmailField(label="Sender")
    subject = forms.CharField(label="Subject", max_length=256)
    message = forms.CharField(label="Message", max_length=1024)
    readonly_fields = ('to_user', 'from_user', 'subject')

    def send_email(self):
        # this sends the email to the user on the inquiry
        pass