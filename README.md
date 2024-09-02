The code was created as solution to a problem and as a final project for postgraduate course on University of Technology in Poznań in 2017.

The business problem is: in a complex, multistep process of loading CAR, how to visualize and measure impact of a single change to this process?

Basic terms:
- CAR - Customer Analytical Repository. Corporate Datawarehouse DataMart, system that is loaded via a process composed of circa 850 SQL queries. The system of loading CAR is an acyclical chain of phases.
The purpose of CAR is to deliver a business multilevel description and image describing customer via his: products, trends, behaviors, preferences, potencials and activities. Examples: average account inflows, number of internet banking successful logins.
- CAR Area - a business area relating to a specific concept in banking, also a data table in CAR containing fields describing the concept per ID (per customer, account etc)
- SQL Part - a single SQL query
- CMT - Customer Mapping Table - SQL documentation and at the same time technically a formal description that is processed in the loading phase of ETL in order to extract the instructions for the software
- characteristic - a unique metric defined in CAR

  The tool solves the problem in the following way:
  - step 1: parser of CMT files that extracts key parts of SQL queries (such as SELECT fields, FROM tables, fields in WHERE and GROUPBY conditions) and exports them.
  - step 2: create a graph database containing all the SQL elements extracted before with edges symbolizing useful connections (type of relation between field and table and relating tables to tables)
  - step 3: a mechanism that shows consequences / impact a given change in SQL query may have on other 
    The scripts use among others: openpyxl, pathlib, networkx, re, matplotlib and pyqt5 libraries.

The code implements an original solution to the problem based on research and experiences of the author.
