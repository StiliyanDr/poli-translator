import sys

import translation as tr


translator = tr.Translator(default_to_lang=tr.Language.EN)


def log_results(pairs):
    for i, (text, translation) in enumerate(pairs):
        print("ITEM ", i + 1)
        print("Original:", text)
        print("Translation:", translation)


def lambda_handler(event, context):
    translation = tr.lambda_handler(event, translator)
    log_results(translation)

    return {
        "py-version": sys.version_info,
        "func-name": context.function_name,
        "func-version": context.function_version,
        "translation": translation,
    }
