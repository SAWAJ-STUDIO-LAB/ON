"""
🎨 HTML Formatter
"""


def bold(text): return "<b>" + str(text) + "</b>"
def italic(text): return "<i>" + str(text) + "</i>"
def code(text): return "<code>" + str(text) + "</code>"
def link(url, text): return "<a href='" + url + "'>" + text + "</a>"
