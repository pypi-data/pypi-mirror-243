import os
from pathlib import Path
from django_silica.utils import pascal_to_snake
from django_silica.SilicaComponent import SilicaComponent
from django_silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest
from django.test import TestCase, RequestFactory, Client, override_settings
from django.core.management import call_command
from django.conf import settings
import importlib.util


def import_from_path(path: Path, object_name: str):
    # Ensure the path is absolute
    if not path.is_absolute():
        path = path.resolve()

    # Get the module name and import path
    module_name = path.stem
    spec = importlib.util.spec_from_file_location(module_name, path)

    # Load the module from the spec
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Return the desired object from the module
    return getattr(module, object_name)

class ComponentTagTestCase(SilicaTestCase):
    # setup create files of self.files list
    def setUp(self):
        self.files = []

    # teardown delete files of self.files list
    def tearDown(self):
        for file in self.files:
            if file.exists():
                file.unlink()


    def test_short_tag_can_be_called(self):
        client = Client()
        response = client.get("/silica/tests/component-tag-test")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I'm component called with short name!")


    def test_components_in_subfolders_can_be_called(self):
        client = Client()
        response = client.get("/silica/tests/component-subfolder-test")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I'm component in subfolder!")

    def test_template_and_component_name_are_snake_case(self):
        call_command('silica_create', "TestUniqueSideBar")

        main_app_dir = Path(settings.BASE_DIR) / "example_project"

        # component
        pascal_component_path = main_app_dir / 'silica' / f"TestUniqueSideBar.py"
        self.files.append(pascal_component_path)

        snake_component_path = main_app_dir / 'silica' / f"test_unique_side_bar.py"
        self.files.append(snake_component_path)

        # template
        pascal_template_path = main_app_dir / 'templates' / 'silica' / f"TestUniqueSideBar.html"
        self.files.append(pascal_template_path)
        snake_template_path = main_app_dir / 'templates' / 'silica' / f"test_unique_side_bar.html"
        self.files.append(snake_template_path)

        # we want pascal components and snake templates
        self.assertTrue(pascal_component_path.exists(), f"{pascal_component_path} does not exist.")
        self.assertTrue(snake_template_path.exists(), f"{snake_template_path} does not exist.")
        

    def test_silica_create_with_nested_subfolders(self):
        call_command('silica_create', "folder1.folder2.folder3.NewComponent")

        main_app_dir = Path(settings.BASE_DIR) / "example_project"

        # Component in nested subfolders
        component_path = main_app_dir / 'silica' / 'folder1' / 'folder2' / 'folder3' / "NewComponent.py"
        self.files.append(component_path)

        # Template in nested subfolders
        template_path = main_app_dir / 'templates' / 'silica' / 'folder1' / 'folder2' / 'folder3' / "new_component.html"
        self.files.append(template_path)

        # Incorrectly created component and template paths
        incorrect_component_path = main_app_dir / 'silica' / 'folder1.folder2.folder3' / 'NewComponent.py'
        self.files.append(incorrect_component_path)
        incorrect_template_path = main_app_dir / 'templates' / 'silica' / 'folder1.folder2.folder3' / 'new_component.html'
        self.files.append(incorrect_template_path)


        self.assertTrue(component_path.exists(), f"{component_path} does not exist.")
        self.assertTrue(template_path.exists(), f"{template_path} does not exist.")



    def test_silica_template_name_in_component_definition(self):
        call_command('silica_create', "folder1.folder2.folder3.NewComponent")

        main_app_dir = Path(settings.BASE_DIR) / "example_project"

        # Component in nested subfolders
        component_path = main_app_dir / 'silica' / 'folder1' / 'folder2' / 'folder3' / "NewComponent.py"
        self.files.append(component_path)

        # Template in nested subfolders
        template_path = main_app_dir / 'templates' / 'silica' / 'folder1' / 'folder2' / 'folder3' / "new_component.html"
        self.files.append(template_path)



        self.assertTrue(component_path.exists(), f"{component_path} does not exist.")
        self.assertTrue(template_path.exists(), f"{template_path} does not exist.")

        # import the component
        Component = import_from_path(component_path, "NewComponent")
        self.assertEqual(Component.template_name, "silica/folder1/folder2/folder3/new_component.html")


    def test_command_allows_kebab_case(self):
        call_command('silica_create', "some.Sub-folder.some-component")
 
        main_app_dir = Path(settings.BASE_DIR) / "example_project"

        # component
        wrong_component_path = main_app_dir / 'silica' / f"some/Sub-folder/some-component.py"
        expected_component_path = main_app_dir / 'silica' / f"some/sub-folder/SomeComponent.py"
        self.files.append(expected_component_path)
        self.files.append(wrong_component_path)

        # template
        wrong_template_path = main_app_dir / 'templates' / 'silica' / f"some/Sub-folder/some-component.html"
        expected_template_path = main_app_dir / 'templates' / 'silica' / f"some/sub-folder/some_component.html"
        self.files.append(expected_template_path)
        self.files.append(wrong_template_path)

        self.assertTrue(expected_component_path.exists(), f"{expected_component_path} does not exist.")
        self.assertTrue(expected_template_path.exists(), f"{expected_template_path} does not exist.")
        

    def test_command_allows_pascal_case(self):
        call_command('silica_create', "some.Sub-folder.SomeComponent")
 
        main_app_dir = Path(settings.BASE_DIR) / "example_project"

        # component
        wrong_component_path = main_app_dir / 'silica' / f"some/Sub-folder/some-component.py"
        expected_component_path = main_app_dir / 'silica' / f"some/sub-folder/SomeComponent.py"
        self.files.append(expected_component_path)
        self.files.append(wrong_component_path)


        # template
        wrong_template_path = main_app_dir / 'templates' / 'silica' / f"some/Sub-folder/some-component.html"
        expected_template_path = main_app_dir / 'templates' / 'silica' / f"some/sub-folder/some_component.html"
        self.files.append(expected_template_path)
        self.files.append(wrong_template_path)

        self.assertTrue(expected_component_path.exists(), f"{expected_component_path} does not exist.")
        self.assertTrue(expected_template_path.exists(), f"{expected_template_path} does not exist.")


    def test_single_word_component_is_capitalized(self):
        call_command('silica_create', "some.folder.component")
 
        main_app_dir = Path(settings.BASE_DIR) / "example_project"

        # component
        wrong_component_path = main_app_dir / 'silica' / f"some/folder/component.py"
        expected_component_path = main_app_dir / 'silica' / f"some/folder/Component.py"
        self.files.append(expected_component_path)
        self.files.append(wrong_component_path)

        # template
        expected_template_path = main_app_dir / 'templates' / 'silica' / f"some/folder/component.html"
        self.files.append(expected_template_path)
        

        self.assertTrue(expected_component_path.exists(), f"{expected_component_path} does not exist.")
        self.assertTrue(expected_template_path.exists(), f"{expected_template_path} does not exist.")