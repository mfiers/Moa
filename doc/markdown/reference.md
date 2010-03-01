#Moa reference 

## moa get

## moa list

Returns a list of available templates

## moa new

## moa ren

A utility to rename directories. If you're numbering directories, as
suggested in the Moa documentation, then this utility helps in
renumbering directories. For example if you have the following directories
structure::
  
   10.download
   20.blast
   30.genepred

Rearranging is made easier wit this command::

   moa ren 30 40

would rename `30.genepred` to `40.genepred`. The command refuses if
there are confliciting numbers, for example moa `ren 20 30` will not
work.

## moa set

## moa status

## moa test


