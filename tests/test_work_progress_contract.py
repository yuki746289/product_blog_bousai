import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "WORK_PROGRESS.md"
GOVERNANCE = ROOT / "docs" / "RULES_GOVERNANCE.md"

ALLOWED_STATUSES = {
    "TODO",
    "IN_PROGRESS",
    "BLOCKED",
    "INTERNAL_CHECK_DONE",
    "USER_CONFIRMATION_PENDING",
    "DONE",
    "REOPENED",
}
REQUIRED_FIELDS = {
    "status",
    "priority",
    "approved_spec",
    "completion_criteria",
    "done",
    "remaining",
    "next_action",
    "blocker",
    "related",
    "updated_at",
    "user_approval",
}


class WorkProgressContractTests(unittest.TestCase):
    def test_progress_ledger_exists_and_is_governance_source(self):
        self.assertTrue(LEDGER.exists())
        governance = GOVERNANCE.read_text(encoding="utf-8")
        self.assertIn("作業進捗の正本", governance)
        self.assertIn("docs/WORK_PROGRESS.md", governance)
        self.assertIn("USER_CONFIRMATION_PENDING", governance)
        self.assertIn("REOPENED", governance)

    def test_every_detailed_task_has_required_fields_and_valid_status(self):
        text = LEDGER.read_text(encoding="utf-8")
        sections = re.findall(
            r"^### ([A-Z]+(?:-[A-Z]+)?-?\d{3})[^\n]*\n(.*?)(?=^### |\Z)",
            text,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertGreaterEqual(len(sections), 1)

        ids = []
        for task_id, body in sections:
            ids.append(task_id)
            fields = {}
            for line in body.splitlines():
                m = re.match(r"^- ([a-z_]+):\s*(.*)$", line.strip())
                if m:
                    fields[m.group(1)] = m.group(2)

            missing = REQUIRED_FIELDS - set(fields)
            self.assertFalse(missing, f"{task_id} missing fields: {sorted(missing)}")

            status = fields["status"].strip("` ")
            self.assertIn(status, ALLOWED_STATUSES, f"{task_id} invalid status: {status}")

            approval = fields["user_approval"].strip("` ")
            self.assertIn(approval, {"YES", "NO"}, f"{task_id} invalid approval: {approval}")

            if status == "DONE":
                self.assertEqual(
                    approval,
                    "YES",
                    f"{task_id} is DONE without user approval",
                )

        self.assertEqual(len(ids), len(set(ids)), "duplicate task IDs")

    def test_timeout_resume_contract_is_recorded(self):
        text = LEDGER.read_text(encoding="utf-8")
        for marker in (
            "承認済み仕様",
            "完了条件",
            "next_action",
            "タイムアウト",
            "ユーザー承認後のみ",
        ):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
