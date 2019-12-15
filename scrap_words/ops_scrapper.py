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
        os.mkdir(path)
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
    TALES_URL_NAME = "tales"
    TALE_URL_NAME = "tale"

    URLS = {
        SENTENCES_URL_NAME: "/api/sentences",
        TALES_URL_NAME: "/api/tales",
        TALE_URL_NAME: "/api/sentences/{}"
    }

    def __init__(self, base_url, output_folder):
        """
        :param base_url: URL from OPS
        :param output_folder: Folder to store all output
        """
        self._base_url = base_url
        self.output_folder = output_folder
        self.api_folder = os.path.join(self.output_folder, "api")
        create_dir_if_does_not_exists(self.api_folder)

    def get_url_for(self, url_name):
        return f"{base_url}{self.URLS[url_name]}"

    def scrap_tales_sentences(self):
        """
        This function scraps data from the tales api
        :param base_url: URL from OPS
        :param output_folder: Folder to store all output
        :return: None
        """
        url_for_all_tales = self.get_url_for(self.TALES_URL_NAME)
        tales_response = requests.get(url_for_all_tales)
        if tales_response.ok:
            tales = tales_response.json()
            tales_dir = os.path.join(self.api_folder, "tales")
            create_dir_if_does_not_exists(tales_dir)
            create_file_with_name_and_content(os.path.join(tales_dir, "index.json"), tales_response.content.decode())
            LOGGER.info("Tales fetched")
            LOGGER.debug(tales)
            for tale in tales.get("tales", list()):
                tale_id = str(tale.get("id", 0))
                url_for_tale = self.get_url_for(self.TALE_URL_NAME).format(tale_id)
                single_tale_response = requests.get(url_for_tale)
                if single_tale_response.ok:
                    create_file_with_name_and_content(
                        os.path.join(tales_dir, tale_id),
                        single_tale_response.content.decode()
                    )
                    LOGGER.info(f"Tale with id {tale_id} with status OK")
                    LOGGER.debug(tale)
                else:
                    LOGGER.error(
                        f"Error calling {url_for_tale}, http error code: {single_tale_response.status_code}"
                    )
        else:
            LOGGER.error(
                f"Error calling {url_for_all_tales}, http error code: {tales_response.status_code}"
            )

    def scrap_ops(self):
        """
        Scraps all data of Open Speech Corpus into a set of files

        :return: None
        """
        self.scrap_tales_sentences()


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
