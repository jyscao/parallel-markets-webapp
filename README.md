# Parallel Markets Investor Intake Web App

See [this document](https://gist.github.com/bmuller/341e89cf87083119ad1241f5b896fa7c) for detailed specifications to the problem.



### Dependencies & Building

* Python 3
* [Flask](https://flask.palletsprojects.com/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)

Python 3 is available by default on almost all Linux and macOS systems. So you
should in theory be able to just use Python's built-in `pip` package manager
to install the 2 project dependencies.

However it's usually recommended that you create an isolated environment for your project
to mitigate the possibility of installed packages (and their pulled-in dependencies) from
breaking your base OS Python environment. Many popular and well established tools exist
for this very purpose, such as `venv`, `virtualenv`, `pipenv`, `poetry`.

I personally prefer to use the [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
package & environment manager, which can be used as follows:

0. Download the installation script from the Miniconda link above, run and follow the prompts to install

1. `$ conda create -n para-mark python=3` to create an environment dedicated to running this project

2. `$ conda activate para-mark` to activate the above environment

3. `$ conda install flask flask-sqlalchemy` to install the project dependencies

4. `cd` into the project root, and you're ready to run the web application

Once complete, use `$ conda deactivate to exit the conda environment`



### Run the Web App

At the project root, there is a CLI script for managing the database, which for simplicity's sake is
chosen to be SQLite. Run `$ ./db-cli.py -h` to see all the options available.

For a quickstart of the web application, simply run `$ ./db-cli.py -c`, which will create an instance of
a SQLite database at `/tmp/parallel-markets/`.

With the database intialized, the correct environment activated, execute `$ flask run`
to serve the web app from your localhost interface. You can optionally pass a `--port` number
if the default one of 5000 is taken.

In case, something doesn't work, you can set the environment variable `FLASK_ENV` to `development` to
get thorough debugging help on the console and from the browser.

Combining all the above, we can do:

`$ FLASK_ENV=development flask run --port=8000`



### Web App Usage

Once the app is served, it can be accessed from any browser at `http://localhost:8000` or whichever port you selected.

The web app consists of a single page with multiple form inputs, which are used to sequentially enter information
of potential investors. All information are required, they are:

* first name
* last name
* date of birth (YYYY-MM-DD)
* phone number (10-digit US/Canada)
* address (street, US State, 5-digit zip code)
* 1 or more documents to be uploaded to the server

If all information are valid, then the investor's info and his/her uploaded document(s)
will be saved to the SQLite database created earlier. There are 2 tables in the database:

* investor - contains all information
* document - contain the file names of all uploads, with investor ID as the foreign key

Note: investor and document is a one-to-many relationship

To inspect the contents of the database, execute `$ ./db-cli.py` without any options, or specify a specific table
with `-i` or `-d` for the `investor` and `document` table respectively.



### TODO List

#### Features
- [x] detecting and handling updating phone numbers and/or addresses for existing investors with matching names & date of birth
- [ ] encrypt uploaded files, since the uploaded documents likely contain sensitive data
- [ ] allow skipping file upload when updating existing users
- [ ] authentication & authorization
- [ ] add page to allow supseruser to view all existing investors that have been entered
- [ ] allow superuser or authenticated users to download their own uploaded file(s)

#### Database & Models
- [ ] add normalized name columns to `investor` table 
- [ ] add more columns to the `document` table for storing useful file attributes: e.g. filetype (extension, MIME), size, upload date, etc.
- [ ] use separate tables for investors' phone number(s) & address(es), since these can potentially be one-to-many relationships
- [ ] use interfaces for the application model classes, which should allow switching DBs easier (SQLite doesn't support concurrent writes)
- [ ] create database schema using SQL scripts instead of the ORM, to allow for better cross framework/language portability

#### Application Logic
- [ ] add application config file for convenient configuration of database storage location, upload folder, secret key, etc.
- [ ] use WTForms to properly validate form inputs (e.g. allow international phone numbers)

#### Front-End
- [ ] add styles using a CSS library (e.g. Bootstrap, Tailwind)
- [ ] use more appropriate input forms where applicable (e.g. date-picker for DOB, dropdown for US State)

#### Miscellaneous
- [ ] add tests
