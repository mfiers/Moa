
## Constants ##

R_FILE=1
R_DIR=2
R_JOB=4
R_WRITE=8




## Internal DB ##

commands={}


## moa-jobinfo Command Entry ##

commands["moa-jobinfo"]={
    "methods" : {"GET" : {"requirements" : R_JOB,
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
    "methods" : {"GET" : {"requirements" : R_DIR,
                          "help" : "Retrieves the status of a Moa job.",
                          "params" : {"output" : {"mandatory" : False,
                                                  "help" : "\
A value that represents whether the outputs \
of the Moa job should be sent in the response. \
A value of '1' indicates that they should; all \
other values indicate that they should not."
                                                  }
                                      }
                          },

                 "PUT" : {"requirements" : R_JOB|R_WRITE,
                          "help" : "Runs a Moa job.",
                          "params" : {"target" : {"mandatory" : False,
                                                  "help" : "The Moa target to execute."
                                                  }
                                      }
                          },

                 "DELETE" : {"requirements" : R_JOB|R_WRITE,
                             "help" : "Cleans up a Moa job.",
                             "params" : {}
                             }
                 },

    "title" : "Moa Job Status Information",
    "help" : "Represents the status of a Moa job."
    }




## moa-jobparams Command Entry ##

commands["moa-jobparams"]={
    "methods" : {"GET" : {"requirements" : R_JOB,
                          "help" : "Retrieves the values of all parameters.",
                          "params" : {}
                          },

                 "POST" : {"requirements" : R_JOB|R_WRITE,
                           "help" : "Sets the value of a single parameter. The value should be sent as the request body.",
                           "params" : {"key" : {"mandatory" : True,
                                                "help" : "\
The key associated with the parameter."
                                                }
                                       }
                           },

                 "PUT" : {"requirements" : R_JOB|R_WRITE,
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
    "methods" : {"GET" : {"requirements" : R_JOB,
                          "help" : "An alias for \"moa-jobinfo\".",
                          "params" : {}
                          },

                 "PUT" : {"requirements" : R_DIR|R_WRITE,
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

                 "DELETE" : {"requirements" : R_JOB|R_WRITE,
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
    "methods" : {"GET" : {"requirements" : R_DIR,
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




## s Command Entry ##

commands["s"]={
    "methods" : {"GET" : {"help" : "\
Retrieves information about how to access a representation \
of the item.",
                          "params" : {}
                          },
                 "PUT" : {"requirements" : R_FILE|R_WRITE,
                          "help" : "\
Updates the contents of a file.  The contents of \
the file should be included in the request body.",
                          "params" : {"multipart" : {"mandatory" : False, 
                                                     "help" : "\
A value that represents whether or not the contents \
of the request body should be interpreted as \
'multipart/form-data'. A value of '1' indicates that \
it should; any other value indicates that the contents \
of the file are included in the request body as is. \
The name of the field that holds the contents should be \
'file'."
                                                     }
                                      }
                          },
                 "POST" : {"requirements" : R_DIR|R_WRITE,
                           "help" : "\
Creates a new file or directory within the item.",
                           "params" : {"multipart" : {"mandatory" : False,
                                                      "help" : "\
Please see the help for the 'multipart' parameter \
for the 'PUT' method."
                                                      },
                                       "name" : {"mandatory" : True,
                                                 "help" : "\
The name of the file or directory to create.  If a \
file or directory with the same name already exists, \
an error occurs. The name cannot be a pathname that points \
to a location outside the current item, or to a location \
within one of the item's children."
                                                 },
                                       "directory" : {"mandatory" : False,
                                                      "help" : "\
A value that represents whether or not the new item should \
be a directory. A value of '1' indicates that it should be; \
any other value indicates that the item should be a file."
                                                      }
                                       }
                           },
                 "DELETE" : {"help" : "\
Deletes the item.  If the item is a directory, all of \
the directories contents are also deleted.",
                             "params" : {}
                             }
                 },
    "title" : "File System Item",
    "help" : "Represents a file system item."
    }



## preview Command Entry ##

commands["preview"]={
    "methods" : {"GET" : {"requirements" : R_FILE,
                          "help" : "Retrieves a preview of a file.",
                          "params" : {"offset" : {"mandatory" : False,
                                                  "help" : "\
The index of the first byte of the piece of the file \
to create the preview from. Default value is 0."
                                                  },
                                      "size" : {"mandatory" : False,
                                                "help" : "\
The size (in bytes) of the piece of the file to create \
the preview from.  If this value is larger than the \
number of available bytes, the piece's length will be \
smaller. Cannot exceed 64 KiB. Default value is 1 KiB. \
Note that the piece's size is not nessesarily the same \
as the size of the preview that is created."
                                                }
                                      }
                          }
                 },

    "title" : "Preview of a File",
    "help" : "Represents a textual preview of a file.  The preview will \
not nessesarily be an exact copy of the file."
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
