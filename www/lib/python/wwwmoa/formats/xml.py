def fix_text(str):
    return str.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("'", "&apos;").replace("\"", "&quot;")
