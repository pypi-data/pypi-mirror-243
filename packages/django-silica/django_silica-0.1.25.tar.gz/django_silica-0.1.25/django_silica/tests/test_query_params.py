import time

from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

from django_silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest, SilicaBrowserTestCase

from selenium.webdriver.common.by import By


from django_silica.SilicaComponent import SilicaComponent


class QueryParamsTestComponent(SilicaComponent):
    property_1 = "foo"

    query_params = ["property_1"]

    def inline_template(self):
        return """
            <div>
                {{ property_1 }}
                <button silica:click.prevent="property_1 = 'foo'" id="set_to_default">Set</button>
            </div>
        """


class QueryParamTests(SilicaTestCase):
    def test_query_params_can_be_set(self):
        (
            SilicaTest(component=QueryParamsTestComponent)
            .assertSet("property_1", "foo")
            .assertSee("foo")
        )

        request = RequestFactory().get("/?property_1=bar")
        request.user = AnonymousUser()

        (
            SilicaTest(component=QueryParamsTestComponent, request=request)
            .assertSet("property_1", "bar")
            .assertSee("bar")
        )



class QueryParamBrowserTests(SilicaBrowserTestCase):
    def test_query_params_are_removed_for_default_values(self):
        self.selenium.get(self.live_server_url + "/silica/tests/query-params?property_1=bar")

        property_1 = self.get_query_param("property_1")

        self.assertTrue(property_1 == "bar")

        self.selenium.find_element(By.ID, 'set_to_default').click()
        time.sleep(0.2)

        property_1 = self.get_query_param("property_1")

        self.assertTrue(property_1 == None)

        # # print the returned source
        # print(self.selenium.page_source)

        # # print the js console
        # print(self.selenium.get_log('browser'))



