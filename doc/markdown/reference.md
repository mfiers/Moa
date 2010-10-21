# Reference

Note: this is a work in progress - and currently not finished

## Moa Makefile load order

Makefiles are sensitive to the order in which definitions are made,
and thus the order in which the include files are loaded. Moa broadly
recognizes two stages: "definition" and "implementation". The
implementation phase starts once the moa core library is
loaded. 

Moa makefile load starts with loading the template makefile in the
current work directory. This Makefile loads a number of other
makefiles that load more Makefiles. The following list shows a
detailed load order

1. **Makefile**: The Makefile in the working directory
    1. **prepare.mk**: initial definitions. At the start of the
        prepare.mk file the following files are loaded:
        
        1. **gmsl**: The
            [GNU Make Standard library](http://gmsl.sourceforge.net/),
            a number of utilities for use in Makefiles.
        1. **global configuration** (`$(MOABASE)/etc/moa.conf`): This
          file loads the global default configuration file (
          `$(MOABASE)/etc/moa.conf.mk.default`)
        1. **Project configuration**: (if present). Moa attempts to
          find this in the first parent directory of the current
          working directory that contains a moa project with template
          "project".
        1. **Local configuration** (`moa.mk`)
        * **Plugin definitions**: For each plugin name defined in the
          variable `moa_plugins`, moa attempts to load a file called
          `$(MOABASE)/template/moa/plugins/PLUGINNAME_def.mk`.
        
        Once these files are loaded, more Moa specific definitions
        follow in `prepare.mk`
        
    1. **template Makefile**: (`$(MOABASE)/template/TEMPLATENAME.mk`) A
        makefile specific for the job at hand. This template Makefile
        might attempt to load prepare.mk, unless it was already loaded
        earlier. The first part of the template Makefile is used for
        defining template specific variables. 
        
        The definition phase of a Moa Makefile is concluded by loading:
        
        1. **Moa core** (`$(MOABASE)/template/moa/core.mk`). The first
          thing the Moa core libraries do is loading a set of plugins:
            1. **Plugin cores**:
              (`$(MOABASE)/template/moa/plugins/PLUGINNAME.mk`)
	      
          After the plugins are loaded moa defines a number of core
          targets, most importantly, the default target that defines
          the execution order (see the next paragraph). As much of the
          functionality as possible is definined as a plubin.
	
	Once the core library has loaded, the template specific
	targets are parsed.
      
## Execution order

### `moa run`

* `moa_hooks_prewelcome`
* `moa_welcome`
* `moa_hooks_precheck`
* `moa_check`
* `moa_prepare`
* `$(moa_id)_prepare`
* `$(moa_id)`
* `$(moa_id)_post`
* `moa_post`

### `moa set`

* `moa_hooks_preset`
* (python routine)
* `moa_hooks_postset`


## Environment variables

These environment variables are recognized by Moa:

`MOAANSI`
:    The default is to use (ANSI) colored characters in the output. To
     prevent this from happening, set this (environment) variable to
     `no`.

`MOAPROJECTROOT`
:    The root of a moa project - project root is a parent directory of
     the current directoy that has a moa job with template
     `project`. If there is no project root, this variable is
     undefined.


## Global functions

These function are meant to be used at the top level of a Makefile
(meaning, not inside a target command block). Function can be called
using: (Note, some of this should go to plugin docs)


`$(call moa_fileset_define,ID,EXTENSION,HELP)`
:    Define a set of files to be recoginized by Moa.

`$(call moa_fileset_remap,INPUT_ID,OUTPUT_ID,OUTPUT_EXTENSION)`
:    Remap a set of input files to ....

`$(call moa_fileset_remap_nodir,INPUT_ID,OUTPUT_ID,OUTPUT_EXTENSION)`
:    as `moa_fileset_remap`, but without prefixing the set with a
     subdirectory

## Command functions

The following commands render a command that can be executed inside
a target command block

* `$(call echo,TEXT)`

  ~ Returns an echo statement for the text with a green block
    prepended. The color allows for easy recognition of the echo'd
    statements. Note that these only work within the code block of a
    target.

- `$(call errr,TEXT)`
  
  ~ as `$(call echo,TEXT)`, but with a red marker (error)

`$(call exer,TEXT)`

  ~ as `$(call errr,TEXT)`, but exits the Makefile with an error

`$(call exerUnlock,TEXT)`

  ~ as `$(call exer,TEXT)`, but remove the Moa lockfile

`$(call warn,TEXT)`

  ~ as `$(call echo,TEXT)`, but with a yellow marker

## Variables

$(comma)

  ~ a comma

$e

  ~ Can be used in place of Makefile "@". A @ prepended to a command
    inside a target in a Makefile supresses echoing of that line
    during execution. If $e is used, then supression is depending on
    executing moa with the -v (verbose) parameter.

$(empty)

  ~ empty

$(parC)

  ~ parentheses close

$(parO)

  ~ parentheses open

$(sep)

  ~ contains the pipe symbol "|"

$(space)

  ~ a single space
