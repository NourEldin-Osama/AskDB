from markdown_it import MarkdownIt

md = MarkdownIt()


def render_markdown_to_html(text: str) -> str:
    """
    Convert Markdown text to HTML, replacing newlines with <br> tags.
    """
    text = md.render(text).replace("\n", "<br>")
    return text
