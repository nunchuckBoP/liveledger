from django import forms
import app.validators
import app.mixins
import django.core.mail

class LedgerShareForm(forms.Form):
    shared_user = forms.CharField(label='User or Email', max_length=256, \
                                validators=[app.validators.validate_user])
    
class InquireForm(forms.Form):
    item_id = forms.CharField(widget=forms.HiddenInput(), required=True)
    to_user = forms.EmailField(label="To", disabled=True, required=False)
    from_user = forms.EmailField(label="Sender", disabled=True, required=False)
    subject = forms.CharField(label="Subject", max_length=256, disabled=True, required=False)
    message = forms.CharField(label="Message", max_length=1024)

    def send_email(self, to_address, from_address, subject, message):
        django.core.mail.send_mail(
            subject, message, from_address, [to_address]
        )