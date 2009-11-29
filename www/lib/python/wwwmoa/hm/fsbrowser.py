### WWWMoa ###############################
### HM_FSBrowser


## Imports ##

from wwwmoa.formats.html import error
from wwwmoa.formats import js
from wwwmoa import rw
from wwwmoa import rl
from wwwmoa import env



## Helper Functions ##

## Outputs a standardized error message.
def output_error(err):
    error.throw_fatal_error("File Browser Error", err)

## Main Entry Point ##
def run(args, env):
    if args==None:
        output_error("An unexpected error has occurred.")
    
    if len(args)<1: # if we were not handed a starting directory
        requested_path="" # use root
    else: # if we were handed a starting directory
        requested_path=args[0] # use it

    rw.send_header("Content-Type", "text/javascript")
    rw.send_header("Cache-Control", "no-cache")
    rw.send_header("Expires", "0")
    rw.end_header_mode()

    rw.send("""

/*** FSBrowser Helper Module ***/

return { // our code will return an object


    // Implementation for receiving contact messages.  This function
    // is nessesary for directory changing.
    doContactAction : function(data)
    {
        var path;
        var a=this;

        if(this.ls_response==null) // if we do not have a response from api call
            return; // we cannot do anything, so exit

        if(data.substr(0,3)==\"rtx\") // if the message sent requested a change to the root directory
            path=\"\"; // use a blank string for the path
        else if(data.substr(0,3)==\"tog\") // if the message sent requested that the files should be shown or hidden
        {
            this.showFiles=!this.showFiles; // toggle the visibility flag
            this.refreshVisualElement(); // refresh the view
            return; // we are done with fulfilling the request
        }
        else if(data.substr(0,4)==\"par-\") // if the message sent requested a parent directory
            path=this.ls_response[\"dir\"][new Number(data.substr(4))][\"path\"]; // retrieve the pathname associated with the parent directory
        else if(data.substr(0,4)==\"itm-\") // if the message sent requested an item in the current directory
            path=this.ls_response[\"ls\"][new Number(data.substr(4))][\"path\"]; // retrieve the pathname associated with the item
        else // if the message has not yet been recognized
            return; // we should just exit

        // start an AJAX request to retrieve a file listing
        wwwmoa.ajax.get(wwwmoa.rl.get_api(\"ls\", path),function(data)
                                                        {
                                                            a.dataCallback.call(a, data); // use the callback function of this object
                                                        } , 8192);
    },

    // Implementation for receiving startup event.
    doIniAction : function()
    {
        this.visualCodeMain=null; // initially, the main visual code will not yet have been created
        this.visualCodeFiles=null; // initially, the visual code for showing files will not yet 
                                   // have been created
        this.showFiles=true; // we will show current directory items by default
        var a=this;

        wwwmoa.ajax.get(\"""" + js.fix_text(rl.get_api("ls", requested_path)) + """\",function(data)
                                                                                      {
                                                                                          a.dataCallback.call(a, data); // use the callback function of this object
                                                                                      } , 8192);
    },

    // Implementation for receiving visual element change.
    doSetVisualElementAction : function(oldid)
    {
        this.refreshVisualElement(); // refresh the visual display to populate the new visual element
    },

    // Takes the previously generated HTML and packages it for viewing.  Then,
    // it pushes the HTML code into the visual element so that it is visible.
    refreshVisualElement : function()
    {
        if(this.getVisualElement()==null) // if we do not have a visual element
            return; // there is no reason to proceed

        if((this.visualCodeMain==null)||(this.visualCodeFiles==null)) // if either the main code or the current directory item code is not present
        {
            this.getVisualElement().innerHTML=\"Loading directory contents...<br>One moment...\"; // create loading message
        }
        else // if both the main code and the current directory item code is present
        {
            if(this.showFiles) // if files should be shown
                this.getVisualElement().innerHTML=\"<table><tr style=\\\"font-size:10pt; font-weight:bold; color:#0000FF; cursor:pointer\\\"><td colspan=\\\"2\\\" style=\\\"text-align:right; padding-right:4px\\\"><span onclick=\\\"wwwmoa.hm.contact(\" + this.getHMId() + \", 'tog');\\\" style=\\\"text-decoration:underline\\\">&lt;&lt; Hide Files</span></td></tr><tr><td style=\\\"vertical-align:top; padding-right:4px\\\">"+this.visualCodeMain+"</td><td style=\\\"padding-left:4px; border-left:1px solid #A0A0A0; vertical-align:top\\\">"+(this.visualCodeFiles!="" ? this.visualCodeFiles : "<span style=\\\"color:#A0A0A0; font-weight:normal; font-style:italic\\\">(No files present.)</span>")+"</td></tr></table>"; // package both pieces of code
            else // if only parent directories should be shown
                this.getVisualElement().innerHTML=\"<table><tr style=\\\"font-size:10pt; font-weight:bold; color:#0000FF; cursor:pointer\\\"><td colspan=\\\"2\\\" style=\\\"text-align:left\\\"><span onclick=\\\"wwwmoa.hm.contact(\" + this.getHMId() + \", 'tog');\\\" style=\\\"text-decoration:underline\\\">&gt;&gt; Show Files</span></td></tr><tr><td>"+this.visualCodeMain+"</td></tr></table>"; // package only the main piece of code



        }
    },

    // Receives data from the API request.  Then, it creates the HTML code that
    // will be used to display the directory contents.  Finally, it request an
    // update of the visual element.
    dataCallback : function(data) {
        var ls_response=wwwmoa.json.parse(data); // attempt a parse of the received data

        var buf_main_code=\"\"; // buffer for \"main code\" (code for directories)
        var buf_file_code=\"\"; // buffer for \"file code\" (code for files)
        var tmp_shared_code=\"\"; // temporary storage for \"shared code\" (code that could be placed in either \"main\" or \"file\" code)

        var is_dir=false; // holds whether the currently processed item is a directory or not
        var levels=1; // holds the number of parent directory levels (always at least one: the root)
        var files_exist=false;  // holds whether or not the current directory has any items

        this.ls_response=ls_response; // save the parsed response we have received for later use

        if(data==null) // if null was passed, we have an error
        {
            this.visualCodeMain=\"Sorry, but the directory contents could not be loaded.\"; // create an error message
            this.visualCodeFiles=\"\";
            this.refreshVisualElement(); // display the error message
        }


        // create code for root directory
        buf_main_code+=\"<img src=\\\"""" + js.fix_text(rl.get_image("FSdiroprtA")) + """\\\" alt=\\\"Directory\\\">\";
        buf_main_code+=\" \";
        buf_main_code+=\"<span style=\\\"font-weight:bold; color:#0000FF; text-decoration:underline; cursor:pointer\\\" onclick=\\\"wwwmoa.hm.contact(\" + this.\
getHMId() + \", 'rtx');\\\">\"
        buf_main_code+=wwwmoa.html.fix_text(\"[Root]\");
        buf_main_code+=\"</span><br><div style=\\\"padding-left:30px\\\">\"; // start first indentation




        for(var x=0; x<ls_response[\"dir\"].length; x++) // for each parent directory
        {
            levels++; // we have a new level

            // create code for level
            buf_main_code+=\"<img src=\\\"""" + js.fix_text(rl.get_image("FSdiropA")) + """\\\" alt=\\\"Directory\\\">\";
            buf_main_code+=\" \";
            buf_main_code+=\"<span style=\\\"font-weight:bold; color:#0000FF; text-decoration:underline; cursor:pointer\\\" onclick=\\\"wwwmoa.hm.contact(\" + this.getHMId() + \", 'par-\" + x + \"');\\\">\"
            buf_main_code+=wwwmoa.html.fix_text(ls_response[\"dir\"][x][\"name\"]);
            buf_main_code+=\"</span><br><div style=\\\"padding-left:30px\\\">\"; // do indentation
        }

        // start structural tables
        buf_main_code+=\"<table>\";
        buf_file_code+=\"<table>\";


        for(var x=0; x<ls_response[\"ls\"].length; x++) // for each item in the current directory
        {
            is_dir=(ls_response[\"ls\"][x][\"type\"]==\"dir\"); // find whether the item is a dir or not

            files_exist|=!is_dir; // if this item is a file, remember that we have encountered files

            if(!is_dir) // if the item is a file
            {
                // create code for start of entry for a file
                buf_file_code+=\"<tr><td>\";
                buf_file_code+=\"<img src=\\\"""" + js.fix_text(rl.get_image("FSfileA")) + """\\\" alt=\\\"File\\\"> \";
                buf_file_code+=\"<span style=\\\"font-weight:bold; color:#0000FF; text-decoration:underline; cursor:pointer\\\" \";
            }
            else // if the item is a directory
            {
                // create code for start of entry for a directory
                buf_main_code+=\"<tr><td>\";
                buf_main_code+=\"<img src=\\\"""" + js.fix_text(rl.get_image("FSdirclA")) + """\\\" alt=\\\"Directory\\\"> \";
                buf_main_code+=\"<span style=\\\"font-weight:bold; color:#0000FF; text-decoration:underline; cursor:pointer\\\" \";
            }

            if(ls_response[\"ls\"][x][\"read-allowed\"]) // if reading the item is allowed
                if(is_dir) // if the item is a directory
                    buf_main_code+=\"onclick=\\\"wwwmoa.hm.contact(\" + this.getHMId() + \", 'itm-\" + x + \"');\\\">\"; // add code to allow for directory changing
                else // if the item is a file
                    buf_file_code+=\"onclick=\\\"wwwmoa.ui.alert('Sorry, but you cannot view a listing for a file.');\\\">\"; // add code to alert user about the fact that they cannot list a file
            else // if reading the item is not allowed
                if(is_dir) // if the item is a directory
                    buf_main_code+=\"onclick=\\\"wwwmoa.ui.alert('Sorry, but you cannot view the listing for this directory, because you do not have permission to do so.');\\\">\"; // add code to alert user that the directory cannot be read
                else // if the item is a file
                    buf_file_code+=\"onclick=\\\"wwwmoa.ui.alert('Sorry, but you cannot select this file, because you do not have permission to do so.');\\\">\"; // add code to alert user that the file cannot be read



            // start creating basic entry code (which is the same for files and directories)

            tmp_shared_code=wwwmoa.html.fix_text(ls_response[\"ls\"][x][\"name\"]); // add the name of the file
            tmp_shared_code+=\"</span>\";

            tmp_shared_code+=\"</td><td>\";

            if(ls_response[\"ls\"][x][\"size\"]>=0) // if the size has a meaning
                tmp_shared_code+=ls_response[\"ls\"][x][\"size\"] + " b"; // add the size

            tmp_shared_code+=\"</td><td>\";

            if(ls_response[\"ls\"][x][\"link\"]) // if the item is a link
                tmp_shared_code+=\"<img src=\\\"""" + js.fix_text(rl.get_image("FSlinkA")) + """\\\" alt=\\\"Link\\\" title=\\\"This item is actually a link.\\\">\"; // give it the proper annotation

            tmp_shared_code+=\"</td><td>\";

            if(ls_response[\"ls\"][x][\"read-allowed\"]) // if the item can be read
                tmp_shared_code+=\"<img src=\\\"""" + js.fix_text(rl.get_image("FScreadA")) + """\\\" alt=\\\"Read Allowed\\\" title=\\\"Reading this item is allowed.\\\"> \"; // give it the proper annotation
            else // if the item cannot be read
                tmp_shared_code+=\"<img src=\\\"""" + js.fix_text(rl.get_image("FScnreadA")) + """\\\" alt=\\\"Read Not Allowed\\\" title=\\\"Reading this item is not allowed.\\\"> \"; // give it proper annotation


            if(ls_response[\"ls\"][x][\"write-allowed\"]) // if the item can be written
                tmp_shared_code+=\"<img src=\\\"""" + js.fix_text(rl.get_image("FScwriteA")) + """\\\" alt=\\\"Write Allowed\\\" title=\\\"Writing this item is allowed.\\\">\"; // give it proper annotation
            else // if the item cannot be written
                tmp_shared_code+=\"<img src=\\\"""" + js.fix_text(rl.get_image("FScnwriteA")) + """\\\" alt=\\\"Write Not Allowed\\\" title=\\\"Writing this item is not allowed.\\\">\"; // give it proper annoation


            tmp_shared_code+=\"</td></tr>\";

            // decide where code we just created should be stashed

            if(is_dir) // if the item is a directory
                buf_main_code+=tmp_shared_code; // stash the code in the \"main\" buffer
            else // otherwise 
                buf_file_code+=tmp_shared_code; // stash the code in the \"file\" buffer
        }

        // end both structural tables
        buf_main_code+=\"</table>\";
        buf_file_code+=\"</table>\";

        while(levels>0) // for each level opened in \"main\" buffer
        {
            levels--; // remember that we have closed an indentation

            buf_main_code+=\"</div>\"; // close an indentation
        }

        this.visualCodeMain=buf_main_code; // make main code \"public\"
        this.visualCodeFiles=(files_exist ? buf_file_code : \"\"); // make file code \"public\"

        this.refreshVisualElement(); // refresh the main visual element
        
    }
};


""")
