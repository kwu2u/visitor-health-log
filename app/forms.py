from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, \
                    SubmitField, SelectField, SelectMultipleField, HiddenField
from wtforms.fields.html5 import DateTimeField, EmailField
from wtforms.validators import InputRequired, DataRequired, Length, Email, \
                               EqualTo
from app.models import User

class LoginForm(Form):
    email = StringField('', validators=[DataRequired()])
    password = PasswordField('', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegisterForm(Form):
    email = EmailField('', [DataRequired(), Email()])
    apartment = SelectField('', choices=[
                                ('2A','2A'),
                                ('2B','2B'),
                                ('2C','2C'),
                                ('2D','2D'),
                                ('2E','2E'),
                                ('2F','2F'),
                                ('2G','2G'),
                                ('3A','3A'),
                                ('3B','3B'),
                                ('3C','3C'),
                                ('3D','3D'),
                                ('3E','3E'),
                                ('3F','3F'),
                                ('3G','3G'),
                                ('4A','4A'),
                                ('4B','4B'),
                                ('4C','4C'),
                                ('4D','4D'),
                                ('4E','4E'),
                                ('4F','4F'),
                                ('4G','4G'),
                                ('5AG','5AG'),
                                ('5B','5B'),
                                ('5C','5C'),
                                ('5D','5D'),
                                ('5E','5E'),
                                ('5F','5F'),
                                ('6A','6A'),
                                ('6B','6B'),
                                ('6C','6C'),
                                ('6D','6D'),
                                ('6E','6E'),
                                ('6F','6F'),
                                ('6G','6G'),
                                ('7A','7A'),
                                ('7B','7B'),
                                ('7C','7C'),
                                ('7D','7D'),
                                ('7E','7E'),
                                ('7F','7F'),
                                ('7G','7G'),
                                ('8A','8A'),
                                ('8B','8B'),
                                ('8C','8C'),
                                ('8D','8D'),
                                ('8EF','8EF'),
                                ('8G','8G'),
                                ('9A','9A'),
                                ('9B','9B'),
                                ('9C','9C'),
                                ('9D','9D'),
                                ('9E','9E'),
                                ('9F','9F'),
                                ('9G10G','9G10G'),
                                ('10AB','10AB'),
                                ('10C','10C'),
                                ('10D','10D'),
                                ('10E','10E'),
                                ('10F','10F'),
                                ('11A','11A'),
                                ('11B','11B'),
                                ('11C','11C'),
                                ('11D','11D'),
                                ('11E','11E'),
                                ('11F','11F'),
                                ('11G','11G'),
                                ('12A','12A'),
                                ('12B','12B'),
                                ('12C','12C'),
                                ('12D','12D'),
                                ('12E','12E'),
                                ('12F','12F'),
                                ('12G','12G'),
                                ('14AB','14AB'),
                                ('14C','14C'),
                                ('14D','14D'),
                                ('14EF','14EF'),
                                ('14G','14G'),
                                ('15A','15A'),
                                ('15B','15B'),
                                ('15C','15C'),
                                ('15D','15D'),
                                ('16A','16A'),
                                ('16B','16B'),
                                ('16C','16C'),
                                ('16D','16D'),
                                ('PHA','PHA'),
                                ('PHB','PHB'),
                                ('PHCD','PHCD'),
                                ('GRND','GRND'),
                                ('OFFICE','OFFICE'),
                                ('MEDICAL','MEDICAL'),
                                ('Staff','Staff')
                            ],
                            validators=[DataRequired()])
    password = PasswordField('',
                             validators=[InputRequired(),
                             EqualTo('pw_confirm', 'Passwords must match')])
    pw_confirm = PasswordField('')
    submit = SubmitField('Submit')

    def validate(self):
        if not Form.validate(self):
            return False
        user_email = User.query.filter_by(email=self.email.data).first()
        if user_email != None:
            self.email.errors.append('Email address already associated with a user name.')
            return False
        return True

class AddVistorForm(Form):
    """Form to add Vistor"""
    datetime = DateTimeField('', validators=[DataRequired()])
    purpose = StringField('', validators=[DataRequired()])
    name = StringField('', validators=[DataRequired()])
    fever = SelectField('a fever of >= 100.4\u00b0 F',
                        choices=[(True,True),(False,False)])
    symptoms = SelectField('a cough or shortness of breath that began within the past 14 days',
                           choices=[(True,True),(False,False)])
    positive_test = SelectField('received a positive result from a COVID-19 test within the past 14 days',
                                choices=[(True,True),(False,False)])
    quarantined = SelectField('notified to quarantine by a medical provider or NYC Test & Trace',
                              choices=[(True,True),(False,False)])
