import tempfile
import unittest
from pathlib import Path
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pipeline


class PipelineSecurityTests(unittest.TestCase):
    def setUp(self):
        self.state_tmp = tempfile.TemporaryDirectory()
        self.state_dir = Path(self.state_tmp.name) / "state"
        self.state_patch = patch.object(pipeline, "STATE_DIR", self.state_dir)
        self.state_patch.start()

    def tearDown(self):
        self.state_patch.stop()
        self.state_tmp.cleanup()

    def test_video_id_cannot_escape_state_directory(self):
        for video_id in ("../escape", "a/b", "/tmp/escape", "", "bad id"):
            with self.subTest(video_id=video_id):
                with self.assertRaises(ValueError):
                    pipeline.state_path(video_id)

    def test_safe_video_id_stays_inside_state_directory(self):
        path = pipeline.state_path("2026-08-09-first-video")
        self.assertEqual(path.parent, self.state_dir)

    def test_external_artifact_requires_explicit_opt_in(self):
        pipeline.init_task("test-video")
        with tempfile.NamedTemporaryFile() as artifact:
            with self.assertRaises(ValueError):
                pipeline.set_artifact("test-video", "brief", artifact.name)

    def test_external_artifact_can_be_explicitly_allowed(self):
        pipeline.init_task("test-video")
        with tempfile.NamedTemporaryFile() as artifact:
            artifact.write(b"example")
            artifact.flush()
            pipeline.set_artifact_with_options(
                "test-video",
                "brief",
                artifact.name,
                allow_external=True,
            )
        state = pipeline.load_state("test-video")
        self.assertEqual(state["stages"]["brief"]["status"], "done")

    def test_negative_or_non_finite_cost_is_rejected(self):
        pipeline.init_task("test-video")
        for cost in (-1, float("nan"), float("inf")):
            with self.subTest(cost=cost):
                with self.assertRaises(ValueError):
                    pipeline.set_remote_task("test-video", "assets", "task-1", cost)


class SkillMetadataTests(unittest.TestCase):
    def test_skill_files_have_required_frontmatter(self):
        repo_root = Path(__file__).resolve().parents[3]
        skill_files = sorted(repo_root.rglob("SKILL.md"))
        self.assertGreaterEqual(len(skill_files), 2)
        for skill_file in skill_files:
            with self.subTest(skill_file=skill_file):
                text = skill_file.read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"))
                self.assertIn("\nname:", text)
                self.assertIn("\ndescription:", text)
                self.assertLessEqual(len(text.splitlines()), 500)


if __name__ == "__main__":
    unittest.main()
