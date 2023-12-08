from django import forms


class UserForm(forms.Form):
    square = forms.IntegerField()
    address = forms.CharField()
    email_address = forms.EmailField()
    type = forms.ChoiceField(choices=((1, "Коммерческая"), (2, "Загородная"), (3, "Жилая")))
    field_order = ["type", "square", "address", "email_address"]


class LoadObject(forms.Form):
    obj_id = forms.IntegerField()


class EntityCatalog(forms.Form):
    entity = forms.IntegerField()
