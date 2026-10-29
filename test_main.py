import json
import tempfile
import unittest
from pathlib import Path

from main import StudentStore


class StudentStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_path = Path(self.temp_dir.name) / "students.json"
        self.store = StudentStore(self.data_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_reload_student(self):
        self.store.add("S01", "  Ada Lovelace  ", 20, "Computer Science")

        reloaded = StudentStore(self.data_path)
        self.assertEqual(
            reloaded.students,
            [
                {
                    "id": "S01",
                    "name": "Ada Lovelace",
                    "age": 20,
                    "course": "Computer Science",
                }
            ],
        )

    def test_duplicate_id_is_rejected(self):
        self.store.add("S01", "Ada", 20, "Computing")

        with self.assertRaisesRegex(ValueError, "already exists"):
            self.store.add("S01", "Grace", 21, "Mathematics")

    def test_search_update_and_delete(self):
        self.store.add("S01", "Ada Lovelace", 20, "Computing")
        self.assertEqual([student["id"] for student in self.store.find("ada")], ["S01"])

        self.store.update("S01", "Ada Byron", 21, "Mathematics")
        self.assertEqual(self.store.find("S01")[0]["course"], "Mathematics")

        self.store.delete("S01")
        self.assertEqual(self.store.students, [])

    def test_invalid_student_file_is_rejected(self):
        self.data_path.write_text(json.dumps({"id": "S01"}), encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "Invalid student data"):
            StudentStore(self.data_path)


if __name__ == "__main__":
    unittest.main()
