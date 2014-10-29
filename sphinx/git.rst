Git integration
===============

Note:
* Integration with Git is a relatively new feature - there might be
  dragons.
* Moa/Git will try to keep track of the *structure* of your workflow,
  **not** of the data you are processing.


Moa integrates with `Git <http://git-scm.com/>`_ for a number of
reasons:

* to automatically keep your workflow under version control. Having
  your work under version control means that at all times you can find
  out what your workflow looked like at a certain date.
* to allow you to share your workflow using Git. For example, you
  could publish your workflow to Github, and allow other researchers
  to clone and improve on your work (which you can then import into
  your own workflow again).
* to pull templates from remote git repositories. This allows anybody
  to create, maintain and distribute templates for you to use.

To make this work, you must make sure that `git` and `git subtree` are
installed and that the moaGit plugin is enabled. Also make sure that
your workflow is under Git version control. If you create 'Moa
projects', Moa will try to create a new repository for you. Otherwise,
you must run `git init` to create a new repository.


A workflow under Git control
----------------------------

If you've created a new Moa project & made sure it is under git
control, Moa will try to automatically commit all changes. One
important thing to notice here is that if you make manual changes to
the workflow - you will need to commit them yourself. If you fail to
do so, they will likely be automatically commited by the next Moa
operation. In which case they are under version control, but the
commit message will not make any sense.


Sharing a workflow using Git
----------------------------

Your workflow is a normal git repository. See the excellent
documentation of Git & Github how to share git repositories.

Getting templates from a remote git repository
----------------------------------------------

If you want to install a template froma remote git repository, Moa
will merge the template repository with the workflow's repository
using `git subtree <https://github.com/apenwarr/git-subtree>`_. This
approach has a a number of nice properties:

- The template is integrated in the local workflow and can be copied
  around and changed (as one normally would do within a git
  repository).
- The template code does not change unless requested (as with regular
  templates). Even when sharing or duplicating your repository - the
  template remains unchanged.
- If required, it is possible to update to the latest version of the
  remote template repository (using a regular `moa refresh`)
- It possible to upload the template changes upstream.

Note - the git submodule approach was another candidate for implenting
this, but submodules are difficult to be copied once they are checked
out. Additionally, the `git subtree
<https://github.com/apenwarr/git-subtree>`_ approach has as an
advantage above the `git subtree merge strategy
<https://www.kernel.org/pub/software/scm/git/docs/howto/using-merge-subtree.html>`_
that it is easier to upload changes upstream.

Define a template provider
~~~~~~~~~~~~~~~~~~~~~~~~~~

To set up moa to work with git template you need to define a template
provider, for example::

	$ moa set -s template.providers.gtp.class=gitmodule
	$ moa set -s template.providers.gtp.base='https://github.com/mfiers/moa_template_%s.git'
    $ moa set -s template.providers.gtp.enabled=true

This defines a provider (called gtp) that pulls templates from github
(but any other git server can be used). Note that it is probably
advisable to set `*.enabled=true` as last - to prevent an incomplete
import.

After doing this you can run::

    $ mkdir 30.run_bowtie
    $ cd 30.run_bowtie
	$ moa new gtp:bowtie -t 'a sensible title'

which would expect and merge a repository in the following location:

    https://github.com/mfiers/moa_template_bowtie

Moa requires to have template name (bowtie in the example above) and
the configured `base` resolve to a valid git repository url. This
provides a user friendly syntax and the ability to use any git
repository required.
