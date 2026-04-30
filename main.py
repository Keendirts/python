import os
import csv
import json
from collections import Counter

class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        if os.path.exists(self.filename):
            print(f"File found: {self.filename}")
            return True
        print(f"Error: {self.filename} not found.")
        return False

    def create_output_folder(self):
        os.makedirs("output", exist_ok=True)
        print("Output folder ready.")


class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.students = list(csv.DictReader(f))
            print(f"Loaded {len(self.students)} students")
            return True
        except FileNotFoundError:
            print(f"Error: {self.filename} not found.")
            return False

    def preview(self, n=5):
        print("\nFirst 5 rows:")
        print("-" * 50)
        for s in self.students[:n]:
            print(f"{s['student_id']} | {s['age']} | {s['gender']} | {s['country']} | GPA: {s['GPA']}")
        print("-" * 50)


class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        country_counts = Counter()
        for s in self.students:
            try:
                float(s["GPA"])
                float(s["class_attendance_percent"])
                country_counts[s["country"]] += 1
            except ValueError:
                print(f"Warning: invalid data for student {s.get('student_id', '?')}")

        top_3 = country_counts.most_common(3)

        self.result = {
            "analysis": "Country Analysis",
            "total_students": len(self.students),
            "total_countries": len(country_counts),
            "top_3_countries": [{"country": c, "count": n} for c, n in top_3],
            "all_countries": dict(country_counts)
        }
        return self.result

    def lambda_map_filter_demo(self):
        print("\nLambda / Map / Filter Demo")
        print("-" * 30)
        high_gpa = list(filter(lambda s: float(s["GPA"]) > 3.5, self.students))
        gpa_values = list(map(lambda s: float(s["GPA"]), self.students))
        good_attendance = list(filter(lambda s: float(s["class_attendance_percent"]) > 90, self.students))

        print(f"Students with GPA > 3.5: {len(high_gpa)}")
        print(f"GPA values (first 5): {gpa_values[:5]}")
        print(f"Students attendance > 90%: {len(good_attendance)}")
        print("-" * 30)

    def print_results(self):
        print("\n" + "=" * 30)
        print("ANALYSIS RESULT")
        print("=" * 30)
        print(f"Analysis: {self.result['analysis']}")
        print(f"Total students: {self.result['total_students']}")
        print(f"Total countries: {self.result['total_countries']}")
        print("-" * 30)
        print("Top 3 Countries:")
        for i, item in enumerate(self.result["top_3_countries"], 1):
            print(f"{i}. {item['country']}: {item['count']}")
        print("=" * 30)


class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(self.result, f, indent=4, ensure_ascii=False)
        print(f"Result saved to {self.output_path}")


def main():
    filename = "students.csv"
    fm = FileManager(filename)
    if not fm.check_file():
        print("Stopping program.")
        return

    fm.create_output_folder()

    dl = DataLoader(filename)
    if not dl.load():
        print("Stopping program.")
        return

    dl.preview()

    analyser = DataAnalyser(dl.students)
    analyser.analyse()
    analyser.print_results()
    analyser.lambda_map_filter_demo()   # ← исправлено!

    saver = ResultSaver(analyser.result, "output/result.json")
    saver.save_json()


if __name__ == "__main__":
    main()