import os
import unittest
import re

class DocumentationUpgradeTest(unittest.TestCase):
    TARGET_STACK_VERSION = "latest stable"  # Replace with the exact target version if known

    # Helper to read file contents
    def read_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def test_readme_reflects_modernized_stack(self):
        """Verify README.md reflects the new, modernized stack version."""
        content = self.read_file("README.md")
        # Assert the target stack or platform/version is present
        self.assertRegex(
            content.lower(),
            re.escape(self.TARGET_STACK_VERSION.lower()),
            msg=f"README.md must mention the target stack version: {self.TARGET_STACK_VERSION}"
        )
        # Must not mention 'legacy', 'deprecated', or obvious old stack names
        self.assertNotRegex(
            content,
            r"\blegacy\b|\bdeprecated\b|\b(old|outdated) stack\b",
            msg="README.md should not reference legacy or outdated stack information"
        )

    def test_deployment_guide_uses_new_workflows(self):
        """Check DEPLOYMENT.md has updated workflows and no references to unsupported steps."""
        content = self.read_file("DEPLOYMENT.md")
        # Must mention new deployment flow or stack
        self.assertIn(
            self.TARGET_STACK_VERSION.lower(),
            content.lower(),
            "DEPLOYMENT.md does not mention the modernized stack/deployment version."
        )
        # Must not reference deprecated steps
        self.assertNotRegex(
            content,
            r"\blegacy deployment\b|\bdeprecated tool\b|\bold way\b|\bunsupported\b",
            "DEPLOYMENT.md should not reference deprecated or unsupported deployment steps."
        )

    def test_changelog_mentions_documentation_upgrade(self):
        """Ensure CHANGELOG.md lists the documentation upgrade and version."""
        content = self.read_file("CHANGELOG.md")
        # Should mention something about "modernized stack" or documentation update in latest section
        top_section = content.partition('\n## ')[2][:500]  # Only check in latest release section
        self.assertRegex(
            top_section,
            r"moderniz(ed|ation) stack|documentation( update| refresh)|deployment guide",
            "CHANGELOG.md should mention documentation upgrade in the latest release."
        )

    def test_onboarding_is_consistent_with_new_deployment(self):
        """doc/ONBOARDING.md should not reference old deployment instructions."""
        path = os.path.join("docs", "ONBOARDING.md")
        content = self.read_file(path)
        # Verify new instructions present—must reference new stack/version
        self.assertIn(
            self.TARGET_STACK_VERSION.lower(),
            content.lower(),
            "ONBOARDING.md does not mention the modernized stack/deployment."
        )
        # Deprecated onboarding steps are not mentioned
        self.assertNotRegex(
            content,
            r"old onboarding|legacy process|deprecated",
            "ONBOARDING.md must not mention old/legacy onboarding steps."
        )

    def test_runbook_operational_steps_are_current(self):
        """doc/RUNBOOK.md reflects new operations and troubleshooting guidance."""
        path = os.path.join("docs", "RUNBOOK.md")
        content = self.read_file(path)
        # Must mention new stack version for operation/troubleshooting
        self.assertIn(
            self.TARGET_STACK_VERSION.lower(),
            content.lower(),
            "RUNBOOK.md does not reference the modernized stack runtime/version."
        )
        # No deprecated troubleshooting or operations
        self.assertNotRegex(
            content,
            r"\bdeprecated troubleshooting\b|\bold troubleshooting\b|\blegacy ops\b",
            "RUNBOOK.md must not reference deprecated operational/troubleshooting instructions."
        )

    def test_links_file_references_updated_docs(self):
        """docs/links.md links to the updated documentation."""
        path = os.path.join("docs", "links.md")
        content = self.read_file(path)
        # Should include links to updated files
        self.assertRegex(
            content,
            r"(README\.md|DEPLOYMENT\.md|ONBOARDING\.md|RUNBOOK\.md)",
            "links.md should reference the modernized documentation files."
        )

    def test_no_deprecated_config_keys_documented(self):
        """Outdated configuration keys are no longer documented anywhere."""
        deprecated_keys = [
            # Add deprecated keys as identified in migration!
            "OLD_CONFIG_", "LEGACY_", "OUTDATED_"
        ]
        files = [
            "README.md",
            "DEPLOYMENT.md",
            os.path.join("docs", "ONBOARDING.md"),
            os.path.join("docs", "RUNBOOK.md"),
        ]
        for filename in files:
            content = self.read_file(filename)
            for key in deprecated_keys:
                self.assertNotIn(
                    key, content,
                    f"{filename} should not mention deprecated configuration key: {key}"
                )

    def test_new_configuration_keys_present(self):
        """New configuration keys from the modernized stack are documented without errors."""
        # Example new keys: replace with actual keys after migration
        new_keys = [
            # Add new config keys as identified in new stack!
            "MODERN_CONFIG_", "NEW_STACK_", "LATEST_FEATURE_"
        ]
        for filename in [
            "README.md",
            "DEPLOYMENT.md",
            os.path.join("docs", "ONBOARDING.md"),
            os.path.join("docs", "RUNBOOK.md"),
        ]:
            content = self.read_file(filename)
            for key in new_keys:
                # The key should be mentioned
                self.assertIn(
                    key, content,
                    f"{filename} does not document new configuration key: {key}"
                )

    # Optionally: Add a summary for test completeness
    def test_all_documentation_files_exist(self):
        files = [
            "README.md",
            "DEPLOYMENT.md",
            "CHANGELOG.md",
            os.path.join("docs", "ONBOARDING.md"),
            os.path.join("docs", "RUNBOOK.md"),
            os.path.join("docs", "links.md"),
        ]
        for filepath in files:
            self.assertTrue(
                os.path.exists(filepath), f"Documentation file missing: {filepath}"
            )

if __name__ == "__main__":
    unittest.main()