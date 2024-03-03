========
ghstatme
========
about
-----

Obscenely trivial program to collect repo stats. This will fetch and keep
your git repo traffic statistics forever (or as long as you don't loose your
data, because you did not care to make a backup).

usage
-----
Simply call::

    ./ghstatme.py -u $user -r $repo -o $db_path -t $token

*user* is owner's repository, in case of this repo, it will be ``mlyszczek``

*repo* is a repository name you want to fetch stats for. In case of this repo
it will be ``ghstatme``

*db_path* program will store traffic statistics here. Check below for format

*token* your github token. Generate your private token here
https://github.com/settings/tokens

db format
---------
Database format is stupidly trivial text file. As backend **ghstatme** is
using your filesystem. Each user has it's own directory. Each repository
has it's own directory. And each day has it's own file. So output format is::

    $db_path/$user/$repo/$timestamp

*timestamp* is in format ``YYYY-mm-dd``

Inside there are 4 integers::

    13 37 21 37

They represent stats for the day in order:

* unique views
* view count
* unique clones
* clone count

With that you can easily do whatever you want.

If you want csv for all stats::

    cat $db_path/$user/$repo/* | tr ' ' ','

Only want csv for single month? Easy::

    cat $db_path/$user/$repo/2024-02-*

Or maybe you want few months? Like, January, February, March and June?
Sure thing::

    cat $db_path/$user/$repo/2023-{{1..3},6} | tr ' ' ','

Use shell globbing and pipes for your advantage!
