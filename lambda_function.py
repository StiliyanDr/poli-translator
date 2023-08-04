import sys

import translation as tr


translator = tr.Translator(default_to_lang=tr.Language.EN)


def create_language(name):
    return (tr.Language.from_string(name)
            if name is not None
            else None)


def lambda_handler(event, context):
    text = event.get("text", "NA")
    from_language = create_language(event.get("from_language"))
    to_language = create_language(event.get("to_language"))
    translation = (translator.translate(text,
                                        from_lang=from_language,
                                        to_lang=to_language)
                   if text != "NA"
                   else "NA")

    return {
        "py-version": sys.version_info,
        "func-name": context.function_name,
        "func-version": context.function_version,
        "text": text,
        "translation": translation,
    }
