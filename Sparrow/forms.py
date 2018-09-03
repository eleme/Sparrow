from django import forms

class ApiCreateForm(forms.Form):
    path = forms.CharField(max_length=128)
    method = forms.CharField(max_length=8)
    name = forms.CharField(max_length=128)
    note = forms.CharField(max_length=512, required=False)
    status = forms.IntegerField()
    responseJson = forms.CharField(widget=forms.Textarea)

class ApiUpdateForm(forms.Form):
    path = forms.CharField(max_length=128)
    method = forms.CharField(max_length=8)
    name = forms.CharField(max_length=128)
    note = forms.CharField(max_length=512, required=False)
    status = forms.IntegerField()
    responseJson = forms.CharField(widget=forms.Textarea)

class ProjectCreateForm(forms.Form):
    name = forms.CharField(max_length=128)
    note = forms.CharField(max_length=512, required=False)
    permissionType = forms.IntegerField()
    status = forms.IntegerField()

class ProjectUpateForm(forms.Form):
    name = forms.CharField(max_length=128)
    note = forms.CharField(max_length=512, required=False)
    permissionType = forms.IntegerField()
    status = forms.IntegerField()

class ResTemplateCreateForm(forms.Form):
    name = forms.CharField(max_length=128)
    note = forms.CharField(max_length=512, required=False)
    type =  forms.IntegerField()
    mimeType = forms.IntegerField()
    responseJson = forms.CharField(widget=forms.Textarea())

class ResTemplateUpdateForm(forms.Form):
    name = forms.CharField(max_length=128)
    note = forms.CharField(max_length=512, required=False)
    type = forms.IntegerField()
    mimeType = forms.IntegerField()
    responseJson = forms.CharField(widget=forms.Textarea())