from datetime import datetime

from django.test import TestCase, override_settings

from ..models import Student, Group, MonthJournal


@override_settings(LANGUAGE_CODE='en')
class ModelsTest(TestCase):
    """Test models"""

    def setUp(self):
        self.student = Student(first_name='Demo', last_name='Student')
        self.group = Group(title='Title')
        self.group1 = Group(title='Title', leader=self.student)
        self.journal = MonthJournal(student=self.student, date=datetime.today())


    def test_student_unicode(self):
        self.assertEqual(unicode(self.student), u'Demo Student')

    def test_group_unicode(self):
        # test without leader
        self.assertEqual(unicode(self.group), u'Title')

        # test with leader
        self.assertEqual(unicode(self.group1), u'Title (Demo Student)')

    def test_journal_unicode(self):
        self.assertEqual(unicode(self.journal), u'Student: %d, %d' % (
            datetime.today().month,
            datetime.today().year))