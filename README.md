# Team Name: SQLytes

## Setting up a working environment
1. Create your own virtual environment folder in the workspace where the program is going to reside. This allows the project to localize the packages and versions instead of applying system-wide changes. Use this as a general guide, as the setup varies based on OS. This is targeted towards macOS users.
   1. Run the following command: `python -m venv <.venv>`
      - `.venv` can be named anything.
      - The creation of your venv was successful if a `<.venv>` folder appears in your workspace and if `(<.venv>)`
        appears at the beginning of your directory. Example: `(<.venv>) <username> <ProjectWorkspace>`
   2. Change your Python environment to the location of where your created venv resides.
   3. Run the following command to activate your venv:
      ```
      source <venv_name>/bin/activate
      ```
2. Install the libraries used in this project by running the following command inside your venv:
   ```
   pip install -r requirements.txt
   ```
3. The required Python version for this is `Python 3.10.2` or newer. If your system-wide version of Python is older,
   the venv can be configured to handle independent versions of Python.

If you're running this on PyCharm, it's worth knowing that PyCharm automatically sets this up for you and can also
auto-activate your venv each time the IDE is fired up. More info on how to configure this can be easily found online.

## Workflow Rules
1. **ALWAYS** make a new branch for your new changes. Never make changes on the main/master branch since this can
   lead to trouble and result in the project being broken for everyone.
2. Write tests for every feature you are going to implement.
3. Commit and push in small steps. If a change is working as expected, commit and push it to the current branch you are
   working on. Do not make commits, push, or merge in where no more than 2 features or working changes have been
   implemented. This allows us to easily traceback where the code broke starting from the last working commit or push.
4. Merge with main once all your changes in the branch you are making have been tested and are working.
5. Remember to update `requirements.txt` as new libraries are introduced.
6. Separate frontend and backend work into their own folders/workspaces.
7. **ALWAYS** work in your venv so that if something goes wrong, your general packages aren't affected.
8. Follow Python best practices :snake:!
9. Remember to **set your line length to 120 characters** so that the source code can be consistently formatted,
   regardless of screen size.
10. Ensure that any IDE, venv, or compilation specific artifacts are listed under `.gitignore`.

## Credentials for the Database (Heroku Data, disactivated)
- Host
   ```
   ec2-34-193-110-25.compute-1.amazonaws.com
   ```
- Database
   ```
   dcfajr03gbu43b
   ```
- User
   ```
   rfuunoitsqrvhu
   ```
- Port
   ```
   5432
   ```
- Password
   ```
   ad03f3262f921e6a03acbf5a2def6d79b298b9e3e732e33a641e359e141e69b3
   ```
- URI
   ```
   postgres://rfuunoitsqrvhu:ad03f3262f921e6a03acbf5a2def6d79b298b9e3e732e33a641e359e141e69b3@ec2-34-193-110-25.compute-1.amazonaws.com:5432/dcfajr03gbu43b
   ```
- Heroku CLI
   ```
   heroku pg:psql postgresql-acute-63860 --app sqlytes-inventory-app
   ```

## Docker Postgres Setup
Install [Docker Desktop](https://docs.docker.com/desktop/). The following are the commands specific to our DB during the setup. It's useful to utilize the GUI to view console outputs when running commands.
#### Initial Setup
First time setup:
```shell
docker pull postgres # ensure it shows up on Docker Desktop
docker-compose build # build container (whenever changes are made to composer or Dockerfile)
```
When testing:
```shell
docker-compose up -d # start container
docker exec -it inventory-tracking-app-sqlytes-db-1 psql -U docker_admin -d sqlytes-inventory-app # access container
```
> The argument for *-it* is the container name. View your containers using: `docker container ls`.

#### Container
- You may or may not need to install the latest version of [PostgreSQL](https://www.postgresql.org/download/).
- Optionally, connect to a DB with a user with `\c` or `\c database`.
- Check the list of available DBs with `\l`.
- View the tables within that DB with `\dt`.
- When finished, stop the current container via: `docker-compose down`. Add `-v` to destroy volumes.

## Voila
In order to get *Voilá* to display the front page of the application:

1) Make sure to download the latest `requirements.txt` packages.
2) *Voilá* web applications display contents of Markdown cells as well as any cell's output. This means that if you want
   to add more content to the Frontend, you can do it by adding new code that outputs something into a new cell.
3) In order to compile and run the application use:
   ```
   voila Frontend/sqlytes_inventory.ipynb
   ```
   Note that both Docker and `main.py` must be running. Additionally, change `dbconfig.py` as needed to connect to
   localhost instead. Finally, *remember to always clear all cell outputs* before pushing.