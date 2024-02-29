import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.staticfiles import finders

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains

from census import models
from tasks import models as task_models


class B2BSeleniumTests(StaticLiveServerTestCase):
    fixtures = ['data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.exists_census = f"{cls.live_server_url}/census/f/22?city=Казань&street=Калинина&house=15к1&guid=00000000001&name=Под%20мостом&depart=b2b"
        cls.new_census = f"{cls.live_server_url}/census/f/2?city=Казань&street=Калинина&house=15к1&guid=00000000001&name=Под%20мостом&depart=b2b"
        cls.load = f"{cls.live_server_url}/census/load/"
        cls.valid_class = 'is-valid'
        cls.invalid_class = 'is-invalid'
        cls.has_inn = '1313131313'
        cls.has_inn_name = "Ленин Владимир Ильич ИП"
        cls.test_string_comment = "Тестовый комментарий"
        cls.test_digit_comment = "12345667890"
        cls.not_inn = "7723032222"
        cls.not_inn_name = 'ЖСК "НАЛЬЧИК"'

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

    def float_valid(self, objects, string=True):
        if string:
            objects.send_keys(self.test_digit_comment)
            self.assertEqual(self.invalid_class in objects.get_attribute('class').split(' '), True)
            objects.clear()
            objects.send_keys(self.test_string_comment)
            self.assertEqual(self.valid_class in objects.get_attribute('class').split(' '), True)
        else:
            objects.send_keys(self.test_string_comment)
            self.assertEqual(self.invalid_class in objects.get_attribute('class').split(' '), True)
            objects.clear()
            objects.send_keys(self.test_digit_comment)
            self.assertEqual(self.valid_class in objects.get_attribute('class').split(' '), True)

    def scroll(self, obj_id):
        self.selenium.execute_script("arguments[0].scrollIntoView(true);",
                                     self.selenium.find_element(By.ID, obj_id))
        time.sleep(3)

    def all_components(self):
        #  Вывеска
        point_name_input = self.selenium.find_element(By.ID, 'signboardId')
        point_name_input.send_keys(Keys.ENTER)

        self.assertEqual(self.invalid_class in point_name_input.get_attribute('class').split(' '), True)
        self.assertEqual(self.selenium.find_element(By.ID, 'signboardIdFeedback').text, 'Укажите вывеску торговой точки')

        point_name_input.send_keys('Название точки')

        self.assertEqual(self.valid_class in point_name_input.get_attribute('class').split(' '), True)

        #  Фотографии точки
        time.sleep(1)
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
                self.selenium.implicitly_wait(10)
                self.select2multi(vector.slug, vector_items, '_load')

            else:
                other_vector = self.selenium.find_element(By.ID, 'otherVectorInputId')
                other_vector.send_keys(Keys.ENTER)
                self.assertEqual(self.invalid_class in other_vector.get_attribute('class').split(' '), True)
                self.assertEqual(self.selenium.find_element(By.ID, 'otherVectorFeedback').text, 'Выберите другие продукты торговой точки')
                other_vector.send_keys(self.test_string_comment)

            ActionChains(self.selenium).key_up(Keys.CONTROL).click(self.selenium.find_element(By.TAG_NAME, 'form')).perform()

        self.scroll('otherVectorInputId')

        #  Парк техники
        equipment_id = "equipmentId"
        equipments = models.EquipmentList.objects.filter(is_active=True).filter(department__name='b2b')
        self.selenium.implicitly_wait(10)

        self.select2multi(equipment_id, equipments)

        self.assertEqual('was-validated' in self.selenium.find_element(By.ID, f"{equipment_id}Div").get_attribute('class').split(' '), True)

        for equipment in equipments:

            if equipment.name != "Другое":
                equipment_input = self.selenium.find_element(By.ID, f"equipment_{equipment.pk}")
                equipment_input.send_keys(self.test_string_comment)
                self.assertEqual(self.invalid_class in equipment_input.get_attribute('class'), True)
                equipment_input.clear()
                equipment_input.send_keys(self.test_digit_comment)
                self.assertEqual(self.valid_class in equipment_input.get_attribute('class'), True)

            else:
                other_equipment_input_name_id = f'equipment_other_name_{equipment.pk}'
                other_equipment_input_name = self.selenium.find_element(By.ID, other_equipment_input_name_id)
                other_equipment_input_name.send_keys(self.test_string_comment)
                self.scroll(other_equipment_input_name_id)
                self.assertEqual(self.valid_class in other_equipment_input_name.get_attribute('class').split(' '), True)

                other_equipment_input_count_id = f'equipment_{equipment.pk}'
                other_equipment_input_count = self.selenium.find_element(By.ID, other_equipment_input_count_id)
                other_equipment_input_count.send_keys(self.test_digit_comment)
                self.assertEqual(self.valid_class in other_equipment_input_count.get_attribute('class').split(' '), True)

                self.scroll(other_equipment_input_count_id)

        #  Поставщики
        providers_id = 'providers'
        providers = models.ProviderList.objects.filter(is_active=True).filter(department__name='b2b')
        self.select2multi(providers_id, providers)
        self.assertEqual('was-validated' in self.selenium.find_element(By.ID, f"{providers_id}Div").get_attribute('class').split(' '), True)

        other_providers = self.selenium.find_element(By.ID, 'otherProvId')
        self.float_valid(other_providers)

        self.scroll(providers_id)

        #  Объем
        volume_id = 'volumeId'
        volumes = models.Volume.objects.filter(is_active=True).filter(department__name='b2b')
        self.select2multi(volume_id, volumes)
        self.assertEqual('was-validated' in self.selenium.find_element(By.ID, f"{volume_id}Div").get_attribute('class').split(' '), True)

        for volume in volumes:

            item = self.selenium.find_element(By.ID, f"volume_{volume.pk}")
            item.send_keys(self.test_string_comment)
            self.assertEqual(self.invalid_class in item.get_attribute('class').split(' '), True)
            item.clear()
            item.send_keys(self.test_digit_comment)
            self.assertEqual(self.valid_class in item.get_attribute('class').split(' '), True)

        other_volume = self.selenium.find_element(By.XPATH, '//input[contains(@id, "other_volume_name")]')

        if other_volume:
            other_volume.send_keys(" ")
            other_volume.send_keys(Keys.BACKSPACE)
            self.assertEqual(self.invalid_class in other_volume.get_attribute('class').split(' '), True)
            other_volume.clear()
            other_volume.send_keys(self.test_string_comment)
            self.assertEqual(self.valid_class in other_volume.get_attribute('class').split(' '), True)

        # Контактное лицо
        firstnameMakerId = self.selenium.find_element(By.ID, 'firstnameMakerId')
        lastnameMakerId = self.selenium.find_element(By.ID, 'lastnameMakerId')
        surnameMakerId = self.selenium.find_element(By.ID, 'surnameMakerId')
        decisionMakerEmailId = self.selenium.find_element(By.ID, 'decisionMakerEmailId')
        decisionMakerFunctionId = self.selenium.find_element(By.ID, 'decisionMakerFunctionId')
        decisionMakerPhoneId = self.selenium.find_element(By.ID, 'decisionMakerPhoneId')
        resultCommentId = self.selenium.find_element(By.ID, 'resultCommentId')

        decisionMakerEmailId.send_keys('test@test.ru')
        self.assertEqual(self.valid_class in decisionMakerEmailId.get_attribute('class').split(' '), True)

        self.float_valid(firstnameMakerId)
        self.float_valid(lastnameMakerId)
        self.float_valid(surnameMakerId)
        self.float_valid(decisionMakerFunctionId)
        self.float_valid(decisionMakerPhoneId, string=False)
        self.float_valid(resultCommentId)

        time.sleep(3)

        tender = Select(self.selenium.find_element(By.ID, 'tenderId'))
        tender.select_by_visible_text("Да")
        self.assertEqual(
            self.valid_class in self.selenium.find_element(By.ID, 'tenderId').get_attribute('class').split(' '), True)
        tender.select_by_visible_text("Нет")
        self.assertEqual(
            self.valid_class in self.selenium.find_element(By.ID, 'tenderId').get_attribute('class').split(' '), True)

        results = task_models.ResultData.objects.filter(group__name="Сенсус")
        result_s = Select(self.selenium.find_element(By.ID, 'controlId'))
        for result in results:
            result_s.select_by_visible_text(result.name)
            self.assertEqual(
                self.valid_class in self.selenium.find_element(
                    By.ID, 'controlId').get_attribute('class').split(' '), True
            )

        self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        button = self.selenium.find_element(By.TAG_NAME, 'button')
        button.click()
        self.selenium.implicitly_wait(10)
        text = self.selenium.find_element(By.TAG_NAME, 'h1')
        self.assertEqual(text.text, 'Сенсус успешно записан, задача выполнена. Спасибо')

    def test_b2b_not_communicate(self):
        # нет коммуникации
        self.selenium.get(self.new_census)
        self.assertEqual(self.selenium.title, 'Сенсус Казань, Калинина, 15к1')
        self.selenium.find_element(By.XPATH, '//*[@id="todo-app"]/form/div[1]/div[2]').click()
        self.selenium.find_element(By.ID, 'formFileMultiple').send_keys(finders.find('images/logo.jpg'))
        self.selenium.find_element(By.ID, 'resultCommentId').send_keys(self.test_string_comment)
        self.selenium.find_element(By.ID, 'formFileMultiple').submit()
        self.selenium.implicitly_wait(10)
        text = self.selenium.find_element(By.TAG_NAME, 'h1')
        self.assertEqual(text.text, 'Сенсус успешно записан, задача выполнена. Спасибо')

    def test_b2b_not_working(self):
        # адрес не актуален
        self.selenium.get(self.new_census)
        self.assertEqual(self.selenium.title, 'Сенсус Казань, Калинина, 15к1')
        self.selenium.find_element(By.ID, 'closeCheckbox').click()
        self.selenium.find_element(By.ID, 'formFileMultiple').send_keys(finders.find('images/logo.jpg'))
        self.selenium.find_element(By.ID, 'resultCommentId').send_keys(self.test_string_comment)
        self.selenium.find_element(By.ID, 'formFileMultiple').submit()
        self.selenium.implicitly_wait(10)
        text = self.selenium.find_element(By.TAG_NAME, 'h1')
        self.assertEqual(text.text, 'Сенсус успешно записан, задача выполнена. Спасибо')

    def test_org_have_in_1C(self):
        self.selenium.get(self.exists_census)
        self.assertEqual(self.selenium.title, 'Сенсус данной точки уже проведен')
        self.selenium.get(self.new_census)
        self.assertEqual(self.selenium.title, 'Сенсус Казань, Калинина, 15к1')
        inn = self.selenium.find_element(By.ID, 'innId')
        inn.send_keys(self.has_inn)
        inn.send_keys(Keys.ENTER)
        time.sleep(1)
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, '#innSearchUl > li.list-group-item.out').text, "Данный ИНН существует в 1С")
        find_inn = self.selenium.find_element(By.CSS_SELECTOR, '#innSearchUl > li.list-group-item.result-inn')
        self.assertEqual(find_inn.text, self.has_inn_name)
        find_inn.click()
        search_client_input = self.selenium.find_element(By.ID, 'searchClient')
        self.assertEqual(search_client_input.get_attribute('value'), 'Ленин Владимир Ильич ИП')
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

        self.all_components()

    def test_org_not_have_in_1c(self):
        self.selenium.get(self.new_census)

        with self.assertRaises(models.CompanyDatabase.DoesNotExist):
            models.CompanyDatabase.objects.get(inn=self.not_inn)

        inn = self.selenium.find_element(By.ID, 'innId')
        inn.send_keys(self.not_inn)
        inn.send_keys(Keys.ENTER)
        time.sleep(3)
        result_list = self.selenium.find_element(By.ID, 'innSearchUl')
        self.assertEqual('block;' in result_list.get_attribute('style').split(': '), True)

        result_item = self.selenium.find_element(By.CLASS_NAME, 'result-inn')
        self.assertEqual(result_item.text == self.not_inn_name, True)
        self.assertEqual(result_item.get_attribute('data-inn') == self.not_inn, True)
        result_item.click()

        org_name = self.selenium.find_element(By.ID, 'organizationsNameId')
        self.assertEqual(org_name.get_attribute('value'), self.not_inn_name)

        self.all_components()
