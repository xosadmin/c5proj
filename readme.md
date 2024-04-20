# CITS5505 Assignment 2 Group Project  
  
## Note: This is a private repository. Do not share it with others.  
  
### Due date: 5 PM on Sunday, May 19th, 2024 (GMT+8)  

#### Live Test user  
User Name: test@test.com  
Password: 123  
  
#### Description
The Assignment 2 is asked to build a request forum application, which allows users to create accounts, post their own requests and answer other people's requests.  
  
#### Program Structure  
![Program Structure](structure.png)  
This program is based on the following structure:  
- The `app.py` is main application and used for template rendering, content structuring and some data processing  
- This program contains `get.py` and `login_process.py`. Some functions (e.g. Requrements, Shop, Community and shop) are rely on the functions in `get.py` to get or set the data from the database.  
- The `login_process.py` is for user login/registration process. When user try to login/register, this file will used for read and verify user input data or save valid data to the database. Also, when user login successful, this file will help to set session. Besides, when user triggered `Logout`, this fill will help to destroy sessions.  
- The `sqlmodel.py` is used for communication between program and SQLite database. It contains data models, and to help to get/set data from/to database  
- This program uses SQLite database (`database/main.db`) to store data  
  
Note: the main database (`database/main.db`) contains some test data. You could use them for program testing.  
  
#### How to get started  
- Clone this project  
- Install dependencies by `pip install -r requirements.txt` (Use `pip install -r requirements.txt --break-system-packages` if you are working on Linux)  
- Use the command `flask run`(Use `flask run --host=0.0.0.0` if debug on productive server) to start the web server  
  
#### Group members  
| Name  | Student ID | Github ID |
| ------------- | ------------- | ------------- |
| Hanxun Xu  | 23885505  | [https://github.com/xosadmin](xosadmin) |
| Jikang Song  | 23877962  | [https://github.com/jikang1116](jikang1116) |
| Phyo Phyo Wut Yee Khine | 23650578 | [https://github.com/Phyo09](Phyo09) |
| Chunhui Chu | 24074951 | [https://github.com/TonyChyu](TonyChyu) |
------  
For full assignment description, see [https://github.com/xosadmin/cits5505Proj/description.md](description.md)  

