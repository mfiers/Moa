### WWWMoa ###############################
### HM_FSBrowser


## Imports ##
import WWWMoaHTMLError
import WWWMoaJS
import WWWMoaRW
import WWWMoaRL
import WWWMoaEnv


## Helper Functions ##

## Outputs a standardized error message.
def output_error(err):
    WWWMoaHTMLError.throw_fatal_error("File Browser Error", err)

## Main Entry Point ##
def run(args, env):
    if args==None:
        output_error("An unexpected error has occurred.")
    
    if len(args)<1: # if we were not handed a starting directory
        requested_path="" # use root
    else: # if we were handed a starting directory
        requested_path=args[0] # use it

    WWWMoaRW.send_header("Content-Type", "text/javascript")
    WWWMoaRW.send_header("Cache-Control", "no-cache")
    WWWMoaRW.send_header("Expires", "0")
    WWWMoaRW.end_header_mode()

    WWWMoaRW.send("""

/*** FSBrowser Helper Module ***************************
* This script was generated on the fly and is designed *
* to be used with the wwwmoa.hm library.               *
*******************************************************/

return { // our code will return an object


    doContactAction : function(data)
    {
        var path;
        var a=this;

        if(this.ls_response==null)
            return;

        if(data.substr(0,3)==\"rtx\")
            path=\"\";
        else if(data.substr(0,3)==\"tog\")
        {
            this.showFiles=!this.showFiles;
            this.refreshVisualElement();
            return;
        }
        else if(data.substr(0,4)==\"par-\")
            path=this.ls_response[\"dir\"][new Number(data.substr(4))][\"path\"];
        else if(data.substr(0,4)==\"itm-\")
            path=this.ls_response[\"ls\"][new Number(data.substr(4))][\"path\"];
        else
            return;

        wwwmoa.ajax.get(wwwmoa.rl.get_api(\"ls\", path),function(data) { a.dataCallback.call(a, data); } , 8192);
    },

    doIniAction : function()
    {
        this.visualCodeMain=null;
        this.visualCodeFiles=null;
        this.showFiles=true;
        var a=this;

        wwwmoa.ajax.get(\"""" + WWWMoaJS.fix_text(WWWMoaRL.get_api("ls", requested_path)) + """\",function(data) { a.dataCallback.call(a, data); } , 8192);
    },

    doSetVisualElementAction : function(oldid)
    {
        this.refreshVisualElement();
    },

    refreshVisualElement : function()
    {
        if(this.getVisualElement()==null)
            return;

        if((this.visualCodeMain==null)||(this.visualCodeFiles==null))
        {
            this.getVisualElement().innerHTML=\"Loading directory contents...<br>One moment...\";
        }
        else
        {
            if(this.showFiles)
                this.getVisualElement().innerHTML=\"<table><tr style=\\\"font-size:10pt; font-weight:bold; color:#0000FF; cursor:pointer\\\"><td colspan=\\\"2\\\" style=\\\"text-align:right; padding-right:4px\\\"><span onclick=\\\"wwwmoa.hm.contact(\" + this.getHMId() + \", 'tog');\\\" style=\\\"text-decoration:underline\\\">&lt;&lt; Hide Files</span></td></tr><tr><td style=\\\"vertical-align:top; padding-right:4px\\\">"+this.visualCodeMain+"</td><td style=\\\"padding-left:4px; border-left:1px solid #A0A0A0; vertical-align:top\\\">"+(this.visualCodeFiles!="" ? this.visualCodeFiles : "<span style=\\\"color:#A0A0A0; font-weight:normal; font-style:italic\\\">(No files present.)</span>")+"</td></tr></table>";
            else
                this.getVisualElement().innerHTML=\"<table><tr style=\\\"font-size:10pt; font-weight:bold; color:#0000FF; cursor:pointer\\\"><td colspan=\\\"2\\\" style=\\\"text-align:left\\\"><span onclick=\\\"wwwmoa.hm.contact(\" + this.getHMId() + \", 'tog');\\\" style=\\\"text-decoration:underline\\\">&gt;&gt; Show Files</span></td></tr><tr><td>"+this.visualCodeMain+"</td></tr></table>";



        }
    },

    dataCallback : function(data) {
        var ls_response=wwwmoa.json.parse(data);
        var tmpvc=\"\";
        var tmpvc2=\"\";
        var tmpvc3=\"\";
        var is_dir=false;
        var levels=1;
        var files_exist=false;
        this.ls_response=ls_response;

        if(data==null)
        {
            this.visualCode=\"Sorry, but the directory contents could not be loaded.\";
            this.refreshVisualElement();
        }



        tmpvc+=\"<img src=\\\"""" + WWWMoaJS.fix_text(WWWMoaRL.get_image("FSdiroprtA")) + """\\\" alt=\\\"Directory\\\">\";
        tmpvc+=\" \";
        tmpvc+=\"<span style=\\\"font-weight:bold; color:#0000FF; text-decoration:underline; cursor:pointer\\\" onclick=\\\"wwwmoa.hm.contact(\" + this.\
getHMId() + \", 'rtx');\\\">\"
        tmpvc+=wwwmoa.html.fix_text(\"[Root]\");
        tmpvc+=\"</span><br><div style=\\\"padding-left:40px\\\">\";




        for(var x=0; x<ls_response[\"dir\"].length; x++)
        {
            levels++;

            tmpvc+=\"<img src=\\\"""" + WWWMoaJS.fix_text(WWWMoaRL.get_image("FSdiropA")) + """\\\" alt=\\\"Directory\\\">\";
            tmpvc+=\" \";
            tmpvc+=\"<span style=\\\"font-weight:bold; color:#0000FF; text-decoration:underline; cursor:pointer\\\" onclick=\\\"wwwmoa.hm.contact(\" + this.getHMId() + \", 'par-\" + x + \"');\\\">\"
            tmpvc+=wwwmoa.html.fix_text(ls_response[\"dir\"][x][\"name\"]);
            tmpvc+=\"</span><br><div style=\\\"padding-left:40px\\\">\";
        }

        tmpvc+=\"<table>\";
        tmpvc2+=\"<table>\";

        is_dir=false;

        for(var x=0; x<ls_response[\"ls\"].length; x++)
        {
            is_dir=(ls_response[\"ls\"][x][\"type\"]==\"dir\");

            files_exist|=!is_dir;

            if(!is_dir)
            {
                tmpvc2+=\"<tr><td>\";
                tmpvc2+=\"<img src=\\\"""" + WWWMoaJS.fix_text(WWWMoaRL.get_image("FSfileA")) + """\\\" alt=\\\"File\\\"> \";
                tmpvc2+=\"<span style=\\\"font-weight:bold; color:#0000FF; text-decoration:underline; cursor:pointer\\\" \";
            }
            else
            {
                tmpvc+=\"<tr><td>\";
                tmpvc+=\"<img src=\\\"""" + WWWMoaJS.fix_text(WWWMoaRL.get_image("FSdirclA")) + """\\\" alt=\\\"Directory\\\"> \";
                tmpvc+=\"<span style=\\\"font-weight:bold; color:#0000FF; text-decoration:underline; cursor:pointer\\\" \";
            }



            if(ls_response[\"ls\"][x][\"read-allowed\"])
                if(is_dir)
                    tmpvc+=\"onclick=\\\"wwwmoa.hm.contact(\" + this.getHMId() + \", 'itm-\" + x + \"');\\\">\";
                else
                    tmpvc2+=\"onclick=\\\"wwwmoa.ui.alert('Sorry, but you cannot view a listing for a file.');\\\">\";
            else
                if(is_dir)
                    tmpvc+=\"onclick=\\\"wwwmoa.ui.alert('Sorry, but you cannot view the listing for this directory, because you do not have permission to do so.');\\\">\";
                else
                    tmpvc2+=\"onclick=\\\"wwwmoa.ui.alert('Sorry, but you cannot select this file, because you do not have permission to do so.');\\\">\";



            
            tmpvc3=wwwmoa.html.fix_text(ls_response[\"ls\"][x][\"name\"]);
            tmpvc3+=\"</span>\";

            tmpvc3+=\"</td><td>\";

            if(ls_response[\"ls\"][x][\"size\"]>=0)
                tmpvc3+=ls_response[\"ls\"][x][\"size\"] + " b";

            tmpvc3+=\"</td><td>\";

            if(ls_response[\"ls\"][x][\"link\"])
                tmpvc3+=\"<img src=\\\"""" + WWWMoaJS.fix_text(WWWMoaRL.get_image("FSlinkA")) + """\\\" alt=\\\"Link\\\" title=\\\"This item is actually a link.\\\">\";

            tmpvc3+=\"</td><td>\";

            if(ls_response[\"ls\"][x][\"read-allowed\"])
                tmpvc3+=\"<img src=\\\"""" + WWWMoaJS.fix_text(WWWMoaRL.get_image("FScreadA")) + """\\\" alt=\\\"Read Allowed\\\" title=\\\"Reading this item is allowed.\\\"> \";
            else
                tmpvc3+=\"<img src=\\\"""" + WWWMoaJS.fix_text(WWWMoaRL.get_image("FScnreadA")) + """\\\" alt=\\\"Read Not Allowed\\\" title=\\\"Reading this item is not allowed.\\\"> \";


            if(ls_response[\"ls\"][x][\"write-allowed\"])
                tmpvc3+=\"<img src=\\\"""" + WWWMoaJS.fix_text(WWWMoaRL.get_image("FScwriteA")) + """\\\" alt=\\\"Write Allowed\\\" title=\\\"Writing this item is allowed.\\\">\";
            else
                tmpvc3+=\"<img src=\\\"""" + WWWMoaJS.fix_text(WWWMoaRL.get_image("FScnwriteA")) + """\\\" alt=\\\"Write Not Allowed\\\" title=\\\"Writing this item is not allowed.\\\">\";


            tmpvc3+=\"</td></tr>\";

            if(is_dir)
                tmpvc+=tmpvc3;
            else
                tmpvc2+=tmpvc3;
        }

        tmpvc+=\"</table>\";
        tmpvc2+=\"</table>\";

        while(levels>0)
        {
            levels--;

            tmpvc+=\"</div>\";
        }

        this.visualCodeMain=tmpvc;
        this.visualCodeFiles=(files_exist ? tmpvc2 : "");

        this.refreshVisualElement();
        
    }
};


""")
