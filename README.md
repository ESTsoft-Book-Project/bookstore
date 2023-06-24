# bookstore

## How to deploy?

1. `python -m venv venv` ==> create virtual environment which is called `env`
2. `source venv/bin/activate` on UNIX-based OS, `.\venv\Scripts\Activate.ps1` on Windows OS ==> activate virtual environment!
3. `git clone git@github.com:ESTsoft-Book-Project/bookstore.git .` ==> don't forget the last `.` in the command!
4. `cd blogtutorial`
5. `pip install -r requirements.txt` ==> THE MOST IMPORTANT THING!
6. `./manage.py migrate` ==> migration is telling django to change state of DB.
7. `./manage.py runserver` ==> as this command says, you'll be prompted some URL that can lead you to a blog! 🎈🎈🎉
