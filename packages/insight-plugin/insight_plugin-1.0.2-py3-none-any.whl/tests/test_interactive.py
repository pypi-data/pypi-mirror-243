import os
import sys
from unittest import TestCase, mock
sys.path.append(os.path.abspath("../"))
from insight_plugin.features.interactive.controller import InteractiveController
from tests import TEST_RESOURCES

import shutil

sys.path.append("../")


# It is important to run these tests in order for it all to work correctly.
class TestInteractive(TestCase):

    # Declare all different relevant directories for inputs
    target_dir = os.path.abspath(f"{TEST_RESOURCES}/interactive_tests")
    existing_plugin_dir = TEST_RESOURCES + '/test_base64/base64'
    plugin_dir = target_dir + "/base64"
    cur_spec = target_dir + "/plugin.spec.yaml"
    path_to_spec_in_plugin = plugin_dir + "/plugin.spec.yaml"
    path_to_spec_out_plugin = target_dir + "/plugin.spec.yaml"
    json_test_target = existing_plugin_dir + "/../tests/encode.json"

    @mock.patch("builtins.input", side_effect=[1, path_to_spec_out_plugin, target_dir, "Y"])
    def test_interactive_create(self, _mock_input):
        PLUGIN_DIR = TestInteractive.plugin_dir

        # If plugin exists, delete it so that create does not re-create the plugin
        # within the plugin folder
        if os.path.exists(PLUGIN_DIR):
            shutil.rmtree(PLUGIN_DIR)

        # Generate the response
        with self.assertRaises(SystemExit):
            InteractiveController.prompt_menu()
        # Test if the plugin directory now exists because of the create command and clean up
        self.assertTrue(os.path.exists(PLUGIN_DIR), True)
        shutil.rmtree(PLUGIN_DIR)

    # Would be better to run refresh on an existing plugin and check changes but for now this checks refresh runs.
    @mock.patch("builtins.input", side_effect=[2, path_to_spec_in_plugin, plugin_dir, "Y"])
    def test_interactive_refresh(self, _mock_input):
        # create target dir and move our spec to there to run refresh command
        os.mkdir(TestInteractive.plugin_dir)
        shutil.copy(TestInteractive.cur_spec, TestInteractive.plugin_dir)

        with self.assertRaises(SystemExit):
            InteractiveController.prompt_menu()
        # Completed with no errors - we should be able to find 'interactive plugin' with plugin files now
        self.assertTrue(os.path.exists(TestInteractive.plugin_dir + '/bin'), True)
        self.assertTrue(os.path.exists(TestInteractive.plugin_dir + '/setup.py'), True)
        shutil.rmtree(TestInteractive.plugin_dir)  # tidy up

    # Check interactive run completes with no errors.
    @mock.patch("builtins.input", side_effect=[3, json_test_target, existing_plugin_dir, "N", "N", "N", "N"])
    def test_interactive_run(self, _mock_input):
        with self.assertRaises(SystemExit) as context:
            InteractiveController.prompt_menu()
        self.assertEqual(SystemExit, type(context.exception))

    # Just check it runs without error by checking if it exits successfully
    @mock.patch("builtins.input", side_effect=[4, existing_plugin_dir])
    def test_interactive_validate(self, _mock_input):
        with self.assertRaises(SystemExit) as context:
            InteractiveController.prompt_menu()
        self.assertEqual(SystemExit, type(context.exception))

    @mock.patch("builtins.input", side_effect=[5, existing_plugin_dir, "y", "y"])
    def test_interactive_export(self, _mock_input):

        FILE_PATH = os.path.join(TestInteractive.existing_plugin_dir, "rapid7_base64_1.1.6.plg")

        # If it exists, delete it first so export can recreate
        if os.path.isfile(FILE_PATH):
            os.remove(FILE_PATH)

        InteractiveController.prompt_menu()

        # No need for assertRaises here because export doesn't seem to trigger
        # SystemExit unlike the other commands.
        self.assertTrue(os.path.isfile(FILE_PATH), True)
        os.remove(FILE_PATH)
