import os
import re
import unittest

TARGET_DOC_VERSION = "latest stable"
STACK_COMPONENTS = [
    "modernized stack",
    "modernized deployment flow"
]

DEPRECATED_TERMS = [
    "legacy stack component",
    "legacy deployment process",
    "legacy config key",
    "deprecated component"
]

REPLACED_API_TERMS = [
    # e.g. "OldApiReference", (add more if specific deprecated APIs are known)
]

NEW_CONFIG_KEYS = [
    # As per the summary, look for known modernized config keys.
    # Since none specifically listed, test for example/placeholder key.
    "modernized_config_key"
]

DOCUMENTATION_PATHS = [
    "docs/README.md",
    "docs/deployment.md",
    "docs/operations.md",
    "CHANGELOG.md",
    "docs/runbook.md"
]


class TestDocumentationUpgrade(unittest.TestCase):
    def test_stack_overview_mentions_modernized_components(self):
        readme_path = "docs/README.md"
        self.assertTrue(os.path.exists(readme_path), f"{readme_path} must exist.")
        with open(readme_path, encoding='utf-8') as f:
            content = f.read().lower()
            found = any(component in content for component in STACK_COMPONENTS)
            self.assertTrue(found, "Modernized stack components must be referenced in README.md.")

    def test_deployment_doc_is_updated(self):
        deployment_path = "docs/deployment.md"
        self.assertTrue(os.path.exists(deployment_path), f"{deployment_path} must exist.")
        with open(deployment_path, encoding='utf-8') as f:
            content = f.read().lower()
            self.assertIn("modernized deployment", content, "Deployment documentation should reference modernized deployment process.")
            self.assertNotIn("legacy deployment", content, "Deployment documentation should not reference legacy deployment process.")

    def test_no_deprecated_terms(self):
        failed_files = []
        for doc_path in DOCUMENTATION_PATHS:
            if not os.path.exists(doc_path):
                continue
            with open(doc_path, encoding='utf-8') as f:
                content = f.read().lower()
                for term in DEPRECATED_TERMS:
                    if term in content:
                        failed_files.append((doc_path, term))
        self.assertFalse(failed_files,
                         f"Deprecated terms present: {failed_files}")

    def test_no_deprecated_apis(self):
        failed_files = []
        if REPLACED_API_TERMS:
            for doc_path in DOCUMENTATION_PATHS:
                if not os.path.exists(doc_path):
                    continue
                with open(doc_path, encoding='utf-8') as f:
                    content = f.read()
                    for term in REPLACED_API_TERMS:
                        if term in content:
                            failed_files.append((doc_path, term))
            self.assertFalse(failed_files, f"Deprecated API terms found: {failed_files}")
        else:
            # If no APIs listed, test passes.
            self.assertTrue(True)

    def test_new_config_keys_documented(self):
        deployment_path = "docs/deployment.md"
        config_found = False
        if os.path.exists(deployment_path):
            with open(deployment_path, encoding='utf-8') as f:
                content = f.read()
                for key in NEW_CONFIG_KEYS:
                    if key in content:
                        config_found = True
                        break
        self.assertTrue(config_found, "Modernized configuration keys must be present in deployment documentation.")

    def test_operations_troubleshooting_section_present(self):
        ops_path = "docs/operations.md"
        self.assertTrue(os.path.exists(ops_path), f"{ops_path} must exist.")
        with open(ops_path, encoding='utf-8') as f:
            content = f.read().lower()
            self.assertIn("troubleshooting", content, "Troubleshooting section missing from operations documentation.")

    def test_changelog_mentions_modernization(self):
        changelog_path = "CHANGELOG.md"
        self.assertTrue(os.path.exists(changelog_path), "CHANGELOG.md must exist.")
        with open(changelog_path, encoding='utf-8') as f:
            content = f.read().lower()
            self.assertIn("modernization", content, "Changelog must mention the modernized stack upgrade.")

    def test_runbook_is_modernized(self):
        runbook_path = "docs/runbook.md"
        self.assertTrue(os.path.exists(runbook_path), "Runbook must exist.")
        with open(runbook_path, encoding='utf-8') as f:
            content = f.read().lower()
            self.assertIn("modernized deployment", content, "Runbook should reference modernized deployment steps.")

    def test_documentation_is_at_target_version(self):
        readme_path = "docs/README.md"
        self.assertTrue(os.path.exists(readme_path), f"{readme_path} must exist.")
        with open(readme_path, encoding='utf-8') as f:
            content = f.read().lower()
            # Require the README to clearly mention the doc version tied to latest stack/runtimes
            version_pattern = re.compile(r"(documentation version|docs version|version:)\s*(latest stable|\d+\.\d+)")
            match = version_pattern.search(content)
            self.assertIsNotNone(match, "README.md must mention documentation version.")
            self.assertIn(TARGET_DOC_VERSION, match.group(), f"Documentation version must be '{TARGET_DOC_VERSION}', found: '{match.group()}'.")

if __name__ == "__main__":
    unittest.main()