The `project` template serves as a placeholder to organize a project
under. The project should be created in the subdirectories of
directory holding the `project` job. Each Moa job in the
subdirectories will automatically load the settings from the project
job, before it loads its project specific settings. This allows a user
to set project specific parameters.

Projects will also play a role in several plugins (under development):

* `git` will create repositories on a project base
* `archive` will have the ability to archive a project with one
  command.
  
It is not advised to place projects within projects, although there is
nothing to stop you from doing so.
