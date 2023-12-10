from django import forms


class UploadFilesForm(forms.Form):
    excel_file = forms.FileField()
    image_archive = forms.FileField()


class ZipUploadForm(forms.Form):
    zip_file = forms.FileField(label="Select a ZIP file")
