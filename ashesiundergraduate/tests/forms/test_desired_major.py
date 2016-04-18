from ...models import DesiredMajor, Course
from ...forms import DesiredMajorForm

from . import FormsTest

class DesiredMajorFormTest(FormsTest):
    
    def setUp(self, *args, **kwargs):
        super(DesiredMajorFormTest, self).setUp(*args, **kwargs)
        course_one = Course.objects.create(name='Computer Science')
        self.data = {'desired_major': course_one.pk}

    def test_save_new(self):
        super(DesiredMajorFormTest, self).form_test(DesiredMajorForm, self.data, obj=self.user_app)

    def test_save_existing(self):
        course_two = Course.objects.create(name='Management Information Systems')
        major = DesiredMajor.objects.create(user_application=self.user_app, desired_major=course_two)
        super(DesiredMajorFormTest, self).form_test(DesiredMajorForm, self.data, obj=self.user_app)
