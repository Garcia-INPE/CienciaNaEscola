# Ciência na Escola
Repositório para os códigos do projeto Ciência na Escola

Este projeto visa incentivar os jovens a dispertar curiosidade científica através do engajamento.

To PythonAnywhare: https://www.youtube.com/watch?v=5jbdkOlf4cY&t=135s

- Create account in PythonAnywhare
- Create account in Github.com
- cd <project_main_dir>
- virtualenv venv                               # create a virtual env in venv/ 
- source venv/bin/activate                      # Activate it
- pip install <packages>                        # Install all packages via "pip install ..."
- pip freeze > requirements.txt                 # Create a list of installed packages (to replicate the env in another host)
- git init                                      # Create a local git repo 
- echo "venv/" > .gitignore                     # Prevent from uploading the venv/ dit to Github.com (can add more files/dir to ignore)
- git add .                                     # Add all files, except those in the .ignore, to a intermediate stage in repo (still locally)
- git commit -m "First commit"                  # Attach a message for the next repo upload
- Create a remote repo in Github.com            # do not choose to create README.md
- Copy the URL of the just created repo         # https://github.com/....
- git remote add origin <URL>
- git push -u origin main                       # Upload the local repo. Take are! Used to be ...origin main
- Refresh the browser at github.com             # To check if local repo files are there 
- Goto PythonAnywhare tab in the browser
- Console / Bash
- git clone <URL>                                  # Copy all the files to PythonAnywhere to a folder (repo name)
- virtualenv venv --python='/usr/bin/pythoon3.10'  # Create and activate venv. Use Python version according to your app.
- cd <repo_folder> 

Installing packages disabling the cache
Sometimes pip requires much more disk space during the installation than the size of the installed package. 
That's why some packages are impossible to install for free accounts on PythonAnywhere. 
You can use pre-installed ones. See pythonanywhere.com/batteries_included#

- pip cache purge                                  # First clear the cache
- pip install -r requirements.txt --no-cache-dir   # Install the the needed packages without cache

- Go to "Web" tab in PythonAnywhere
- Create a new web app, next, Flask, Python version, next
- Click on the just created app shown under "Configuration for"     # A Hello, World! should appear
- Virtualenv: choose env
- Code:
  . Source code: <repo_folder>  
  . Working directory: <repo_folder>, exemple: /home/JRMGarcia/CienciaNaEscola
- WSGI Config file: click, delete lines 19-48                       # Refers to Hello World
- Got to Flask section and uncomnent
  - In path --> especify repo directory
  - in from main_flask_app_file import app as application, adapt for your app
    . Exemple: from index import server as application
- Go to PA Web tab and reload
- Check logs if errors

