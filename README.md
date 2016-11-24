LibraryHog
==========

A simple script which automatically renews all items checked out from the University of Warwick's library.

![Screenshot](https://lol768.com/i/movajfs6TEJg9Q)

A note on renewals
------------------

Renewals are possible if:

* The item is not on hold
* At least a day has passed since the last renewal

When renewals happen, the due date is extended to the current date + the standard loan length (2 weeks).

Thus, to maximise the time you can have a single book without returning it, it is best to make a renewal attempt
every day:

* If another library user places a hold, you will have renewed as close as possible to the hold, and will get the
largest amount of the standard loan length
* Renewing every day like this will continuously move the due date one day in the future, so at all points in time
there will be two weeks to read the book

Using the script
----------------

Authentication is via LDAP (not WebSignOn), so the script needs to know your Warwick usercode and password. It is
suggested that you carefully read through the script prior to using it in the interests of security. It's very simple
and well-documented.

You can either provide the credentials at runtime (the script will prompt you) or set two environment variables:

```
export WARWICK_USERNAME="uxxxxxxx"
export WARWICK_PASSWORD="password123"
python3 main.py
```

The latter approach is suggested for automation. If you're planning on using the script with a cronjob, it's suggested
to only run it once a day at 0030 or similar:

```
30 0 * * * /path/to/lib_hog.sh
```

If you are going to store your password for this use, you must ensure it is done in a secure manner to comply with
the ITS AUP.

TODO
----

* Watch recently returned items (due to a hold) and request a hold as soon as they are checked out.

Motivation and ethical considerations
-------------------------------------

Motivations:

* Different library users are arbitrarily given different loan lengths. University staff take out books for the entire
  academic year by default which forces use of holds to try and take out items which would otherwise be available.
* Holds placed very close to the due date on an item you were planning to renew are inconvenient. The fine amount
  is also impacted.

Ethical considerations:

* The script should not be used to take out an item for longer than is required to read/refer to/make notes on it.