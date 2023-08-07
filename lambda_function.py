import sys

import translation as tr


translator = tr.Translator(default_to_lang=tr.Language.EN)


def lambda_handler(event, context):
    translation = tr.lambda_handler(event, translator)

    return {
        "py-version": sys.version_info,
        "func-name": context.function_name,
        "func-version": context.function_version,
        "translation": translation,
    }
