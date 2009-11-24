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
        this.visualCode=null;
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

        if(this.visualCode==null)
        {
            this.getVisualElement().innerHTML=\"Loading directory contents...<br>One moment...\";
        }
        else
        {
            this.getVisualElement().innerHTML=this.visualCode;
        }
    },

    dataCallback : function(data) {
        var ls_response=wwwmoa.json.parse(data);
        var tmpvc=\"\";
        var levels=1;
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

        for(var x=0; x<ls_response[\"ls\"].length; x++)
        {
            tmpvc+=\"<tr><td>\";

            if(ls_response[\"ls\"][x][\"type\"]==\"file\")
                tmpvc+=\"<img src=\\\"""" + WWWMoaJS.fix_text(WWWMoaRL.get_image("FSfileA")) + """\\\" alt=\\\"File\\\">\";
            else
                tmpvc+=\"<img src=\\\"""" + WWWMoaJS.fix_text(WWWMoaRL.get_image("FSdirclA")) + """\\\" alt=\\\"Directory\\\">\";

            tmpvc+=\" \";

            tmpvc+=\"<span style=\\\"font-weight:bold; color:#0000FF; text-decoration:underline; cursor:pointer\\\" \";

            if(ls_response[\"ls\"][x][\"read-allowed\"])
                tmpvc+=\"onclick=\\\"wwwmoa.hm.contact(\" + this.getHMId() + \", 'itm-\" + x + \"');\\\">\";
            else
                tmpvc+=\"onclick=\\\"wwwmoa.ui.alert('Sorry, but you do not have permission to list the directory you have selected.');\\\">\";


            tmpvc+=wwwmoa.html.fix_text(ls_response[\"ls\"][x][\"name\"]);
            tmpvc+=\"</span>\";

            tmpvc+=\"</td><td>\";

            if(ls_response[\"ls\"][x][\"size\"]>=0)
                tmpvc+=ls_response[\"ls\"][x][\"size\"] + " b";

            tmpvc+=\"</td><td>\";

            if(ls_response[\"ls\"][x][\"link\"])
                tmpvc+=\"<img src=\\\"""" + WWWMoaJS.fix_text(WWWMoaRL.get_image("FSlinkA")) + """\\\" alt=\\\"Link\\\" title=\\\"This item is actually a link.\\\">\";

            tmpvc+=\"</td><td>\";

            if(ls_response[\"ls\"][x][\"read-allowed\"])
                tmpvc+=\"<img src=\\\"""" + WWWMoaJS.fix_text(WWWMoaRL.get_image("FScreadA")) + """\\\" alt=\\\"Read Allowed\\\" title=\\\"Reading this item is allowed.\\\"> \";
            else
                tmpvc+=\"<img src=\\\"""" + WWWMoaJS.fix_text(WWWMoaRL.get_image("FScnreadA")) + """\\\" alt=\\\"Read Not Allowed\\\" title=\\\"Reading this item is not allowed.\\\"> \";


            if(ls_response[\"ls\"][x][\"write-allowed\"])
                tmpvc+=\"<img src=\\\"""" + WWWMoaJS.fix_text(WWWMoaRL.get_image("FScwriteA")) + """\\\" alt=\\\"Write Allowed\\\" title=\\\"Writing this item is allowed.\\\">\";
            else
                tmpvc+=\"<img src=\\\"""" + WWWMoaJS.fix_text(WWWMoaRL.get_image("FScnwriteA")) + """\\\" alt=\\\"Write Not Allowed\\\" title=\\\"Writing this item is not allowed.\\\">\";


            tmpvc+=\"</td></tr>\";
        }

        tmpvc+=\"</table>\";

        while(levels>0)
        {
            levels--;

            tmpvc+=\"</div>\";
        }

        this.visualCode=tmpvc;

        this.refreshVisualElement();
        
    }
};


""")
