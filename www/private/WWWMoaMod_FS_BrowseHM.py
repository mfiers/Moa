### WWWMoa ###############################
### Mod_FS_BrowseHM


## Imports ##
import WWWMoaHTMLEngine
import WWWMoaHTML
import WWWMoaHTMLError
import WWWMoaJS
import WWWMoaRW
import WWWMoaRL
import WWWMoaEnv
import os
import os.path

from WWWMoaMod_FS import in_root
from WWWMoaMod_FS import is_root

## Helper Functions ##

## Outputs a standardized error message.
def output_error(err):
    WWWMoaHTMLError.throw_fatal_error("File Browser Error", err)

## Main Entry Point ##
def run_fs(argd):
    if argd==None:
        output_error("An unexpected error has occurred.")
    
    # [!] Note: Security checks should have been done already to make sure path is valid and available to the user. Often, this module is used by WWWMoaMod_FS, which does do those security checks.

    # find what directories and files are in the requested directory
    filelist=os.listdir(argd["path"])

    filelist.sort() # sort in alpha order (ascending)

    # prepare buffers
    file_buffer="" # will hold the HTML code corresponding to files
    dir_buffer="" # will hold the HTML code corresponding to directories
    c_buffer="" # will hold some of the HTML code for a small part of the processing
    o_buffer="" # will hold the entire HTML code, after being JS escaped

    for f in filelist: # for each file or directory
        f_joined=os.path.join(argd["path"],f) # get the absolute path of the item
        f_real=os.path.realpath(f_joined) # get the actual path of the item (remove symb linking)
        f_real=os.path.normpath(f_real) # normalize the path, to make it as simple as possible


        # [!] Security Note: The following code outputs an alert if the item cannot be accessed for security reasons.  However, the code above checks this again on the server side, so this does not create a security hole.

        if in_root(f_real): # if the item is in the psuedo-root directory
            c_buffer=WWWMoaJS.fix_text("<a href=\"#"+WWWMoaHTML.fix_text(WWWMoaRL.url_encode(WWWMoaHTMLEngine.get_unique_id()))+"\" onclick=\"wwwmoa.hm.contact(")
            c_buffer+="\" + this.getHMId() + \""
            c_buffer+=", " + WWWMoaJS.fix_text("'"+WWWMoaRL.get_fs_command(os.path.relpath(f_real,argd["content_path"]), "browsehm")+"');\">") # start a normal hyperlink to it
        else: # if the item is not in the psuedo-root directory
            c_buffer=WWWMoaJS.fix_text(WWWMoaHTML.get_tag_open("a", {"href" : "#"+WWWMoaRL.url_encode(WWWMoaHTMLEngine.get_unique_id()), "onclick" : "alert(\"The directory or file you are attempting to access cannot be accessed by you.\")"})) # output a link to an alert

        # finish off link and get ready for item attributes
        c_buffer+=WWWMoaJS.fix_text(WWWMoaHTML.translate_text(f)+WWWMoaHTML.get_tag_close("a")+WWWMoaHTML.get_simple_tag_close("td")+WWWMoaHTML.get_tag_open("td",{"style" : "padding:1px 2px 1px 8px"}))

        # create next attribute
        if os.path.islink(f_joined): # if the item is actually a link
            c_buffer+="Link" # tell the user this
        else: # if the item is not a link
            pass # do not output anything

        # get ready for next item attribute
        c_buffer+=WWWMoaJS.fix_text(WWWMoaHTML.get_simple_tag_close("td")+WWWMoaHTML.get_tag_open("td", {"style" : "padding:1px 8px 1px 8px"}))

        # create next attribute
        if os.path.isfile(f_joined): # if the item is a file
            c_buffer+=WWWMoaJS.fix_text(WWWMoaHTML.translate_text(str(os.path.getsize(f_joined))+" b")) # output its size (in bytes)
        else: # if the item is not a file
            pass # do not output anything

        # end item entry
        c_buffer+=WWWMoaJS.fix_text(WWWMoaHTML.get_simple_tag_close("td"))
        c_buffer+=WWWMoaJS.fix_text(WWWMoaHTML.get_simple_tag_close("tr")+"\n")

        # [!] Logic Note: c_buffer does not contain the first part of the HTML code for the item entry, as this depends on whether it is a directory or a file.

        # finish up item entry code and output it to the correct buffer

        if os.path.isdir(f_joined): # if the item is a directory
            dir_buffer+=WWWMoaJS.fix_text(WWWMoaHTML.get_simple_tag_open("tr")+WWWMoaHTML.get_tag_open("td",{"style" : "font-weight:bold"})+WWWMoaHTML.get_tag("img", {"src" : WWWMoaRL.get_image("FSdirclA"), "alt" : "Directory"})+" ")+c_buffer # output a piece of code with the directory icon, and the contents of c_buffer

        if os.path.isfile(f_joined): # if the item is a file
            file_buffer+=WWWMoaJS.fix_text(WWWMoaHTML.get_simple_tag_open("tr")+WWWMoaHTML.get_tag_open("td",{"style" : "font-weight:bold"})+WWWMoaHTML.get_tag("img", {"src" : WWWMoaRL.get_image("FSfileA"), "alt" : "File"})+" ")+c_buffer # output a piece of code with the file icon, and the contents of c_buffer


    # output HTML code for root directory (this will always exist)
    o_buffer+=WWWMoaJS.fix_text(WWWMoaHTML.get_tag("img", {"src" : WWWMoaRL.get_image("FSdiroprtA"), "alt" : "Directory"})) # root directory icon
    o_buffer+=" "
    o_buffer+=WWWMoaJS.fix_text("<a style=\"font-weight:bold;\" href=\"#" + WWWMoaHTML.fix_text(WWWMoaRL.url_encode(WWWMoaHTMLEngine.get_unique_id())))
    o_buffer+=WWWMoaJS.fix_text("\" onclick=\"wwwmoa.hm.contact(")
    o_buffer+= "\" + this.getHMId() + \""
    o_buffer+=", " + WWWMoaJS.fix_text("'"+WWWMoaRL.get_fs_command("/", "browsehm")+"');\">") # start a normal hyperlink to it
    o_buffer+="[Root]"
    o_buffer+=WWWMoaJS.fix_text(WWWMoaHTML.get_tag_close("a"))


    # [!] Logic Note: At this point, we will switch gears and begin constructing the code for the directory hierarchy.

    hierarchypath=argd["rel_path"] # at the beginning, we will work with the entire requested path
    hierarchypath_complete=argd["path"] # at the beginning, we will work with the entire requested path
    hierarchy_count=0 # so far, we have not encountered any nested sub-directories
    hierarchy_buff="" # we will put HTML code for hierarchy in this buffer

    while not is_root(hierarchypath_complete): # while we have not made our way back to the pseudo-root directory yet
        hierarchy_count=hierarchy_count+1 # there is a nest level between the current path and the pseudo-root

        singledirbuff="" # this will hold the HTML code for one nest level

        # [!] Logic Note: The next few lines of code are a little extra complicated to ensure that trailing slashes are trimmed off.

        # attempt splitting of current path
        (hierarchypath_h, hierarchypath_t)=os.path.split(hierarchypath) # split the path the user will see
        (hierarchypath_complete_h, hierarchypath_complete_t)=os.path.split(hierarchypath_complete) # split the path we will use
    
        if hierarchypath_t=="": # if the tail is empty, it means that a trailing slash existed
            (hierarchypath_h,hierarchypath_t)=os.path.split(hierarchypath_h) # the trailing slash is gauranteed to have been removed, so splitting again should do the trick

        if hierarchypath_complete_t=="": # if the tail is empty, it means that a trailing slash existed
            (hierarchypath_complete_h, hierarchypath_complete_t)=os.path.split(hierarchypath_complete_h) # the trailing slash is gauranteed to have been removed, so spliting again should do the trick

        # generate HTML code for this nest level
        singledirbuff+=WWWMoaJS.fix_text(WWWMoaHTML.get_tag_open("div", {"style" : "padding-left:24px"})) # we will ensure that this is matches in a little while
        singledirbuff+=WWWMoaJS.fix_text(WWWMoaHTML.get_tag("img", {"src" : WWWMoaRL.get_image("FSdiropA"), "alt" : "Current Directory"}))
        singledirbuff+=" "
        singledirbuff+=WWWMoaJS.fix_text(WWWMoaHTML.get_tag_open("span", {"style" : "font-weight:bold"}))
        singledirbuff+=WWWMoaJS.fix_text("<a href=\"#"+WWWMoaRL.url_encode(WWWMoaHTMLEngine.get_unique_id())+"\" onclick=\"wwwmoa.hm.contact(")
        singledirbuff+="\" + this.getHMId() + \""
        singledirbuff+=", " + WWWMoaJS.fix_text("'"+WWWMoaRL.get_fs_command(os.path.relpath(hierarchypath_complete,argd["content_path"]), "browsehm")+"');\">") # start a normal hyperlink to it
        singledirbuff+=WWWMoaJS.fix_text(WWWMoaHTML.translate_text(hierarchypath_t))
        singledirbuff+=WWWMoaJS.fix_text(WWWMoaHTML.get_tag_close("a"))
        singledirbuff+=WWWMoaJS.fix_text(WWWMoaHTML.get_tag_close("span"))
        singledirbuff+=WWWMoaJS.fix_text(WWWMoaHTML.get_linefeed_tag())

        hierarchy_buff=singledirbuff+hierarchy_buff # add to main buffer
        hierarchypath=hierarchypath_h # we will now work on the fragment of the path that is left
        hierarchypath_complete=hierarchypath_complete_h # we will now work on the fragment of the path that is left

    # buffer the rest of the HTML document
    c_buffer=hierarchy_buff # send the buffer we just generated
    c_buffer+=WWWMoaJS.fix_text(WWWMoaHTML.get_tag_open("div", {"style" : "padding-left:24px"})) # add an additional level for the contents of the directory to be placed in
    c_buffer+=WWWMoaJS.fix_text(WWWMoaHTML.get_simple_tag_open("table"))
    c_buffer+=dir_buffer # place directory code
    c_buffer+=file_buffer # place file code
    c_buffer+=WWWMoaJS.fix_text(WWWMoaHTML.get_simple_tag_close("table"))
    c_buffer+=WWWMoaJS.fix_text(WWWMoaHTML.get_tag_close("div")) # close additional level
    o_buffer+=c_buffer

    # match nest levels
    while hierarchy_count>0: # while we still have nest levels open
        hierarchy_count=hierarchy_count-1 # say that we have matched a level
        o_buffer+=WWWMoaJS.fix_text(WWWMoaHTML.get_tag_close("div")) # match a level
        o_buffer+="\\n"

    WWWMoaRW.send_header("Content-Type", "text/javascript")
    WWWMoaRW.send_header("Cache-Control", "no-cache")
    WWWMoaRW.send_header("Expires", "0")
    WWWMoaRW.end_header_mode()

    WWWMoaRW.send("""/* RESPONSE FOR DIRECTORY REQUEST */

return {
    doAction : function(data)
    {
        wwwmoa.hm.unlink(this.getHMId());
        var a=this;

        wwwmoa.hm.create(data, function(obj)
            {
                 obj.setVisualElement(a.getVisualElement())
            });
    },

    doSetVisualElementAction : function(oldid)
    {
        this.getVisualElement().innerHTML=\"""" + o_buffer + """\";
    }
};


""")
