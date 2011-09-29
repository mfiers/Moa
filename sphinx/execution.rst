Execution
=========

What is executed upon a Moa run can either be defined by a plugin, or
by a template. Most Moa commands (such as `moa show` are plugin
defined). Only `moa prepare`, `moa run` and `moa finish` call code
defined in a template. 


Each Moa run goes through a number of processes during execution:

- **Main invocation**
- *hook* `prepare_background`
- **Step 1 - Background check**
- *hook*: `post_background` or `background_exit`
- **Step 2 - Recursive check**
- **Step 3 - Execute**

Main invocation
###############

The complete Moa Invocation is embedded in a try / except.

On an error, Moa tries to executed a `post_error` hook and only then
further raise the error

Upon keyboard interrupt, Moa executes the `post_interrupt` hook and
exists with a return code of -2.

Step 1 - Background check
#########################

Is '--bg' defined on the command line? If so, fork, let the child
thread continue and let parent thread exit.

Before continuation, the parent thread executes the `background_exit`
hook. The child thread executes the `post_background` hook.

Step 2 - Recursive check
########################

Moa can be executed recursively by defining -r on the command line. If
`-r` is defined on the commandline, Moa will check what `recursivity
mode` the command has, and proceed accordingly. If it concerns a
template defined command - the recusivity mode is always
`global`, plugins have more options.

global recursive mode (default) 
  Recursive operation is executed at the top level. This means that
  Moa starts walking through the directory structure (starting at
  `cwd`) and executes the command in each directory subsequently
  (proceeding with step 3). The approach is depth first. Directories
  are processed alphabetically and directories starting with '.' or
  '_' are ignored. This is the only option for template defined
  commands.

local recursive mode
  Only for plugins - Recursive operation is executed by the
  plugin. From the top level this means that Moa proceeds as if -r has
  not been defined and expects the plugin callback to deal with
  recursivity.


none recursive mode 
  Only for plugins - recusive execution is not allowed - Moa should
  exit with an error message
  
Each Moa template can have three that are executed in successively:

- Prepare
- Run 
- Finish

