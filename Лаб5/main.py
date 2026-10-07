from gradebook import GradeBook
from student import Student

def main():
    book = GradeBook()
    book.register(Student(101, "Amina", "IS-24-1"))
    book.register(Student(102, "Dias", "IS-24-1"))
    book.register(Student(103, "Mira", "IS-24-1"))

    for score in (88, 92, 79):
        book.add_score(101, score)

    for score in (45, 52, 48):
        book.add_score(102, score)

    for student in book.rating():
        avg_str = "-" if student.average is None else f"{student.average:.2f}"
        print(f"{student.name}: {avg_str}; {student.status}")

if __name__ == "__main__":
    main()
