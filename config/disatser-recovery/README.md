If the server is somehow destroyed then this document will outline the steps to
recover.


You simply need to reconfigure the software on a new server just as if you are
setting up HIVE for the first time.

Then you must use the database backup file.

Its url is https://cegphi.s3.amazonaws.com/hive-bin-backup.des3

This url is protected and the file located here is encrypted.  You need AWS
credwentials to access this file.  This file is also copied nightly to the
HIVE backup server at CEG's facility.

To decrypt the file do this (note you must know the passphrase):

openssl des3 -d < hive-bin-backup.des3 | tar zx