"""
Gnumake
-------

"""
import os
import sys

import moa.utils
import moa.template
import moa.actor
import moa.backend
import moa.sysConf
import moa.logger as l

NEW_MAKEFILE_HEADER = """#!/usr/bin/env make
## Moa Makefile
## http://mfiers.github.com/Moa

include $(MOABASE)/lib/gnumake/prepare.mk
"""

def prepare(job):
	"""
	Prepare for later execution
	"""

	job.options = job.options

	job.makeArgs = getattr(job, 'makeArgs', [])
	job.env = getattr(job, 'env', {})
	
	if job.options.makedebug:
		job.makeArgs.append('-d')

	## Define extra parameters to use with Make
	if job.options.remake:
		job.makeArgs.append('-B')
	if job.options.makedebug:
		job.makeArgs.append('-d')

	job.makeArgs.extend(job.args)

def execute(job, command, **options):
	"""
	Execute!
	"""
	verbose = options.get('verbose', False)
	background = options.get('background', False)

	## make sure the MOA_THREADS env var is set - this is used from inside
	## the Makefiles later threads need to be treated different from the
	## other parameters. multi-threaded operation is only allowed in the
	## second phase of execution.
	job.env['MOA_THREADS'] = "%s" % job.options.threads
	job.env['moa_plugins'] = "%s" % " ".join(moa.sysConf.getPlugins())

	#if moa is silent, make should be silent
	if not job.options.verbose:
		job.makeArgs.append('-s')

	background = job.options.background

	l.debug("Calling make for command %s" % command)
	actor = job.getActor()

	#dump the job env into the actor environment (sys env)
	actor.setEnv(job.env)

	#and the job configuration
	confDict = {}
	moaId = job.template.moa_id
	for k in job.conf.keys():
		v = job.conf[k]
		if isinstance(v, dict):
			continue
		if isinstance(v, list) or \
			   isinstance(v, set):
			v = " ".join(map(str,v))
		if isinstance(v, bool):
			if not v: v = ""
		if k[:3] == 'moa':
			confDict[k] = v
		else:
			confDict['%s_%s' % (moaId, k)] = str(v)

	actor.setEnv(confDict)

	cl = ['make', command] + job.makeArgs

	l.debug("executing %s" % " ".join(cl))
	actor.run(cl, background = background)

def defineOptions(job, parser):
	g = parser.add_option_group('Gnu Make Backend')
	parser.set_defaults(threads=1)
	g.add_option("-j", dest="threads", type='int',
			  help="threads to use when running Make (corresponds " +
			  "to the make -j parameter)")

	g.add_option("-B", dest="remake", action='store_true',
			  help="Reexecute all targets (corresponds to make -B) ")

	g.add_option("--md", dest="makedebug", action='store_true',
			  help="Run Make with -d : lots of extra debugging "+
			  "information")

def initialize(job):

	"""
	Create a new GnuMake job in the `wd`
	"""

	l.debug("Creating a new job from template '%s'" %
			job.template.name)
	l.debug("- in wd %s" % job.wd)

	if not job.template.backend == 'gnumake':
		l.error("template backend mismatch")
		return False

	makefile = os.path.join(job.wd, 'Makefile')
    
	l.debug("Start writing %s" % makefile)
	with open(makefile, 'w') as F:
		F.write(NEW_MAKEFILE_HEADER)
		F.write("$(call moa_load,%s)\n" % job.template.moa_id)
