from ashesiundergraduate.tests import AppTest

class FormsTest(AppTest):

    def setUp(self, *args, **kwargs):
        super(FormsTest, self).setUp(*args, **kwargs)

    def save_form(self, form_class, data, files=None, **kwargs):
        parent_obj = kwargs.pop('parent', None)
        form = form_class(data, files, **kwargs)
        if form.is_valid():
            if parent_obj is not None:
                obj = form.save(parent_obj)
            else:
                obj = form.save()
        else:
            return form.errors
        return obj.to_dict()

    def form_test_without_bound_parent_form(self, parent_form_class, child_form_class, parent_data, child_data, **kwargs):
        parent_form = parent_form_class(parent_data, **kwargs)
        if parent_form.is_valid():
            parent_obj = parent_form.save(commit=False)
            form = child_form_class(child_data, obj=parent_obj)
            self.assertRaises(AttributeError, getattr, form, 'is_bound')
