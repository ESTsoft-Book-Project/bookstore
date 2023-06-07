# bookstore

## How to deploy?

1. `python -m venv venv` ==> create virtual environment which is called `env`
2. `source venv/bin/activate` on UNIX-based OS, `.\venv\Scripts\Activate.ps1` on Windows OS ==> activate virtual environment!
3. `git clone git@github.com:ESTsoft-Book-Project/bookstore.git .` ==> don't forget the last `.` in the command!
4. `cd blogtutorial`
5. `pip install -r requirements.txt` ==> THE MOST IMPORTANT THING!
6. `./manage.py migrate` ==> migration is telling django to change state of DB.
7. `./manage.py runserver` ==> as this command says, you'll be prompted some URL that can lead you to a blog! 🎈🎈🎉

## Troubleshooting: migration failed

First of all, we need to understand of [migrations(doc)](https://docs.djangoproject.com/en/4.2/topics/migrations/).

> makemigrations is responsible for packaging up your model changes into individual migration files - analogous to commits - and migrate is responsible for applying those to your database.

- `makemigrations` affects to specific app's `migrations` files
- `migrate` affects to database tables.

> You should be making them once on your development machine and then running the same migrations on your colleagues’ machines, your staging machines, and eventually your production machines.

Migration files are version control for databases. Each commits are produced by run `migrate` command. So it might have conflicts when two contributors push different migrations on the same time!!! ⌚

### Answer from Google Bard

Sure, here are some ways to deal with migration conflicts on Django:

1. **Resolve the conflict manually.** This is the most common way to deal with migration conflicts. To do this, you will need to open the conflicting migration files and manually resolve the differences. This can be a tedious process, but it is the only way to ensure that the changes are applied correctly.
2. **Use the `merge` option.** The `merge` option can be used to automatically resolve some types of migration conflicts. To use this option, you will need to run the following command:

```
python manage.py makemigrations --merge
```

The `merge` option will attempt to merge the conflicting migrations together. This may not always be possible, but it can be a helpful way to resolve some common conflicts.
3. **Delete the conflicting migrations.** If you are unable to resolve the conflict manually or using the `merge` option, you can delete the conflicting migrations. To do this, you will need to open the `migrations` folder for the app that is causing the conflict. Then, you can delete the conflicting migration files. Once you have deleted the conflicting migrations, you can run the `makemigrations` command again to create new migration files.

It is important to note that deleting conflicting migrations can cause data loss. If you are not sure whether or not deleting the conflicting migrations will cause data loss, you should consult with a Django expert.

Here are some tips for avoiding migration conflicts:

* Always use the `makemigrations` command before making changes to your Django models. This will create a new migration file for each change that you make.
* Always review the migration files before running the `migrate` command. This will help you to identify any potential conflicts.
* If you are working on a team, make sure that everyone is using the same version of the Django code. This will help to prevent conflicts caused by different versions of the code.

By following these tips, you can help to avoid migration conflicts and keep your Django projects running smoothly.
