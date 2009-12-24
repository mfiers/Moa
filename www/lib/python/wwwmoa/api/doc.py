## Imports ##

import wwwmoa.api.reg as apireg
import wwwmoa.formats.html as html




## Constants ##

FORMAT_TEXT=0
FORMAT_HTML=1




## Main Logic ##

def getCommandDoc(command, format=FORMAT_TEXT):
    helper=_FormatHelper(format)

    try:
        command_help=apireg.getCommandHelp(command)
    except apireg.NotSupportedError:
        helper.addMajorHeading("Command Not Supported")
        helper.addText("The command you specified, "+command+", is not supported.")
        helper.setTitle("Doc Error")
        return helper.finish()

    helper.setTitle("API Doc - "+command)

    helper.addMajorHeading("Functionality")
    helper.addText(command_help)
    helper.addSectionSep()

    helper.addMajorHeading("Supported Methods")
    helper.addText("The "+command+" command may only be accessed using certain HTTP methods.  \
These methods are listed below, with details on how they can be used.")
    helper.addSectionSep()
    methods=apireg.getSupportedMethods(command)

    methods.sort()

    for m in methods:
        helper.addMinorHeading(m)
        helper.addText(apireg.getMethodHelp(command, m))
        helper.addSectionSep()
    
        parameters=apireg.getAcceptedParameters(command, m)

        for p in parameters:
            helper.addText(p + " - ")
            helper.addText(apireg.getParameterHelp(command, m, p))
            helper.addText("\n")

        helper.addSectionSep()

    return helper.finish()

def getCommandsDoc(format=FORMAT_TEXT):
    helper=_FormatHelper(format)

    commands=apireg.getSupportedCommands()

    helper.setTitle("API Doc")

    helper.addMajorHeading("Supported Commands")
    helper.addText("All of the supported commands are listed below.")
    helper.addSectionSep()

    commands.sort()

    for c in commands:
        helper.addMinorHeading(c)
        helper.addText(apireg.getCommandHelp(c))
        helper.addSectionSep()
        helper.addText(c+" supports the following methods: "+"; ".join(apireg.getSupportedMethods(c)))
        helper.addSectionSep()

    return helper.finish()





## Output Formatter ##

class _FormatHelper:
    def __init__(self, format):
        global FORMAT_HTML

        self._isHTML=(format==FORMAT_HTML)
        self._isFinished=False
        self._buff=""
        self._title=""
        self._indent=0

    def finish(self):
        if self._isFinished:
            return self._buff

        self._isFinished=True

        if not self._isHTML:
            self._buff="".ljust(len(self._title)+4, "#")+"\n# "+self._title+" #\n"+"".ljust(len(self._title)+4, "#")+"\n\n"+self._buff
        else:
            self._buff="""<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">

<html>

<head>

<title>""" + html.fix_text(self._title) + """</title>

<meta name=\"generator\" content=\"""" + html.fix_text(__name__) + """\">

</head>

<body style=\"background-color:#F8FFF8; color:#000000; font-family:arial, sans-serif; font-size:12pt\">

<div style=\"background-color:#FFFFFF; color:#000000; border:1px solid #004000; padding:8px\">

<div style=\"font-size:36pt; font-weight:bold; color:#008000\">""" + html.fix_text(self._title) + """</div>

""" + self._buff + """

</div>

</body>

</html>"""

        return self._buff


    def addText(self, text):
        if self._isHTML:
            self._addBuff(html.translate_text(text))
        else:
            self._addBuff(text)

    def addMajorHeading(self, text):
        if self._isHTML:
            self._addBuff("<span style=\"font-weight:bold; font-size:20pt; text-decoration:underline\">")
            self.addText(text)
            self._addBuff("</span><br>")
        else:
            self._addBuff(text + "\n" + "".rjust(len(text)+6, "=") + "\n")


    def addMinorHeading(self, text):
        if self._isHTML:
            self._addBuff("<span style=\"font-weight:bold; font-size:14pt\">")
            self.addText(text)
            self._addBuff("</span><br>")
        else:
            self.addText("-- "+text+" --\n")

    def addSectionSep(self):
        if self._isHTML:
            self._addBuff("<br><br>")
        else:
            self._addBuff("\n\n")

    def _addBuff(self, buff):
        if not self._isFinished:
            self._buff+=buff

    def setTitle(self, title):
        self._title=title
