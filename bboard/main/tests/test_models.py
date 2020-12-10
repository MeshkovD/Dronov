from django.test import TestCase

from main.models import Rubric, AdvUser, SuperRubric, SubRubric


class AdvUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        AdvUser.objects.create(
            username='Test_user_1',
            first_name='Test_user_fn',
            last_name='Test_user_ln',
            email='test@user.com',
            is_staff=False,
            is_active=True,
            is_activated=True,
        )

    def setUp(self):
        AdvUser.objects.create(
            username='Test_user_2',
            first_name='Test_user2_fn',
            last_name='Test_user2_ln',
            email='test@user2.com',
            is_staff=False,
            is_active=True,
            is_activated=True,
        )

    def test_is_activated_label(self):
        test_user_1 = AdvUser.objects.get(username='Test_user_1')
        field_label = test_user_1._meta.get_field('is_activated').verbose_name
        self.assertEquals(field_label, 'Прошёл активацию?')

    def test_send_messages_label(self):
        test_user_1 = AdvUser.objects.get(username='Test_user_1')
        field_label = test_user_1._meta.get_field('send_messages').verbose_name
        self.assertEquals(field_label, 'Слать оповещения о новых комментариях?')

    def test_delete_method(self):
        test_user_2 = AdvUser.objects.get(username='Test_user_2')
        test_user_2.delete()
        self.assertEquals(test_user_2.pk, None)


class RubricModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Rubric.objects.create(name='Test_rubric_1')

    def test_name_label(self):
        rubric = Rubric.objects.get(name='Test_rubric_1')
        field_label = rubric._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название')

    def test_first_name_max_length(self):
        rubric = Rubric.objects.get(name='Test_rubric_1')
        max_length = rubric._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)


class SuperRubricModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        SuperRubric.objects.create(
            name='Test_Super_Rrubric_1',
        )
        SuperRubric.objects.create(
            name='Test_Super_Rrubric_2',
        )
        SubRubric.objects.create(
            name='Test_Sub_Rrubric',
            super_rubric=SuperRubric.objects.get(name='Test_Super_Rrubric_1')
        )

    def test_superrubric_manager(self):
        new_super_rubric = SuperRubric.objects.get(name='Test_Super_Rrubric_1')
        super_rubric_queryset = SuperRubric.objects.all()
        value_of_field_super_rubric = new_super_rubric.super_rubric
        # Проверяем, что менеджер модели возвращает queryset верного размера,
        self.assertEquals(len(super_rubric_queryset), 2)
        # Проверяем, что менеджер модели вернул экземпляры с значением поля super_rubric=None
        self.assertIsNone(value_of_field_super_rubric)

    def test_str_method(self):
        new_super_rubric = SuperRubric.objects.get(name='Test_Super_Rrubric_1')
        self.assertEquals(str(new_super_rubric), 'Test_Super_Rrubric_1')

    def test_model_is_proxy(self):
        new_super_rubric = SuperRubric.objects.get(name='Test_Super_Rrubric_1')
        self.assertTrue(new_super_rubric._meta.proxy)

    def test_ordering(self):
        new_super_rubric = SuperRubric.objects.get(name='Test_Super_Rrubric_1')
        self.assertEquals(new_super_rubric._meta.ordering, ('order', 'name'))

    def test_verbose_name_label(self):
        new_super_rubric = SuperRubric.objects.get(name='Test_Super_Rrubric_1')
        verbose_name = new_super_rubric._meta.verbose_name
        self.assertEquals(verbose_name, 'Надрубрика')

    def test_verbose_name_plural_label(self):
        new_super_rubric = SuperRubric.objects.get(name='Test_Super_Rrubric_1')
        verbose_name_plural = new_super_rubric._meta.verbose_name_plural
        self.assertEquals(verbose_name_plural, 'Надрубрики')


class SubRubricModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        SuperRubric.objects.create(
            name='Test_Super_Rrubric',
        )
        SubRubric.objects.create(
            name='Test_Sub_Rrubric_1',
            super_rubric=SuperRubric.objects.get(name='Test_Super_Rrubric')        )
        SubRubric.objects.create(
            name='Test_Sub_Rrubric_2',
            super_rubric=SuperRubric.objects.get(name='Test_Super_Rrubric')
        )

    def test_subrubric_manager(self):
        new_sub_rubric = SubRubric.objects.get(name='Test_Sub_Rrubric_1')
        sub_rubric_queryset = SubRubric.objects.all()
        value_of_field_super_rubric = new_sub_rubric.super_rubric
        # Проверяем, что менеджер модели возвращает queryset верного размера,
        self.assertEquals(len(sub_rubric_queryset), 2)
        # Проверяем, что менеджер модели вернул экземпляры с значением поля super_rubric!=None
        self.assertIsNotNone(value_of_field_super_rubric)

    def test_str_method(self):
        new_sub_rubric = SubRubric.objects.get(name='Test_Sub_Rrubric_1')
        self.assertEquals(str(new_sub_rubric), 'Test_Super_Rrubric - Test_Sub_Rrubric_1')

    def test_model_is_proxy(self):
        new_sub_rubric = SubRubric.objects.get(name='Test_Sub_Rrubric_1')
        self.assertTrue(new_sub_rubric._meta.proxy)

    def test_ordering(self):
        new_sub_rubric = SubRubric.objects.get(name='Test_Sub_Rrubric_1')
        self.assertEquals(new_sub_rubric._meta.ordering, ('super_rubric__order', 'super_rubric__name', 'order', 'name'))

    def test_verbose_name_label(self):
        new_sub_rubric = SubRubric.objects.get(name='Test_Sub_Rrubric_1')
        verbose_name = new_sub_rubric._meta.verbose_name
        self.assertEquals(verbose_name, 'Подрубрика')

    def test_verbose_name_plural_label(self):
        new_sub_rubric = SubRubric.objects.get(name='Test_Sub_Rrubric_1')
        verbose_name_plural = new_sub_rubric._meta.verbose_name_plural
        self.assertEquals(verbose_name_plural, 'Подрубрики')


class BbModelTest(TestCase):
    pass


class AdditionalImageModelTest(TestCase):
    pass


class CommentModelTest(TestCase):
    pass