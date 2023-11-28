import tempfile, shutil, os
import sys
from unittest import TestCase

import ruamel.yaml

sys.path.append("../")

from insight_plugin.features.common.plugin_spec_util import PluginSpecUtil
from insight_plugin.features.version.controller import VersionController
from tests import TEST_RESOURCES

new_yaml = ruamel.yaml.YAML()


class TestSemver(TestCase):
    # Root directory for the test plugin
    target_dir = os.path.abspath(f"{TEST_RESOURCES}/semver_tests/base64")
    version_num = "1.1.7"
    spec_dict = PluginSpecUtil.get_spec_file(target_dir)

    def test_semver_function(self):
        target_version = "1.1.8"
        version_feature = VersionController.new_from_cli(
            target_dir=self.target_dir, version_num=target_version
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            # take a copy of the files before updating
            SemverUtil.copy_files_cur_dir_target_dir(self.target_dir, temp_dir)

            # carry out semver action
            response = version_feature.semver()
            self.assertEqual(None, response)
            spec = PluginSpecUtil.get_spec_file(self.target_dir)
            self.assertEqual(spec["version"], target_version)

            # move back original files
            SemverUtil.copy_files_cur_dir_target_dir(temp_dir, self.target_dir)

    def test_spec_not_found(self):
        version_feature = VersionController.new_from_cli(
            target_dir=f"{TEST_RESOURCES}/run_tests/run_test_base64"
        )
        with self.assertRaises(Exception) as context:
            version_feature.semver()
        self.assertTrue("No such file or directory" in context.exception.strerror)
        self.assertTrue("plugin.spec.yaml" in str(context.exception.filename))

    def test_error_handling_for_lesser_version(self):
        version_feature = VersionController.new_from_cli(
            target_dir=f"{TEST_RESOURCES}/semver_tests/base64", version_num="1.1.5"
        )
        with self.assertRaises(Exception) as context:
            version_feature.semver()
        self.assertTrue(
            "New version must not be less than current version."
            in str(context.exception)
        )

    def test_error_handling_for_equal_version(self):
        version_feature = VersionController.new_from_cli(
            target_dir=f"{TEST_RESOURCES}/semver_tests/base64", version_num="1.1.6"
        )
        with self.assertRaises(Exception) as context:
            version_feature.semver()
            self.assertTrue(
                "New version must not match current version." in str(context.exception)
            )


class SemverUtil:
    @staticmethod
    def copy_files_cur_dir_target_dir(cur_path, temp_dir):
        os.makedirs(f"{temp_dir}/bin", exist_ok=True)  # special case for bin as it needs the directory created first
        files = ['/bin/icon_base64', '/.CHECKSUM', '/help.md', '/plugin.spec.yaml', '/setup.py']
        for file in files:
            shutil.copy2(f"{cur_path}{file}", f"{temp_dir}{file}")
