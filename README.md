# Student resource system

# A student resources sharing platform

This platform aims to share notes, ppts, assignments and such among the common faculty and students of institute. The website has been done in Django, with SQLite3 as backup.
Given are various steps for above.

# Requirements
Python, git, and pip.
Code editor preferred if vs code is used.

# Steps for local deployment

1. Clone the above repository using ```git clone https://github.com/shreyasudaya/student-res```

2. Navigate to repository using ```cd student-res/student_resource_sharing```

3. Activate virtual environment as per directions in directory:
        - ```python -m venv venv``` 
        - ```venv/bin/activate``` if the venv shows Scripts instead of bin, replace with Scripts instead. Just make sure you use the path towards activating the venv.
    This will activate the virtual environment. 

4. Install requirements using ```pip install -r requirements.txt``` 

5. Just to make sure migrations are in order:
        - run command ```python manage.py makemigrations```
        - after which run ```python manage.py migrate```

6. Now for admin login you will want to create an admin in terminal. For this you will type in ```python manage.py createsuperuser```. You will be asked to give username, email and password. Do the needful and you will have an admin account.

7. Run in local using command ```python manage.py runserver```

# Features implemented

- File upload
- User authentication(While signing up, it would be preferred to use '.nitk.edu.in' email id)
- Admin authentication(note: works different than user authentication)
- Admin has various privileges such as determining status of files. Through admin one can view all users and delete the users.

# Tentative to do

- add rating review system to models.
- integrate with a NoSQL database such as through Firebase or MongoDB
- Add filter system which allows filtering of notes by Branch and file type.

# Types of Users and accounts to use if you are too lazy to sign up.
- Account 1: Type faculty
        - email: shreekararajendra.211cs152@nitk.edu.in
        - password: 123456
- Account 2: Type normal student user
        - email: shreyasudaya.211cs152@nitk.edu.in
        - password: 123456
- Account 3: Type admin: Use in admin login you can navigate to by clicking admin in top right navbar.
        - email: bofadeesnatsu@gmail.com
        - password: 1234567
