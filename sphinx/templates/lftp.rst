lftp
------------------------------------------------

**lftp** - Use LFTP to download files. This template has two modi, one is set lftp_mode to mirror data, in which case both lftp_url and lftp_pattern (default *) are used. The other modus is lftp_mode=get, when one file defined by lftp_url is downloaded. In the mirror mode it is possible to download only those files that are newer as the files already downloaded by using the lftp_timestamp parameter

Commands
~~~~~~~~
['lftp', 'clean']


Backend 
  gnumake
Author
  Mark Fiers
Creation date
  Wed Nov 10 07:56:48 2010
Modification date
  Wed Nov 10 07:56:48 2010



