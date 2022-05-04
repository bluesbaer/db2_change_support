# db2_change_support

**WHAT**   
Sometimes you have to change an field in an table.   
Then there is the question:   
*Do I use this field in any other table, view, function or procedure?*   

**HOW**
Start the program:   
```
python change.py
```
Then you type in the server, port, databasename and user in the first row.   
In the next row you type in the fieldname you want to change.   
In the third row you may type in an schemaname to limit where the program should search.   
Otherwise it searches through the whole database.   

The program lists:   
- TABLES which contain a field with the same name   
- VIEWS which contain a field with the same name   
- FUNCTIONS using a field with the same name   
- PROCEDURES using a field with the same name   
