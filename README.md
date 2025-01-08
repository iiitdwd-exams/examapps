# `examapps`

`examapps` is intended to be a collection of streamlet apps bound by a navigation page. Each app is meant to implement a simple but independent solution specific to the tasks of the Exam Cell at IIIT Dharwad. At present, there are two apps:

1. **Supplementray Exams Stats** prepares stats of students eligible to appear for Supplementary Exams and prepares a set of protected Microsoft Excel files which serve as registration forms for students.
2. **Remove PDF password** decrypts a password protected file using the known password and saves a decrypted form of the file.

In time, more apps are expected to be added.

## Supplementary Exam Stats
### Input File
The input file can be either a `.xlsx` or a `.csv` file. It **must** contain columns withese exact names, which will be renamed as indicated.

**Required column names:* "Roll No.", "Name", "Acad Period", "Code", "Course", "Credits", "Grade", "Degree". Note the period (`.`) at the end of "Roll No.". Columns can be in any order.

**New names for these columns in the output file:" "roll_no", "name", "acad_period", "code", "course", "credits", "grade", "degree", respectively.

### Output Files
Two output files are generated:
1. <input_filename>_Consolidated_Courselist.xlsx - it contains the list of all courses with one or more students with an "F" grade, unique for each *Academic Period*.
2. <input_filename>_Consolidated.zip - a compressed archive of one or more .xlsx file, one for each student. Each file contains the list of courses with an "F" grade and the credits. Cells of the .xlsx file are protected, except the "register" column where the student can enter a "1" to indicate an intention to register for that course for the Supplementary Exam, and a "0" to indicate otherwise.
