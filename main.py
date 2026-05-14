import os
import csv
import json


class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        return os.path.exists(self.filename)

    def create_output_folder(self):
        if not os.path.exists("output"):
            os.makedirs("output")


class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.students = list(csv.DictReader(f))
            return self.students
        except FileNotFoundError:
            print("File not found")
            return []

    def preview(self, n=5):
        for s in self.students[:n]:
            print(s["student_id"], s["country"], s["GPA"])


class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        print("Not implemented — use a child class")

    def print_results(self):
        for key, value in self.result.items():
            print(f"{key}: {value}")

    def __str__(self):
        return f"DataAnalyser: base class, {len(self.students)} students"


class CountryAnalyser(DataAnalyser):
    def __init__(self, students):
        super().__init__(students)

    def analyse(self):
        counts = {}

        for s in self.students:
            country = s["country"]
            counts[country] = counts.get(country, 0) + 1

        top_3 = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:3]

        self.result = {
            "analysis": "Country Analysis",
            "total_students": len(self.students),
            "total_countries": len(counts),
            "top_3_countries": top_3
        }

    def print_results(self):
        print("=" * 30)
        print("COUNTRY ANALYSIS REPORT")
        print("=" * 30)
        super().print_results()
        print("=" * 30)

    def __str__(self):
        return f"CountryAnalyser: Country Analysis, {len(self.students)} students"


class GpaAnalyser(DataAnalyser):
    def __init__(self, students):
        super().__init__(students)

    def analyse(self):
        gpas = [float(s["GPA"]) for s in self.students]

        self.result = {
            "analysis": "GPA Analysis",
            "average_gpa": round(sum(gpas) / len(gpas), 2),
            "max_gpa": max(gpas),
            "min_gpa": min(gpas)
        }

    def print_results(self):
        print("=" * 30)
        print("GPA ANALYSIS REPORT")
        print("=" * 30)
        super().print_results()
        print("=" * 30)

    def __str__(self):
        return f"GpaAnalyser: GPA Statistics, {len(self.students)} students"


class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(self.result, f, indent=4, ensure_ascii=False)
        print(f"Result saved to {self.output_path}")


class Report:
    def __init__(self, analyser, saver):
        self.analyser = analyser
        self.saver = saver

    def generate(self):
        print("Generating report...")
        self.analyser.analyse()
        self.analyser.print_results()
        self.saver.result = self.analyser.result
        self.saver.save_json()
        print("Report complete.")


def main():
    fm = FileManager("students.csv")

    if not fm.check_file():
        print("students.csv not found")
        return

    fm.create_output_folder()

    dl = DataLoader("students.csv")
    students = dl.load()

    if not students:
        return

    dl.preview()

    analysers = [
        CountryAnalyser(students),
        GpaAnalyser(students[:10])
    ]

    print("Running all analysers:")

    for analyser in analysers:
        print(analyser)
        analyser.analyse()
        analyser.print_results()

    saver = ResultSaver({}, "output/result.json")
    report = Report(analysers[0], saver)
    report.generate()


if __name__ == "__main__":
    main()