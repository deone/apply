from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from setup.models import Organization, Application, UserApplication

class FormsTest(TestCase):

    def setUp(self, *args, **kwargs):
        user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        organization = Organization.objects.create(name='Ecobank Ghana', short_name='Ecobank')
        application = Application.objects.create(
            organization=organization,
            name='Account Opening Form',
            is_open=True,
            deadline=timezone.now()
            )
        self.user_app = UserApplication.objects.create(user=user, application=application)

    def form_test(self, form_class, data, **kwargs):
        parent_obj = kwargs.pop('parent', None)
        form = form_class(data, **kwargs)
        if form.is_valid():
            if parent_obj is not None:
                obj = form.save(parent_obj)
            else:
                obj = form.save()
        else:
            print form.errors

        if obj:
            self.assertEqual(obj.to_dict(), data)

    def form_test_without_bound_parent_form(self, parent_form_class, child_form_class, parent_data, child_data, **kwargs):
        parent_form = parent_form_class(parent_data, **kwargs)
        if parent_form.is_valid():
            parent_obj = parent_form.save(commit=False)
            form = child_form_class(child_data, obj=parent_obj)
            self.assertRaises(AttributeError, getattr, form, 'is_bound')
