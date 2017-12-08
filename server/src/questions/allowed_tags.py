"""Tags already included found in bleach.sanitizer.ALLOWED_TAGS
    [a, abbr, acronym, b, blockquote, code, em, i, li, ol, strong, ul]
    When called this two lists are merged
"""
# New tags to be allowed to use with bleach
allowed_tags = ['figure', 'img', 'figcaption', 'p', 'pre', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
                'video', 'table', 'tbody', 'th','tr', 'td','hr','sup','sub', 'source', '!--pagebreak--'
                ]
""" bleach.sanitizer.ALLOWED_ATTRIBUTES is not used as it is stored in a dictionary, everything found in it is included 
    in the allowed_attributes dictionary. The * represents attributes available to all tags
"""
#List of allowed attributes to use with bleach
allowed_attributes = {'a': ['href', 'title', 'target', 'rel'], 'acronym': ['title'], 'abbr': ['title'], 
                    'img': ['src', 'alt'], 'video': ['poster', 'controls'], 'source' : ['src'], 'table' : ['border'], 
                    'th': ['scope'], '*': ['width', 'height', 'style']
                     }
"""bleach.sanitizer.ALLOWED_STYLES by default is an empty list"""
#List of available styles to use with bleach
allowed_styles = ['text-decoration', 'color', 'background-color', 'text-align', 'padding-left', 'border-collapse', 
                'border-style', 'border-color', 'width', 'height']
                