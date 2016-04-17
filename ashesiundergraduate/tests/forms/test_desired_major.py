from ...models import DesiredMajor, Course
from ...forms import DesiredMajorForm

from . import FormsTest, bind_save_form

class DesiredMajorFormTest(FormsTest):
    
    def setUp(self, *args, **kwargs):
        super(DesiredMajorFormTest, self).setUp(*args, **kwargs)
        self.major = Course.objects.create(name='Computer Science')
        self.data = {'desired_major': self.major.pk}

    def _assert(self, value):
        self.assertEqual(value, self.major)

    def test_save_new(self):
        desired_major = bind_save_form(DesiredMajorForm, self.data, obj=self.user_app)
        self._assert(desired_major.desired_major)

    def test_save_existing(self):
        course_two = Course.objects.create(name='Management Information Systems')
        major = DesiredMajor.objects.create(user_application=self.user_app, desired_major=course_two)

        desired_major = bind_save_form(DesiredMajorForm, self.data, obj=self.user_app)
        self._assert(desired_major.desired_major)
