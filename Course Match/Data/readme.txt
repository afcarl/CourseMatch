1. Extract_courses_names.py will extract the courses' names and pickle them to Course_data.p
2. In order to update the class list, run update_class_list.py outside this folder with argument "new".
3. In step 2, a new instance of each class would be created, so it is necessary to delete old db file.
4. If you want to update the database without deleting it (having some addition entry but keep the structure of the db) then add argument " add" when running the script. This automatically add relation between teachers and the classes they are teaching.
5. To modify the db structure, run the script database.py with argument "db migrate" then "db upgrade"
