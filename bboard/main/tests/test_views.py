from django.test import TestCase
from django.urls import reverse

from main.models import Bb, SubRubric, SuperRubric, AdvUser


class IndexTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Creat test user for Bb
        AdvUser.objects.create(
            username='Test_user_1',
            first_name='Test_user1_fn',
            last_name='Test_user1_ln',
            email='test@user1.com',
            is_staff=False,
            is_active=True,
            is_activated=True,
        )
        # Creat test superrubric for Bb
        SuperRubric.objects.create(name='Test_superrubric')
        # Creat test subrubric for Bb
        SubRubric.objects.create(
            name='Test_subrubric',
            super_rubric=SuperRubric.objects.get(name='Test_superrubric')
        )
        # Create 13 Bb for pagination tests
        number_of_bb = 13
        for bb_num in range(number_of_bb):
            Bb.objects.create(
                rubric=SubRubric.objects.get(name='Test_subrubric'),
                title='Test_title%s' % bb_num,
                content='Test_content',
                contacts='Test_contacts',
                author=AdvUser.objects.get(username='Test_user_1')
            )

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('main:index'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('main:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main/index.html')

    def test_number_displayed_ads_is_ten(self):
        resp = self.client.get(reverse('main:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue( len(resp.context['bbs']) == 10)


class Other_pageTest(TestCase):
    def test_other_page_return_404(self):
        wrong_other_page_name = '/wrong/'
        resp = self.client.get(wrong_other_page_name)
        self.assertEqual(resp.status_code, 404)

    def test_other_page_return_200(self):
        true_other_page_name = '/about/'
        resp = self.client.get(true_other_page_name)
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('main:other', kwargs={'page': 'about'}))
        self.assertEqual(resp.status_code, 200)
