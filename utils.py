from jinja2 import Environment, FileSystemLoader
import settings

def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    extensions.append('jinja2.ext.i18n')
    globals = context.pop('globals', {})

    jinja_env = Environment(
        loader=FileSystemLoader(settings.TEMPLATE_PATH),
        extensions=extensions
    )

    jinja_env.globals.update(globals)

    return jinja_env.get_template(template_name).render(context)
