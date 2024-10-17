import bleach

# Lista de etiquetas permitidas
ALLOWED_TAGS = ['a', 'b', 'i', 'u', 'em', 'strong', 'p', 'ul', 'ol', 'li', 'br', 'span', 'h1']

# Lista de atributos permitidos
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'img': ['src', 'alt'],
}

def sanitize_html(html_content: str) -> str:
    return bleach.clean(
        html_content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )
