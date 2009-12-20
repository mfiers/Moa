List of terms used in Moa


(GNU) Make

    GNU Make is the central piece of software around which Moa is
    build. GNU Make is a powerful system that is able to automate
    building and processing of files. Make is usually employed to
    compile software, but is remarkably useful in other contexts, such
    as bioinformatics.

Makefile

    A makefile that provides a step-by-step description of a build
    process. A makefile is used by (GNU) Make to automate that build
    process. In the context of Moa, a makefile describe a
    bioinformatics related job.


(Makefile) templates

    Moa aims at providing reusable building blocks that can be used to
    build elaborate bioinformatics pipelines. Moa provides a set of
    core makefile libraries that provide the core functionality well
    as an extensive set of 'templates' that describe a single
    taks (such as BLAST).


Job

    An job is a directory with a Moa Makefile that includes a Moa
    template makefile. A job performs a single analysis step. The
    Makefile is a full fledged, extensible, Makefile that in its most
    basic form performs the analysis specified but provides sufficient
    hooks for an experienced user to fully customize it.