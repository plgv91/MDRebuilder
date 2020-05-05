from django import template

register = template.Library()

@register.filter(name='addAttr')
def addAttr(field, css):
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            key, val = d.split(':')
            attrs[key] = val

    return field.as_widget(attrs=attrs)

@register.filter(name='addClass')
def addClass(value, args):
    return value.as_widget(attrs={'class': args})

@register.filter(name='addId')
def addId(value, args):
    return value.as_widget(attrs={'id': args})

@register.filter(name='addType')
def addType(value, args):
    return value.as_widget(attrs={'type': args})

@register.filter(name='addPlaceholder')
def addPlaceholder(value, args):
    return value.as_widget(attrs={'placeholder': args})

@register.filter(name='addRequired')
def addRequired(value, args):
    return value.as_widget(attrs={'required': args})

@register.filter(name='addDataValidation')
def addDataValidation(value, args):
    return value.as_widget(attrs={'data-validation-required-message': args})