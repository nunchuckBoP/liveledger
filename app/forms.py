from django import forms
import app.validators
import app.mixins
from django.core.mail import EmailMessage

class LedgerShareForm(forms.Form):
    shared_user = forms.CharField(label='User or Email', max_length=256, \
                                validators=[app.validators.validate_user])
    
class InquireForm(forms.Form):
    item_id = forms.CharField(widget=forms.HiddenInput(), required=True)
    to_user = forms.EmailField(label="To", disabled=True, required=False)
    from_user = forms.EmailField(label="Sender", disabled=True, required=False)
    subject = forms.CharField(label="Subject", max_length=256, disabled=True, required=False)
    message = forms.CharField(label="Message", max_length=1024)

    def send_email(self, domain_address, to_address, from_address, subject, message):
        # send the email
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=domain_address,
            to=[to_address],
            cc=[from_address],
            reply_to=[domain_address, from_address]
        )
        email.send(fail_silently=False)