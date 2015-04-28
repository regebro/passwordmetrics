Password strength
=================

Password strength is a measure of the effectiveness of a password in resisting
guessing and brute-force attacks.[1]_  Since users like to have passwords that
are easy to remember, they tend to pick weak passwords that are easy to guess.

Many administrators of systems and sites try to force their users to have more
secure passwords by forcing a length or requiring that you use both uppercase
and lowercase, or add punctuation, etc. This XKCD cartoon illustrates why
this is a bad idea:

.. image:: https://imgs.xkcd.com/comics/password_strength.png

In addition, many users will just take their weak password and add ones and
exclemation marks to it. So instead of "banana" they now have "Banana1!".
That is harder to guess, but not a lot harder.

The most secure passwords are long passwords with randomly generated characters,
such as "/JGuJzxbm<K%n3d^7#,)". This is however hard to remember and type,
so it's a good password for when you have a password manager, like in your
web browser, but not a good password for an admin password on a computer.

How to get your users to have strong passwords
----------------------------------------------

The passwordmetrics package enables you to get a measurement of how hard the
entered password is to guess. The 'entropy' is a measurement that is
approximately how many bits of information is contained in the password, and
therefore how hard it is to guess. The higher, the better.

You can then tell your users if that is a weak, average or strong password.
Google's user management is a good example of a UI that does this correctly.
You can also set a minimum strength.

To determine what is "good", run pass wordmetrics on a couple of passwords you
would think are good, and use the resulting number as a measurement.

For reference, "banana", a password that is unacceptably easy, has an entropy
of approximately, 6. The above 20 character random string has an entropy of
around 124, and XKCD's "correcthorsebatterystaple" has an entropy of around 45.


.. [1] http://en.wikipedia.org/wiki/Password_strength

