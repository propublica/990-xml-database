# 990-xml-database
Installable Django apps to consume and store 990 data and metadata. Depends on [IRSx](https://github.com/jsfenfen/990-xml-reader).

## Setup and use

This repo contains four installable django apps. 

Two are used for loading in IRS 990 filings and returns.

* `irsdb.filing`
* `irsdb.return`

And two of which are used for generating the schemas for the returns.

* `irsdb.metadata`
* `irsdb.schemas`

### Loading in 990 Filings and Returns
To use `irsdb.filing` and `irsdb.return` in in your application, first
install this package. You could do that by adding
`https://github.com/datamade/990-xml-db/archive/refs/heads/feature/installable.zip`
to your app's `requirements.txt` file.

Then have the following settings in your app's settings.py file:

```python

INSTALLED_APPS = [
    ...
    'irsdb.filing',
    'irsdb.return',
    ...
]

```

Assuming you have a `manage.py` for your application, you can then run

```console
> python manage.py makemigrations
> python manage.py migrate
```

And now we are finally ready to load in the data.

First, we need to load in the index of filings for a given year. That looks like

```console
> python manage.py enter_yearly_submissions 2021
```

This script checks to see if the IRS' index file is any bigger than
the one one disk, and only runs if it has. You can force it to try to
enter any new filings (regardless of whether the file is updated) with
the `--enter` option.

And then we can load the actual returns. If you want to return all the
returns for a given year, you can do

```console
> python manage.py load_filings 2021
```

If you have a list of target organizations and a list of their EINs, you can just
load those in by supplying a CSV that has a column of EINs with "ein" as the field name.

```console
> python manage.py load_filings 2021 --file=target.csv
```

### Adjusting the return models.py

The IRS's 990 Schema changes over time. The `irsdb.metadata` and `irsdb.schemas` apps 
will generate a new `models.py` that you can use for the `return` app based on what
the `irsx` package currently knows about schemas.

To use, first install this repo. You could do that by adding
`https://github.com/datamade/990-xml-db/archive/refs/heads/feature/installable.zip`
to your app's `requirements.txt` file.

Then have the following settings in your app's settings.py file:

```python

INSTALLED_APPS = [
    ...
    'irsdb.metadata',
    'irsdb.schemas',
    ...
]

GENERATED_MODELS_DIR = '/where/you/want/the/output/to/go'

```

Assuming you have a `manage.py` for your application, you can then run

```console
> python manage.py makemigrations
> python manage.py migrate
```

Next, run

```console
> python manage.py load_metadata
> python manage.py generate_schemas_from_metadata
```

The `generate_schemas_from_metadata` command will create a file called `django_models_auto.py` in the directory you set `GENERATED_MODELS_DIR` to.

You can replace the `irsdb/return/models.py` with this file.


#### Sidebar: 2014 file may need fixing
__There's a problem with the 2014 index file.__ An internal comma has "broken" the .csv format for some time. You can fix it with a perl one liner (which first backs the file up to index_2014.csv.bak before modifying it)

	$ perl -i.bak -p -e 's/SILVERCREST ASSET ,AMAGEMENT/SILVERCREST ASSET MANAGEMENT/g' index_2014.csv

We can see that it worked by diffing it.

	$ diff index_2014.csv index_2014.csv.bak
	39569c39569
	< 11146506,EFILE,136171217,201212,1/14/2014,MOSTYN FOUNDATION INC CO SILVERCREST ASSET MANAGEMENT,990PF,93491211007003,201302119349100700
	---
	> 11146506,EFILE,136171217,201212,1/14/2014,MOSTYN FOUNDATION INC CO SILVERCREST ASSET ,AMAGEMENT,990PF,93491211007003,201302119349100700  

For more details see [here](https://github.com/jsfenfen/990-xml-reader/blob/master/2014_is_broken.md).


### Post-loading concerns


#### Analyze the load process

The loading process uses columns in the filing model to track load process (and to insure the same files aren't loaded twice). 

TK - explanation of keyerrors


#### Removing all rows

There's a [sql script](https://github.com/jsfenfen/990-xml-database/blob/master/irsdb/return/sql/delete_all_return.sql) that will remove all entered rows from all return tables and reset the fields in filing as if they were new. 

If you want to live dangerously, you can run it from the console like this:

`$ python manage.py dbshell < ./return/sql/delete_all_return.sql`


#### Adding or removing indexes

There are management commands to create or drop indexes on object\_id, ein and (for schedule K) documentId. Use
`$ python manage.py make_indexes` or 
`$ python manage.py drop_indexes` . These are just conveniences to create indexes named xx_\<tablename\> --they won't remove other indexes.

#### Removing a subset of all rows

You can remove all filings from a given index file with the [remove_year](https://github.com/jsfenfen/990-xml-database/blob/master/irsdb/return/management/commands/remove_year.py). It's likely to run faster if indexes are in place. 

#### Removing only the rows that were half loaded

If loading gets interrupted, you can remove only the rows where parse\_started is true and parse\_complete is not with the management command [remove\_half\_loaded](https://github.com/jsfenfen/990-xml-database/blob/master/irsdb/return/management/commands/remove_half_loaded.py). It also requires a year as a command line argument.
 
 `$ python manage.py remove_half_loaded 2018`

#### File size concerns

The full download of uncompressed .xml files is over ~74 gigabytes. Processing a complete year of data probably entails moving at least 15 gigs of xml. 

You probably want to look into a tool to help you move these files in bulk. AWS' S3 CLI can dramatically reduce download time, but seems unhelpful when trying to pull a subset of files (it seems like [--exclude '*'](https://docs.aws.amazon.com/cli/latest/reference/s3/index.html#use-of-exclude-and-include-filters) hangs when processing so many files). You may want to look into moving all the files to your own S3 bucket as well. There are also alternatives to AWS' CLI tool, like [S3 CMD](http://s3tools.org/s3cmd).

You'll also want to [configure IRSx file cache directory](https://github.com/jsfenfen/990-xml-reader/#configuring-the-file-cache-directory) to set the WORKING_DIRECTORY variable to the file path of the folder where the xml files are located.

The worst option is to download the uncompressed files one at a time. That sounds, really, really slow. 


#### Server considerations

With most hosting providers, you'll need to configure additional storage to support the static files and the database that's ultimately loaded. Make sure that you set the database storage directory to *that storage*, and get the fastest storage type you can afford.

You may want to look into tuning your database parameters to better support data loading. And you'll get better performance if you only create indexes after loading is complete (and delete them before bulk loads take place).

One random datapoint: on an Amazon t2.medium ec2 server (~$38/month) with 150 gigs of additional storage and postgres running on the default configs and writing to an SSD EBS volume, load time for the complete set of about 490,000 filings from 2017 took about 3 hours.

#### Monthly load

This assumes no schema changes are required, which is usually the case.

Run an S3 sync to the location of the fillings. The whole collection is now over 80 GB, make sure you have room. You can also retrieve some other way (if you don't retrieve en masse the load_filings.py script will attempt to download one filing at a time). It's useful to run this with nohup, i.e.

	nohup aws s3 sync s3://irs-form-990/ ./ & 

Then update the index file data

	$ python manage.py enter_yearly_submissions 2018
	
	
	index_2018.csv has changed. Downloading updated file...
	Done!
	Entering xml submissions from /home/webuser/virt/env/lib/python3.5/site-packages/irsx/CSV/index_2018.csv
	
	Committing 10000 total entered=10000
	commit complete
	Committing 10000 total entered=20000
	commit complete
	Added 24043 new entries.
	
Then enter the filings into the relational database with:

	$ python manage.py load_filings 2018
	
	Running filings during year 2018
	Processed a total of 100 filings
	Processed a total of 200 filings
	Processed a total of 300 filings
	
	...
	
	Handled 24000 filings
	Processed a total of 24000 filings
	Processed a total of 24043 filings
	Done
	
This script finds filings where `submission_year` is the entered year and `parse_complete` has not been set to True. It enters them in groups of 100 and sets `parse_complete` to True after each batch has completed. The script is fairly fault tolerant, but if it dies in the middle it's important to remove all the half entered filings where `parse_started` = True and `parse_complete` is not True. (By default it is null, so don't try to match on `parse_complete` = False). 


--
