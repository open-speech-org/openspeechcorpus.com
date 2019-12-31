#!/usr/bin/python

import argparse
import logging
import os

import requests

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())


def create_dir_if_does_not_exists(path):
    """
    This function creates a directory in the specified path if does not exists
    :param path: file_path
    :return: None
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    else:
        LOGGER.debug(f"Directory {path} already exists, skipping")


def configure_log_level(logger_level):
    """
    This function configure the logger level
    :param logger_level:
    :return: None
    """
    try:
        LOGGER.setLevel(logger_level)
    except ValueError:
        LOGGER.error("Invalid logger_level: values available: DEBUG, INFO, WARNING, ERROR, CRITICAL")
        exit(0)


def create_file_with_name_and_content(file_path, content):
    """
    This function creates a file in the file_name path with the content
    :param file_path: path of file
    :param content: content to append into file
    :return: None
    """
    file = open(file_path, "w+")
    file.write(content)


class OPSScrapper(object):
    SENTENCES_URL_NAME = "sentences"
    AUTHORS_URL_NAME = "authors"
    AUTHOR_URL_NAME = "author"
    TALES_URL_NAME = "tales"
    TALE_URL_NAME = "tale"
    LEVELS_URL_NAME = "levels"
    CATEGORY_LEVELS = "category_levels"
    WORDS_BY_CATEGORY_LEVEL = "aphasia_words"
    ISOLATED_CATEGORY = "isolated_category"
    ISOLATED_BY_CATEGORY = "isolated_by_category"

    URLS = {
        SENTENCES_URL_NAME: "/api/sentences",
        AUTHORS_URL_NAME: "/api/authors",
        AUTHOR_URL_NAME: "/api/tales/{}",
        TALES_URL_NAME: "/api/tales",
        TALE_URL_NAME: "/api/sentences/{}",
        LEVELS_URL_NAME: "/api/levels",
        CATEGORY_LEVELS: "/api/level/{}",
        WORDS_BY_CATEGORY_LEVEL: "/api/level/{}/category/{}",
        ISOLATED_CATEGORY: "/api/isolated-words/categories",
        ISOLATED_BY_CATEGORY: "/api/isolated-words/{}"
    }

    def __init__(self, base_url, output_folder):
        """
        :param base_url: URL from OPS
        :param output_folder: Folder to store all output
        """
        self._base_url = base_url
        self.output_folder = output_folder
        create_dir_if_does_not_exists(output_folder)
        self.api_folder = os.path.join(self.output_folder, "api")
        create_dir_if_does_not_exists(self.api_folder)

    def get_url_for(self, url_name):
        return f"{base_url}{self.URLS[url_name]}"

    @staticmethod
    def generic_master_detail_scrap(
        master_url,
        detail_url,
        master_output_path,
        detail_output_path,
        entity_name,
        master_response_node_with_detail_info,
        master_output_name="index.json",
        attribute_to_extract_and_name_detail="id",
        extra_detail_process=None
    ):
        """
        This functions has utilities to scrap an entity and its related detail
        :param master_url: URL for  master
        :param detail_url: URL for detail
        :param master_output_path: output to store the master
        :param detail_output_path: output to store the detail
        :param entity_name: Entity name for logging purposes
        :param master_response_node_with_detail_info: Node inside the master response with the detail info
        :param master_output_name: file to store master response
        :param attribute_to_extract_and_name_detail: attribute from the master response to query detail
        :param extra_detail_process: function to generate an extra process with the detail response
        :return:
        """
        master_response = requests.get(master_url)
        if master_response.ok:
            master_json_content = master_response.json()
            #TODO: Can we drop this function call?
            create_dir_if_does_not_exists(master_output_path)
            create_file_with_name_and_content(
                os.path.join(master_output_path, master_output_name),
                master_response.content.decode()
            )
            LOGGER.info(f"{entity_name} fetched")
            LOGGER.debug(master_json_content)
            container = master_json_content.get(master_response_node_with_detail_info, []) \
                if master_response_node_with_detail_info else \
                master_json_content
            for detail in container:
                detail_identifier = str(detail.get(attribute_to_extract_and_name_detail))
                detail_response = requests.get(detail_url.format(detail_identifier))
                if detail_response.ok:
                    detail_decoded_content = detail_response.content.decode()
                    create_file_with_name_and_content(
                        os.path.join(detail_output_path, detail_identifier),
                        detail_decoded_content
                    )
                    LOGGER.info(f"{entity_name} with id {detail_identifier} with status OK")
                    LOGGER.debug(detail_decoded_content)
                    if extra_detail_process:
                        extra_detail_process(detail_response.json())
                else:
                    LOGGER.error(
                        f"Error calling {detail_url}, http error code: {detail_response.status_code}"
                    )

    def orchestrate_master_detail(
        self,
        master_url_name,
        detail_url_name,
        api_folder_master_name,
        api_folder_detail_name,
        entity_name,
        master_response_node_with_detail_info,
    ):
        """
        This is a function to orchestrate the behavior for a master detail scrapper
        :return:
        """
        url_for_master = self.get_url_for(master_url_name)
        url_for_detail = self.get_url_for(detail_url_name)
        master_dir = os.path.join(self.api_folder, api_folder_master_name)
        create_dir_if_does_not_exists(master_dir)
        detail_dir = os.path.join(self.api_folder, api_folder_detail_name)
        create_dir_if_does_not_exists(detail_dir)
        self.generic_master_detail_scrap(
            url_for_master,
            url_for_detail,
            master_dir,
            detail_dir,
            entity_name,
            master_response_node_with_detail_info
        )

    def scrap_authors(self):
        """
        This function scraps data from the authors api
        :return:
        """
        self.orchestrate_master_detail(
            self.AUTHORS_URL_NAME,
            self.AUTHOR_URL_NAME,
            "author",
            "tales",
            "Author",
            "authors"
        )

    def scrap_tales_sentences(self):
        """
        This function scraps data from the tales api
        :return: None
        """
        self.orchestrate_master_detail(
            self.TALES_URL_NAME,
            self.TALE_URL_NAME,
            "tales",
            "sentences",
            "Tales",
            "tales"
        )

    def scrap_aphasia(self):
        """
        This function scraps data from the isolated words API
        :return: None
        """
        self.orchestrate_master_detail(
            ,
            ,
            "levels",
            "level",
            "Aphasia",
            None
        )
        levels_url = self.get_url_for(self.LEVELS_URL_NAME)
        url_for_detail = self.get_url_for(self.CATEGORY_LEVELS)
        levels_dir = os.path.join(self.api_folder, "levels")
        create_dir_if_does_not_exists(levels_dir)
        detail_dir = os.path.join(self.api_folder, "level")
        create_dir_if_does_not_exists(detail_dir)
        master_response = requests.get(levels_url)
        if master_response.ok:
            master_json_content = master_response.json()
            create_dir_if_does_not_exists(master_output_path)
            create_file_with_name_and_content(
                os.path.join(master_output_path, master_output_name),
                master_response.content.decode()
            )
            LOGGER.info(f"{entity_name} fetched")
            LOGGER.debug(master_json_content)
            container = master_json_content.get(master_response_node_with_detail_info, []) \
                if master_response_node_with_detail_info else \
                master_json_content
            for detail in container:
                detail_identifier = str(detail.get(attribute_to_extract_and_name_detail))
                detail_response = requests.get(detail_url.format(detail_identifier))
                if detail_response.ok:
                    detail_decoded_content = detail_response.content.decode()
                    create_file_with_name_and_content(
                        os.path.join(detail_output_path, detail_identifier),
                        detail_decoded_content
                    )
                    LOGGER.info(f"{entity_name} with id {detail_identifier} with status OK")
                    LOGGER.debug(detail_decoded_content)
                    if extra_detail_process:
                        extra_detail_process(detail_response.json())
                else:
                    LOGGER.error(
                        f"Error calling {detail_url}, http error code: {detail_response.status_code}"
                    )



    def scrap_isolated_words(self):
        """
        This function scraps data from the isolated words API
        :return: None
        """
        self.orchestrate_master_detail(
            self.ISOLATED_CATEGORY,
            self.ISOLATED_BY_CATEGORY,
            "isolated-words/categories",
            "isolated-words",
            "Isolated words",
            None
        )

    def scrap_ops(self):
        """
        Scraps all data of Open Speech Corpus into a set of files

        :return: None
        """
        # self.scrap_tales_sentences()
        # self.scrap_authors()
        # self.scrap_isolated_words()
        self.scrap_aphasia()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        "Scrap text from Open Speech Corpus"
    )
    parser.add_argument(
        "--url",
        help="Open Speech Corpus Host",
        default="http://openspeechcorpus.contraslash.com"
    )
    parser.add_argument(
        "--output_folder",
        help="Folder to store results",
        default="output"
    )
    parser.add_argument(
        '--logger_level',
        help="Logger level, values available: DEBUG, INFO, WARNING, ERROR, CRITICAL",
        default="ERROR"
    )

    args = vars(parser.parse_args())
    configure_log_level(args.get("logger_level"))
    output_folder = args.get("output_folder")
    base_url = args.get("url")
    ops_scrapper = OPSScrapper(base_url, output_folder)
    ops_scrapper.scrap_ops()
