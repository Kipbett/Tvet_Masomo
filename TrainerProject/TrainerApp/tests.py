from django.test import TestCase

# Create your tests here.
from .models import Document, Unit

unit = Unit.objects.get(id=1)
os_doc = Document.objects.filter(unit=unit, document_type='OS').first()
cu_doc = Document.objects.filter(unit=unit, document_type='CU').first()
print(os_doc.file.url if os_doc else "No OS document")
print(cu_doc.file.url if cu_doc else "No CU document")