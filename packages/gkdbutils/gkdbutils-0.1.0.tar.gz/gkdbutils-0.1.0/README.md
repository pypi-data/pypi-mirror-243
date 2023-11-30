# gkdbutils
Database ingest methods and command line utilities for MySQL and Cassandra

This code does NOT install mysqlclient or cassandra-driver.  If you want to use either you MUST install whichever driver you need.

The command line utilities are:
* cassandraIngest (ingest into a Cassandra table from a text file - requires cassandra-driver)
* mysqlIngest (ingest into a MySQL table from a text file - requires mysqlclient)
