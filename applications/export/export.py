import json
from collections import OrderedDict

from applications.aphasia import (
    models as aphasia_models,
    serializers as aphasia_serializers
)


def export(key_separator="."):
    """
from applications.export.export import export
export()
    :return:
    """
    main_dict = dict()
    main_dict["aphasia"] = export_aphasia(key_separator=key_separator)
    print(json.dumps(main_dict, indent=4))


def export_aphasia(key_separator="."):
    local_dict = OrderedDict()
    aphasia_levels = aphasia_models.Level.objects.all()
    for level in aphasia_levels:
        serialized_level = aphasia_serializers.Level(level)
        data_for_level = serialized_level.data
        aphasia_level_categories_for_level = aphasia_models.LevelCategory.objects.filter(level=level)
        children_for_level = OrderedDict()
        for category in aphasia_level_categories_for_level:
            serialized_category = aphasia_serializers.LevelCategory(category)
            data_for_category = serialized_category.data
            data_for_category.pop("level")
            children_for_level[category.title] = data_for_category

            aphasia_sentences = aphasia_models.LevelSentence.objects.filter(level_category=category)
            children_for_category = OrderedDict()
            for sentence in aphasia_sentences:
                serialized_sentence = aphasia_serializers.LevelSentence(sentence)
                data_for_sentence = serialized_sentence.data
                data_for_sentence.pop("level_category")
                data_for_sentence["key"] = f"aphasia{key_separator}{level.title}{key_separator}{category.title}{key_separator}{sentence.text}"
                children_for_category[sentence.text] = data_for_sentence
            data_for_category["children"] = children_for_category

        data_for_level["children"] = children_for_level
        local_dict[level.title] = data_for_level

    return local_dict