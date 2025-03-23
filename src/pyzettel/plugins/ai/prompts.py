
import jinja2

generate_article_template = """Please generate a short article on the following topic: {{title}}.
Do not output anything apart from the short article. 
Write the article in {{language}}. 
Use Markdown to format the document. For the markup of sections and sub-sections, 
only use hash-tags (like this: '# Title' or '## Subsection'), and do not use any 
"-" or "=" to underline sections names.
{% if additional_input %}
{{additional_input}}
{% endif %}
Start like this: `# {{title}}`
"""

generate_tags_template = """Output a list of (at most 5) hashtags from this text, which 
can be used to categorize the content. Do not include the hash sign (#), and
format the tags in lower case. Join words with a minus sign.
{% if tags %}
Here is a list of pre-exisiting tags. Use them where appropriate, or invent new ones 
when neccessary, in the format of the existing ones:
{{ tags }}
{% else %}
Valid tags look like 'operations-technolog', 'itot-convergence', 'linux-distributions'
{% endif %}
"""

generate_summary = """
"""

generate_improve = """Consider the following markdown-based text between 
<begin> and <end>.
Please improve the text with respect to the following: {{ improve }}.
{% if language %}
Translate the document into {{ language }}
{% endif %}
The output should be a markdown document. For the markup of sections and sub-sections, 
only use hash-tags (like this: '# Title' or '## Subsection'), and do not use any 
"-" or "=" to underline sections names.
<begin>
{{ document }}
<end>
"""



def generate_tags(tags: list[str] | None = None):
    if tags is None:
        tags = []
    return jinja2.Template(generate_tags_template).render(tags=tags)


def generate_article(title: str, language: str | None = None, additional_input: str = ""):
    if language is None:
        language = "english" # hard coded default
    return jinja2.Template(generate_article_template).render(
        title=title, language=language, additional_input=additional_input
    )


def generate_improve_zettel(
    document: str, improve_regards: list[str], language: str | None = None
):
    return jinja2.Template(generate_improve).render(
        document=document, improve=", ".join(improve_regards), language=language
    )

def bibtex_key(author_entry: str, year: str) -> str:
    template = """Generate a bibtex key in the form <author>:<year> from the 
    following bibtex author and year specification. Return only the key. Note 
    that no spaces are allowed.
    Use the last name of the first author only.
    Do not use umlauts.

    author: "{{ author_entry }}"
    year: "{{ year }}"
"""
    return jinja2.Template(template).render(author_entry=author_entry, year=year)


