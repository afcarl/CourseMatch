import pickle
def main():
    '''This function process the HTML file (Raw_course_catalog.txt)
    and create a new file (Courses_names.txt) that contains the name of
    the courses.'''
    fopen = open("Raw_course_catalog.txt","r")
    fwrite = open("Courses_data.p","wb")
    course_list = []
    first_entry = True
    for line in fopen:
        if "ddtitle" in line:
            for position in range(len(line) - 2):
                if line[position] == ">" and line[position+1] != "<":
                    start_position = position + 1
            end_position = len(line)
            first_entry = True
            course_name = "-".join(line[start_position:end_position].split("-")
                                [0:len(line[start_position:end_position].split("-"))-3])
            course_id = (line[start_position:end_position].split("-")
                        [len(line[start_position:end_position].split("-"))-2])
        if "Primary" in line:
            if first_entry == True:
                names = ""
                is_True = 0
                for chars in line:
                    if chars == "<" or chars == "(":
                        is_True -= 1
                        continue
                    if chars == ">" or chars == ")":
                        is_True += 1
                        continue
                    if is_True == 0:
                        names += chars
                names = " ".join(names.rstrip().split())
                print(names)
                course_list.append((course_name, course_id, names))
                first_entry = False
    pickle.dump(course_list, fwrite)
    fopen.close()
    fwrite.close()
if __name__ == "__main__":
    main()
