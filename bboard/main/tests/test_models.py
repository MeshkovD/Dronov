import tempfile

from django.test import TestCase

from main.models import Rubric, AdvUser, SuperRubric, SubRubric, Bb, AdditionalImage, Comment


class AdvUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
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
        # Set up non-modified objects used by all test methods
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
        # Set up non-modified objects used by all test methods
        SuperRubric.objects.create(
            name='Test_Super_Rubric_1',
        )
        SuperRubric.objects.create(
            name='Test_Super_Rubric_2',
        )
        SubRubric.objects.create(
            name='Test_Sub_Rubric',
            super_rubric=SuperRubric.objects.get(name='Test_Super_Rubric_1')
        )

    def test_superrubric_manager(self):
        new_super_rubric = SuperRubric.objects.get(name='Test_Super_Rubric_1')
        super_rubric_queryset = SuperRubric.objects.all()
        value_of_field_super_rubric = new_super_rubric.super_rubric
        # Проверяем, что менеджер модели возвращает queryset верного размера,
        self.assertEquals(len(super_rubric_queryset), 2)
        # Проверяем, что менеджер модели вернул экземпляры с значением поля super_rubric=None
        self.assertIsNone(value_of_field_super_rubric)

    def test_str_method(self):
        new_super_rubric = SuperRubric.objects.get(name='Test_Super_Rubric_1')
        self.assertEquals(str(new_super_rubric), 'Test_Super_Rubric_1')

    def test_model_is_proxy(self):
        new_super_rubric = SuperRubric.objects.get(name='Test_Super_Rubric_1')
        self.assertTrue(new_super_rubric._meta.proxy)

    def test_ordering(self):
        new_super_rubric = SuperRubric.objects.get(name='Test_Super_Rubric_1')
        self.assertEquals(new_super_rubric._meta.ordering, ('order', 'name'))

    def test_verbose_name_label(self):
        new_super_rubric = SuperRubric.objects.get(name='Test_Super_Rubric_1')
        verbose_name = new_super_rubric._meta.verbose_name
        self.assertEquals(verbose_name, 'Надрубрика')

    def test_verbose_name_plural_label(self):
        new_super_rubric = SuperRubric.objects.get(name='Test_Super_Rubric_1')
        verbose_name_plural = new_super_rubric._meta.verbose_name_plural
        self.assertEquals(verbose_name_plural, 'Надрубрики')


class SubRubricModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        SuperRubric.objects.create(
            name='Test_Super_Rubric',
        )
        SubRubric.objects.create(
            name='Test_Sub_Rubric_1',
            super_rubric=SuperRubric.objects.get(name='Test_Super_Rubric'))
        SubRubric.objects.create(
            name='Test_Sub_Rubric_2',
            super_rubric=SuperRubric.objects.get(name='Test_Super_Rubric')
        )

    def test_subrubric_manager(self):
        new_sub_rubric = SubRubric.objects.get(name='Test_Sub_Rubric_1')
        sub_rubric_queryset = SubRubric.objects.all()
        value_of_field_super_rubric = new_sub_rubric.super_rubric
        # Проверяем, что менеджер модели возвращает queryset верного размера,
        self.assertEquals(len(sub_rubric_queryset), 2)
        # Проверяем, что менеджер модели вернул экземпляры с значением поля super_rubric!=None
        self.assertIsNotNone(value_of_field_super_rubric)

    def test_str_method(self):
        new_sub_rubric = SubRubric.objects.get(name='Test_Sub_Rubric_1')
        self.assertEquals(str(new_sub_rubric), 'Test_Super_Rubric - Test_Sub_Rubric_1')

    def test_model_is_proxy(self):
        new_sub_rubric = SubRubric.objects.get(name='Test_Sub_Rubric_1')
        self.assertTrue(new_sub_rubric._meta.proxy)

    def test_ordering(self):
        new_sub_rubric = SubRubric.objects.get(name='Test_Sub_Rubric_1')
        self.assertEquals(new_sub_rubric._meta.ordering, ('super_rubric__order', 'super_rubric__name', 'order', 'name'))

    def test_verbose_name_label(self):
        new_sub_rubric = SubRubric.objects.get(name='Test_Sub_Rubric_1')
        verbose_name = new_sub_rubric._meta.verbose_name
        self.assertEquals(verbose_name, 'Подрубрика')

    def test_verbose_name_plural_label(self):
        new_sub_rubric = SubRubric.objects.get(name='Test_Sub_Rubric_1')
        verbose_name_plural = new_sub_rubric._meta.verbose_name_plural
        self.assertEquals(verbose_name_plural, 'Подрубрики')


class BbModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        AdvUser.objects.create(
            username='Test_user_1',
            first_name='Test_user_fn',
            last_name='Test_user_ln',
            email='test@user.com',
            is_staff=False,
            is_active=True,
            is_activated=True,
        )

        SuperRubric.objects.create(
            name='Test_Super_Rubric',
        )

        SubRubric.objects.create(
            name='Test_Sub_Rubric',
            super_rubric=SuperRubric.objects.get(name='Test_Super_Rubric'))

        Bb.objects.create(
            rubric=SubRubric.objects.get(name='Test_Sub_Rubric'),
            title='Test_item',
            content='Test_content',
            price='10',
            contacts='Test_contacts',
            author=AdvUser.objects.get(username='Test_user_1'),
            is_active=True,
        )

    def test_rubric_field(self):
        new_bb = Bb.objects.get(title='Test_item')
        name = new_bb.rubric.name
        verbose_name = new_bb._meta.get_field('rubric').verbose_name
        self.assertEquals(name, 'Test_Sub_Rubric')
        self.assertEquals(verbose_name, 'Рубрика')

    def test_title_field(self):
        new_bb = Bb.objects.get(title='Test_item')
        max_length = new_bb._meta.get_field('title').max_length
        verbose_name = new_bb._meta.get_field('title').verbose_name
        self.assertEquals(max_length, 100)
        self.assertEquals(verbose_name, 'Название товара')

    def test_content_field(self):
        new_bb = Bb.objects.get(title='Test_item')
        verbose_name = new_bb._meta.get_field('content').verbose_name
        self.assertEquals(verbose_name, 'Описание товара')

    def test_price_field(self):
        new_bb = Bb.objects.get(title='Test_item')
        verbose_name = new_bb._meta.get_field('price').verbose_name
        new_price = new_bb.price
        self.assertEquals(verbose_name, 'Цена товара')
        self.assertEquals(new_price, 10)
        self.assertTrue(str(new_price).isdigit())

    def test_image_field(self):
        new_bb = Bb.objects.get(title='Test_item')
        verbose_name = new_bb._meta.get_field('image').verbose_name
        self.assertEquals(verbose_name, 'Основная иллюстрация к объявлению')

    def test_author_field(self):
        new_bb = Bb.objects.get(title='Test_item')
        new_bb_author = new_bb.author
        verbose_name = new_bb._meta.get_field('author').verbose_name
        self.assertEquals(new_bb_author.username, 'Test_user_1')
        self.assertEquals(verbose_name, 'Пользователь оставивший объявление')

    def test_is_active_field(self):
        new_bb = Bb.objects.get(title='Test_item')
        verbose_name = new_bb._meta.get_field('is_active').verbose_name
        self.assertTrue(new_bb.is_active)
        self.assertEquals(verbose_name, 'Выводить в списке?')

    def test_created_at_field(self):
        new_bb = Bb.objects.get(title='Test_item')
        verbose_name = new_bb._meta.get_field('created_at').verbose_name
        self.assertEquals(str(type(new_bb.created_at)), "<class 'datetime.datetime'>")
        self.assertEquals(verbose_name, 'Дата и время публикации объявления')

    def test_meta(self):
        new_bb = Bb.objects.get(title='Test_item')
        verbose_name = new_bb._meta.verbose_name
        verbose_name_plural = new_bb._meta.verbose_name_plural
        self.assertEquals(new_bb._meta.ordering, ['-created_at'])
        self.assertEquals(verbose_name, 'Объявление')
        self.assertEquals(verbose_name_plural, 'Объявления')

    def test_delete(self):
        new_bb = Bb.objects.get(title='Test_item')
        self.assertIsNotNone(new_bb.pk)
        new_bb.delete()
        self.assertIsNone(new_bb.pk)


class AdditionalImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        AdvUser.objects.create(
            username='Test_user_1',
            first_name='Test_user_fn',
            last_name='Test_user_ln',
            email='test@user.com',
            is_staff=False,
            is_active=True,
            is_activated=True,
        )

        SuperRubric.objects.create(
            name='Test_Super_Rubric',
        )

        SubRubric.objects.create(
            name='Test_Sub_Rubric',
            super_rubric=SuperRubric.objects.get(name='Test_Super_Rubric'))

        Bb.objects.create(
            rubric=SubRubric.objects.get(name='Test_Sub_Rubric'),
            title='Test_item',
            content='Test_content',
            price='10',
            contacts='Test_contacts',
            author=AdvUser.objects.get(username='Test_user_1'),
            is_active=True,
        )

        AdditionalImage.objects.create(
            bb=Bb.objects.get(title='Test_item'),
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )
        AdditionalImage.objects.create(
            bb=Bb.objects.get(title='Test_item'),
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )

    def test_all_fields(self):
        new_images = AdditionalImage.objects.all()
        new_image = AdditionalImage.objects.all()[0]
        bb_verbose_name = new_image._meta.get_field('bb').verbose_name
        image_verbose_name = new_image._meta.get_field('image').verbose_name
        self.assertEquals(new_images.count(), 2)
        self.assertEquals(bb_verbose_name, 'Объявление')
        self.assertEquals(image_verbose_name, 'Изображение')

    def test_meta(self):
        new_image = AdditionalImage.objects.all()[0]
        verbose_name_plural = new_image._meta.verbose_name_plural
        verbose_name = new_image._meta.verbose_name
        self.assertEquals(verbose_name_plural, 'Дополнительные иллюстрации')
        self.assertEquals(verbose_name, 'Дополнительная иллюстрация')


class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        AdvUser.objects.create(
            username='Test_user_1',
            first_name='Test_user_fn',
            last_name='Test_user_ln',
            email='test@user.com',
            is_staff=False,
            is_active=True,
            is_activated=True,
        )

        SuperRubric.objects.create(
            name='Test_Super_Rubric',
        )

        SubRubric.objects.create(
            name='Test_Sub_Rubric',
            super_rubric=SuperRubric.objects.get(name='Test_Super_Rubric'))

        Bb.objects.create(
            rubric=SubRubric.objects.get(name='Test_Sub_Rubric'),
            title='Test_item',
            content='Test_content',
            price='10',
            contacts='Test_contacts',
            author=AdvUser.objects.get(username='Test_user_1'),
            is_active=True,
        )

        Comment.objects.create(
            bb=Bb.objects.get(title='Test_item'),
            author='Test_author',
            content='Test_content',
            is_activate=True,
        )

    def test_bb_field(self):
        new_comment = Comment.objects.get(pk=1)
        verbose_name = new_comment._meta.get_field('bb').verbose_name
        self.assertEquals(verbose_name, 'Объявление')

    def test_author_field(self):
        new_comment = Comment.objects.get(pk=1)
        new_bb_author = new_comment.author
        verbose_name = new_comment._meta.get_field('author').verbose_name
        self.assertEquals(new_bb_author, 'Test_author')
        self.assertEquals(verbose_name, 'Автор')

    def test_content_field(self):
        new_comment = Comment.objects.get(pk=1)
        new_content = new_comment.content
        verbose_name = new_comment._meta.get_field('content').verbose_name
        self.assertEquals(new_content, 'Test_content')
        self.assertEquals(verbose_name, 'Содержание')

    def test_is_activate_field(self):
        new_comment = Comment.objects.get(pk=1)
        verbose_name = new_comment._meta.get_field('is_activate').verbose_name
        self.assertTrue(new_comment.is_activate)
        self.assertEquals(verbose_name, 'Выводить на экран?')

    def test_created_at_field(self):
        new_comment = Comment.objects.get(pk=1)
        verbose_name = new_comment._meta.get_field('created_at').verbose_name
        self.assertEquals(str(type(new_comment.created_at)), "<class 'datetime.datetime'>")
        self.assertEquals(verbose_name, 'Опубликован')

    def test_meta(self):
        new_comment = Comment.objects.get(pk=1)
        verbose_name_plural = new_comment._meta.verbose_name_plural
        verbose_name = new_comment._meta.verbose_name
        ordering = new_comment._meta.ordering
        self.assertEquals(verbose_name_plural, 'Комментарии')
        self.assertEquals(verbose_name, 'Комментарий')
        self.assertEquals(ordering, ['created_at'])
