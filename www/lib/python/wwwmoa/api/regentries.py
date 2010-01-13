
## Constants ##

REQUIREMENT_PRESENCE=1
REQUIREMENT_ABSENCE=-1
REQUIREMENT_NONE=0





## Internal DB ##

commands={}


## moa-jobinfo Command Entry ##

commands["moa-jobinfo"]={
    "methods" : {"GET" : {"requirements" : {"job" : REQUIREMENT_PRESENCE,
                                            "dir" : REQUIREMENT_NONE,
                                            "file" : REQUIREMENT_NONE,
                                            "read" : REQUIREMENT_PRESENCE,
                                            "write" : REQUIREMENT_PRESENCE
                                            },

                          "help" : "Retrieves information about a Moa job.",
                          "params" : {}
                          }
                 },

    "title" : "Moa Job Information",
    "help" : 
"Represents information about a Moa job, including its parameters, targets, \
and \"help strings\"."
    }




## moa-jobsession Command Entry ##

commands["moa-jobsession"]={
    "methods" : {"GET" : {"requirements" : {"job" : REQUIREMENT_PRESENCE,
                                            "dir" : REQUIREMENT_NONE,
                                            "file" : REQUIREMENT_NONE,
                                            "read" : REQUIREMENT_PRESENCE,
                                            "write" : REQUIREMENT_PRESENCE
                                            },

                          "help" : "Retrieves the status of a Moa job.",
                          "params" : {}
                          },

                 "PUT" : {"requirements" : {"job" : REQUIREMENT_PRESENCE,
                                            "dir" : REQUIREMENT_NONE,
                                            "file" : REQUIREMENT_NONE,
                                            "read" : REQUIREMENT_PRESENCE,
                                            "write" : REQUIREMENT_PRESENCE
                                            },

                          "help" : "Runs a Moa job.",
                          "params" : {"target" : {"mandatory" : False,
                                                  "help" : "The Moa target to execute."
                                                  }
                                      }
                          },

                 "DELETE" : {"requirements" : {"job" : REQUIREMENT_PRESENCE,
                                               "dir" : REQUIREMENT_NONE,
                                               "file" : REQUIREMENT_NONE,
                                               "read" : REQUIREMENT_PRESENCE,
                                               "write" : REQUIREMENT_PRESENCE
                                               },

                             "help" : "Cleans up a Moa job.",
                             "params" : {}
                             }
                 },

    "title" : "Moa Job Status Information",
    "help" : "Represents the status of a Moa job."
    }




## moa-jobparams Command Entry ##

commands["moa-jobparams"]={
    "methods" : {"GET" : {"requirements" : {"job" : REQUIREMENT_PRESENCE,
                                            "dir" : REQUIREMENT_NONE,
                                            "file" : REQUIREMENT_NONE,
                                            "read" : REQUIREMENT_PRESENCE,
                                            "write" : REQUIREMENT_PRESENCE
                                            },

                          "help" : "Retrieves the values of all parameters.",
                          "params" : {}
                          },

                 "POST" : {"requirements" : {"job" : REQUIREMENT_PRESENCE,
                                             "dir" : REQUIREMENT_NONE,
                                             "file" : REQUIREMENT_NONE,
                                             "read" : REQUIREMENT_PRESENCE,
                                             "write" : REQUIREMENT_PRESENCE
                                             },

                           "help" : "Sets the value of a single parameter. The value should be sent as the request body.",
                           "params" : {"key" : {"mandatory" : True,
                                                "help" : "\
The key associated with the parameter."
                                                }
                                       }
                           },

                 "PUT" : {"requirements" : {"job" : REQUIREMENT_PRESENCE,
                                            "dir" : REQUIREMENT_NONE,
                                            "file" : REQUIREMENT_NONE,
                                            "read" : REQUIREMENT_PRESENCE,
                                            "write" : REQUIREMENT_PRESENCE
                                            },

                          "help" : "Updates the entire collection of parameters.  The parameters should be included \
in the body of the request, and should be a JSON encoded dictionary of key-value pairs.  Not all \
parameters must be specified; if not specified, the current values will be maintained.",
                          "params" : {}
                          }
                 },

    "title" : "Moa Job Parameters",
    "help" : "Represents a Moa job parameter set."
    }




## moa-job Command Entry ##

commands["moa-job"]={
    "methods" : {"GET" : {"requirements" : {"job" : REQUIREMENT_PRESENCE,
                                          "dir" : REQUIREMENT_NONE,
                                          "file" : REQUIREMENT_NONE,
                                          "read" : REQUIREMENT_PRESENCE,
                                          "write" : REQUIREMENT_PRESENCE
                                          },

                          "help" : "An alias for \"moa-jobinfo\".",
                          "params" : {}
                          },

                 "PUT" : {"requirements" : {"job" : REQUIREMENT_NONE,
                                            "dir" : REQUIREMENT_PRESENCE,
                                            "file" : REQUIREMENT_ABSENCE,
                                            "read" : REQUIREMENT_PRESENCE,
                                            "write" : REQUIREMENT_PRESENCE
                                            },

                          "help" : "\
Creates a new Moa job in the specified directory, \
overwriting one if it already exists.",
                          "params" : {"template" : {"mandatory" : True,
                                                    "help" : "\
The template to create the new job from."
                                                    },

                                      "title" : {"mandatory" : False,
                                                 "help" : "A title for the new job."
                                                 }
                                      }
                          },

                 "DELETE" : {"requirements" : {"job" : REQUIREMENT_PRESENCE,
                                               "dir" : REQUIREMENT_NONE,
                                               "file" : REQUIREMENT_NONE,
                                               "read" : REQUIREMENT_PRESENCE,
                                               "write" : REQUIREMENT_PRESENCE
                                               },
                             "help" : "\
Removes a Moa job from the specified directory.",
                             "params" : {}
                             }

                 },
    "title" : "Moa Job",
    "help" : "Represents a Moa job."
    }




## moa-templates Command Entry ##

commands["moa-templates"]={
    "methods" : {"GET" : {"help" : "Retrieves the template listing.",
                          "params" : {}
                          }
                 },
    "title" : "Template Collection",
    "help" : "Represents the collection of currently installed templates."
    }




## ls Command Entry ##

commands["ls"]={
    "methods" : {"GET" : {"requirements" : {"job" : REQUIREMENT_NONE,
                                            "dir" : REQUIREMENT_PRESENCE,
                                            "file" : REQUIREMENT_ABSENCE,
                                            "read" : REQUIREMENT_PRESENCE,
                                            "write" : REQUIREMENT_NONE
                                            },
                          "help" : "Retrieves a directory listing.",
                          "params" : {"filter" : {"mandatory" : False,
                                                  "help" : "\
A filename filter to apply to the listing."
                                                  },

                                      "filter-type" : {"mandatory" : False,
                                                       "help" : "\
A type of filename filter to apply to the listing. \
If not included, \"filter\" will be ignored."
                                                       },

                                      "filter-ignorecase" : {"mandatory" : False,
                                                             "help" : "\
A value that represents whether or not the filename \
filter should be case-sensitive. If not included, \
the default is case-sensitive."
                                                             }
                                      }
                          }
                 },

    "title" : "Directory Listing",
    "help" : "Represents a directory listing."
    }




## help Command Entry ##

commands["help"]={
    "methods" : {"GET" : {"help" : "Retrieves an API Doc.",
                          "params" : {"command" : {"mandatory" : False,
                                                   "help" : "\
The command to access help for."
                                                   }
                                      }
                          }
                 },

    "title" : "API Doc Collection",
    "help" : "Represents the API Doc collection."
    }
