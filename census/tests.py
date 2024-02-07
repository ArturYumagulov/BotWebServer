import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.staticfiles import finders

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains

from census import models


class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.b2b_url = f"{cls.live_server_url}/census/f/1?city=Казань&street=Калинина&house=15к1&guid=00000000001&name=Под%20мостом&depart=b2b"
        cls.valid_class = 'is-valid'
        cls.invalid_class = 'is-invalid'
        cls.has_inn = '1313131313'
        cls.has_inn_name = "Ленин Владимир Ильич ИП"
        cls.test_comment = "Тестовый комментарий"
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def select2multi(self, eid, items, typing="Div"):
        elem_1 = self.selenium.find_element(By.CSS_SELECTOR, f'#{eid} > option:nth-child(2)')
        ActionChains(self.selenium).key_up(Keys.CONTROL).click(elem_1).perform()

        for item in items:

            elem = self.selenium.find_element(By.XPATH,
                                              f'//*[@id="{eid}{typing}"]/span[2]/span/span/ul/li[contains(text(), "{item.name}")]')
            elem.click()

        ActionChains(self.selenium).key_up(Keys.CONTROL).click(elem_1).perform()
        ActionChains(self.selenium).key_up(Keys.CONTROL).click(elem_1).perform()

    def test_b2b_not_communicate(self):
        # нет коммуникации
        self.selenium.get(self.b2b_url)
        self.assertEqual(self.selenium.title, 'Сенсус Казань, Калинина, 15к1')
        self.selenium.find_element(By.XPATH, '//*[@id="todo-app"]/form/div[1]/div[2]').click()
        self.selenium.find_element(By.ID, 'formFileMultiple').send_keys(finders.find('images/logo.jpg'))
        self.selenium.find_element(By.ID, 'resultCommentId').send_keys(self.test_comment)
        self.selenium.find_element(By.ID, 'formFileMultiple').submit()
        text = self.selenium.find_element(By.TAG_NAME, 'h1')
        self.assertEqual(text.text, 'Сенсус успешно записан, задача выполнена. Спасибо')

    def test_b2b_not_working(self):
        # адрес не актуален
        self.selenium.get(self.b2b_url)
        self.assertEqual(self.selenium.title, 'Сенсус Казань, Калинина, 15к1')
        self.selenium.find_element(By.ID, 'closeCheckbox').click()
        self.selenium.find_element(By.ID, 'formFileMultiple').send_keys(finders.find('images/logo.jpg'))
        self.selenium.find_element(By.ID, 'resultCommentId').send_keys(self.test_comment)
        self.selenium.find_element(By.ID, 'formFileMultiple').submit()
        text = self.selenium.find_element(By.TAG_NAME, 'h1')
        self.assertEqual(text.text, 'Сенсус успешно записан, задача выполнена. Спасибо')

    def test_org_have_in_1C(self):
        self.selenium.get(self.b2b_url)
        self.assertEqual(self.selenium.title, 'Сенсус Казань, Калинина, 15к1')
        inn = self.selenium.find_element(By.ID, 'innId')
        inn.send_keys(self.has_inn)
        inn.send_keys(Keys.ENTER)
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, '#innSearchUl > li.list-group-item.out').text, "Данный ИНН существует в 1С")
        find_inn = self.selenium.find_element(By.CSS_SELECTOR, '#innSearchUl > li.list-group-item.result-inn')
        self.assertEqual(find_inn.text, self.has_inn_name)
        find_inn.click()
        search_client_input = self.selenium.find_element(By.ID, 'searchClient')
        self.assertEqual(self.valid_class in search_client_input.get_attribute('class').split(' '), True)

        #  Уже работаем с точкой
        work_checkbox = self.selenium.find_element(By.CSS_SELECTOR, '#workCheckbox')

        self.assertEqual(work_checkbox.is_selected(), True)

        #  Нет коммуникации
        not_communicate = self.selenium.find_element(By.ID, 'communicateCheckbox')

        self.assertEqual(not_communicate.get_attribute('disabled'), 'true')

        #  Точка не существует
        closing_checkbox = self.selenium.find_element(By.ID, 'closeCheckbox')

        self.assertEqual(closing_checkbox.get_attribute('disabled'), 'true')

        #  Вывеска
        point_name_input = self.selenium.find_element(By.ID, 'signboardId')
        point_name_input.send_keys(Keys.ENTER)

        self.assertEqual(self.invalid_class in point_name_input.get_attribute('class').split(' '), True)
        self.assertEqual(self.selenium.find_element(By.ID, 'signboardIdFeedback').text, 'Укажите вывеску торговой точки')

        point_name_input.send_keys('Название точки')

        self.assertEqual(self.valid_class in point_name_input.get_attribute('class').split(' '), True)

        #  Фотографии точки
        files = self.selenium.find_element(By.ID, 'formFileMultiple')

        self.assertEqual(self.invalid_class in files.get_attribute('class').split(' '), True)
        self.assertEqual(self.selenium.find_element(By.XPATH, '//*[@id="todo-app"]/form/div[5]/div').text,
                         'Пожалуйста, загрузите фотографии точки')
        files.send_keys(finders.find('images/logo.jpg'))

        self.assertEqual(self.valid_class in files.get_attribute('class').split(' '), True)

        # Категория точки?
        category = self.selenium.find_element(By.ID, 'shopCategoryId')
        category_select = Select(category)
        category_select.select_by_visible_text('Добывающая промышленность')

        self.assertEqual(category_select.first_selected_option.text, 'Добывающая промышленность')
        self.assertEqual(len(category_select.options),
                         models.PointCategory.objects.filter(is_active=True).filter(department__name='b2b').count() + 1)
        self.assertEqual(self.valid_class in category.get_attribute('class').split(' '), True)

        #  Направленность
        vector_id = 'vectorMulti'
        vectors = models.PointVectors.objects.filter(is_active=True).filter(department__name='b2b')
        self.select2multi(vector_id, vectors)
        self.assertEqual('was-validated' in self.selenium.find_element(By.ID, f"{vector_id}Div").get_attribute('class').split(' '), True)

        for vector in vectors:
            if vector.name != "Другое":
                select_input = self.selenium.find_element(By.ID, f'{vector.slug}_load')
                self.assertEqual('was-validated' in select_input.get_attribute('class').split(' '), True)
                vector_items = models.PointVectorsSelectItem.objects.filter(vectors=vector)
                self.select2multi(vector.slug, vector_items, '_load')
            else:
                other_vector = self.selenium.find_element(By.ID, 'otherVectorInputId')
                other_vector.send_keys(Keys.ENTER)
                self.assertEqual(self.invalid_class in other_vector.get_attribute('class').split(' '), True)
                self.assertEqual(self.selenium.find_element(By.ID, 'otherVectorFeedback').text, 'Выберите другие продукты торговой точки')
                other_vector.send_keys(self.test_comment)

        #  Парк техники
        self.selenium.execute_script("window.scrollTo(0,600);")
        time.sleep(1)

        equipment_id = "equipmentId"
        equipments = models.EquipmentList.objects.filter(is_active=True).filter(department__name='b2b')
        self.select2multi(equipment_id, equipments)
        self.assertEqual('was-validated' in self.selenium.find_element(By.ID, f"{equipment_id}Div").get_attribute('class').split(' '), True)

        #  Поставщики
        providers_id = 'providers'
        providers = models.ProviderList.objects.filter(is_active=True).filter(department__name='b2b')
        self.select2multi(providers_id, providers)
        self.assertEqual('was-validated' in self.selenium.find_element(By.ID, f"{providers_id}Div").get_attribute('class').split(' '), True)

        #  Объем
        volume_id = 'volumeId'
        volumes = models.Volume.objects.filter(is_active=True).filter(department__name='b2b')
        self.select2multi(volume_id, volumes)
        self.assertEqual('was-validated' in self.selenium.find_element(By.ID, f"{volume_id}Div").get_attribute('class').split(' '), True)

        for volume in volumes:
            item = self.selenium.find_element(By.ID, f"volume_{volume.pk}")
            item.send_keys(self.test_comment)
            self.assertEqual(self.invalid_class in item.get_attribute('class').split(' '), True)


        time.sleep(60)



