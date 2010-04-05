

## Set, append, remove and change job variables

A variable can be set (or changed) using:
 
    moa set variable=value

The construct `variable=value` needs to interpreted as a single
parameter by bash. Hence, you must not use spaces around the equal
sign. If you want to use spaces or special characters in the value,
use single quotes, for example:

    moa set title='This is a $pec!@l title'

Bash attempts to expand values inside double quotes, so, unless you
know what you are doing it is better to stick to single quotes.

Tips:
* A single quote can be embedded in double quotes:
        moa set title="It's a single quote"
* If you need to have single quotes in a complex string that needs to
  be surrounded by single quotes to prevent bash interpolation, use
  this:
        moa set title='It'\''s a $%@^ title'

## Remove 

It is possible to remove a variable from the configuration using:

    moa set variable=

## Appending 

Some Moa templates make use lists of variables. It is possible to add
another value to a list by:

   moa set variable+=value

Note that GNU Make makes no distinction between 


