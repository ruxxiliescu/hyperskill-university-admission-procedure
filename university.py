from statistics import mean


class Department:
    def __init__(self, department_name):
        self.department_name = department_name
        self.applicants = []
        self.students = []

    def __str__(self):
        return f'\n{self.department_name}'

    def fill_students(self, n):  # n - number of department priority
        self.applicants = persons[:]  # copy base list of applicants
        self.applicants = self.sorter(self.applicants)  # sorting applicants by their score for this department
        for applicant in self.applicants:
            if len(self.students) < maximum_students and applicant.department_priority[n] == self.department_name:
                applicant.student_of_department = self.department_name
                self.students.append(applicant)
                persons.remove(applicant)  # remove admitted applicant from initial list
        self.students = self.sorter(self.students)  # sort students of department by score

    def sorter(self, sequence):
        return sorted(sequence, key=lambda x: (-x.scores[self.department_name],
                                               x.name, x.surname))


class Person:
    """represents applicants and students, takes list with elements
    [name, surname, phys, chem, math, compsc, dep1, dep2, dep3] as input for __init__"""
    def __init__(self, person):
        name, surname, phys, chem, math, compsc, exam, dep1, dep2, dep3 = person
        self.name = name
        self.surname = surname
        self.scores = {'Biotech': (round(mean([float(phys), float(chem)]), 1)
                                   if round(mean([float(phys), float(chem)])) > float(exam)
                                   else float(exam)),
                       'Chemistry': (float(chem)
                                     if float(chem) > float(exam)
                                     else float(exam)),
                       'Engineering': (round(mean([float(compsc), float(math)]), 1)
                                       if round(mean([float(compsc), float(math)]), 1) > float(exam)
                                       else float(exam)),
                       'Mathematics': (float(math)
                                       if float(math) > float(exam)
                                       else float(exam)),
                       'Physics': (round(mean([float(phys), float(math)]), 1)
                                   if round(mean([float(phys), float(math)]), 1) > float(exam)
                                   else float(exam))
                       }
        self.department_priority = [dep1, dep2, dep3]
        self.student_of_department = None

    def __str__(self):
        return f'{self.name} {self.surname} {self.scores[self.student_of_department]}'


departments_names = ['Biotech', 'Chemistry', 'Engineering', 'Mathematics', 'Physics']
file_name = 'applicants.txt'
persons_from_file = []

with open(file_name, 'r') as file:
    for line in file:
        persons_from_file.append(line.split())

maximum_students = int(input())
persons = [Person(person) for person in persons_from_file]  # creating list of objects of class Person
departments = [Department(name) for name in departments_names]  # creating list of objects of class Department

for n in range(3):  # n - number of priority
    for department in departments:  # for each priority for each dept take students with highest grade
        department.fill_students(n)

for department in departments:
    with open(department.department_name.lower() + '.txt', 'w') as file:
        print(department)
        for student in department.students:
            file.write(str(student) + '\n')
            print(student)
