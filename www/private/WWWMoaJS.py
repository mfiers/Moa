### WWWMoa ###############################
### JS / JavaScript Utility Libraries
### Version: 0.1
### Date: November 20, 2009

## Imports ##
import WWWMoaHTML

## Escapes a string for embedding in a JavaScript string literal.
def fix_text(txt):
    return txt.replace("\\", "\\\\").replace("\"", "\\\"").replace("'", "\\'").replace("\n", "\\n")

## Escapes a string for embedding in a JavaScript string literal, and ensures that it can safely be placed in a <script> tag in an HTML document.
def fix_text_for_html(txt):
    return WWWMoaHTML.fix_text(fix_text(txt))
