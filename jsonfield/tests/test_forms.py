from django.test import TestCase as DjangoTestCase
from django.utils import unittest
from django.forms import ValidationError

from jsonfield.forms import JSONFormField
from jsonfield.tests.jsonfield_test_app.forms import JSONTestForm, JSONTestModelForm

class JSONFormFieldTest(DjangoTestCase):
    def test_form_field_clean_empty_object(self):
        field = JSONFormField(required=False)
        self.assertEqual({}, field.clean('{}'))
        
    def test_form_field_clean_object(self):
        field = JSONFormField(required=False)
        self.assertEqual(
            {'foo':'bar', 'baz':2},
            field.clean('{"foo":"bar","baz":2}')
        )

    def test_form_field_widget(self):
        field = JSONFormField(required=False)
        self.assertIn(
            '{\n  &quot;a&quot;: true\n}',
            field.widget.render('json', {"a": True})
        )

    def test_form_field_clean_empty_array(self):
        field = JSONFormField(required=False)
        self.assertEqual([],field.clean('[]'))
    
    def test_required_form_field_array(self):
        field = JSONFormField(required=True)
        self.assertEqual([], field.clean('[]'))
        
    def test_required_form_field_object(self):
        field = JSONFormField(required=True)
        self.assertEqual({}, field.clean('{}'))
    
    def test_required_form_field_empty(self):
        field = JSONFormField(required=True)
        with self.assertRaises(ValidationError):
            field.clean('')
    
    def test_invalid_json(self):
        field = JSONFormField(required=True)
        
        with self.assertRaises(ValidationError):
            field.clean('{"foo"}')

class JSONFormTest(DjangoTestCase):
    def test_form_clean(self):
        form = JSONTestForm({})
        self.assertFalse(form.is_valid())
    

class JSONFormMultipleSelectFieldTest(DjangoTestCase):
    def test_multiple_select_data(self):
        form = JSONTestForm({'json_data': ['SA', 'WA']})
        assert form.is_valid()
        
        self.assertEqual(['SA', 'WA'], form.cleaned_data['json_data'])


