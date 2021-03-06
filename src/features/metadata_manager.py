import asyncio
import multiprocessing
import traceback
from collections import ChainMap
from itertools import repeat
from logging import Logger
from multiprocessing import shared_memory

from config.config_manager import ConfigManager
from features.accessibility import Accessibility
from features.cookies import Cookies
from features.extract_from_files import ExtractFromFiles
from features.gdpr import GDPR
from features.html_based import (
    Advertisement,
    AntiAdBlock,
    CookiesInHtml,
    EasylistAdult,
    EasylistGermany,
    EasyPrivacy,
    FanboyAnnoyance,
    FanboyNotification,
    FanboySocialMedia,
    IFrameEmbeddable,
    LogInOut,
    Paywalls,
    PopUp,
    RegWall,
)
from features.javascript import Javascript
from features.malicious_extensions import MaliciousExtensions
from features.metadata_base import MetadataBase
from features.metatag_explorer import MetatagExplorer
from features.security import Security
from features.website_manager import Singleton, WebsiteManager
from lib.constants import MESSAGE_ALLOW_LIST, MESSAGE_SHARED_MEMORY_NAME
from lib.logger import create_logger
from lib.timing import get_utc_now


def _parallel_setup(
    extractor_class: type(MetadataBase), logger: Logger
) -> MetadataBase:
    extractor = extractor_class(logger)
    extractor.setup()
    return extractor


@Singleton
class MetadataManager:
    metadata_extractors: list[type(MetadataBase)] = []

    def __init__(self) -> None:
        self._logger = create_logger()
        self._setup_extractors()

    def _setup_extractors(self) -> None:

        extractors = [
            Advertisement,
            EasyPrivacy,
            MaliciousExtensions,
            ExtractFromFiles,
            CookiesInHtml,
            FanboyAnnoyance,
            FanboyNotification,
            FanboySocialMedia,
            AntiAdBlock,
            EasylistGermany,
            EasylistAdult,
            Paywalls,
            Security,
            IFrameEmbeddable,
            PopUp,
            RegWall,
            LogInOut,
            Cookies,
            GDPR,
            Javascript,
            MetatagExplorer,
            Accessibility,
        ]

        pool = multiprocessing.Pool(processes=6)
        self.metadata_extractors = pool.starmap(
            _parallel_setup, zip(extractors, repeat(self._logger))
        )

    async def _extract_meta_data(
        self,
        allow_list: dict,
        config_manager: ConfigManager,
        shared_memory_name: str,
    ) -> dict:
        data = {}
        tasks = []

        shared_status = shared_memory.ShareableList(name=shared_memory_name)
        shared_status[0] = 0

        for metadata_extractor in self.metadata_extractors:
            if allow_list[metadata_extractor.key]:
                if (
                    config_manager.is_host_predefined()
                    and config_manager.is_metadata_predefined(
                        metadata_extractor.key
                    )
                ):
                    extracted_metadata = (
                        config_manager.get_predefined_metadata(
                            metadata_extractor.key
                        )
                    )
                    data.update(extracted_metadata)
                    shared_status[0] += 1
                elif metadata_extractor.call_async:
                    tasks.append(metadata_extractor.astart())
                else:
                    data.update(metadata_extractor.start())
                    shared_status[0] += 1

        extracted_metadata = await asyncio.gather(*tasks)
        shared_status[0] += len(tasks)
        data = {**data, **dict(ChainMap(*extracted_metadata))}
        return data

    def start(self, message: dict) -> dict:

        website_manager = WebsiteManager.get_instance()
        website_manager.load_website_data(message=message)

        config_manager = ConfigManager.get_instance()
        config_manager.top_level_domain = (
            website_manager.website_data.top_level_domain
        )

        starting_extraction = get_utc_now()
        if website_manager.website_data.html == "":
            exception = "Empty html. Potentially, splash failed."
            extracted_meta_data = {"exception": exception}
        else:
            try:
                extracted_meta_data = asyncio.run(
                    self._extract_meta_data(
                        allow_list=message[MESSAGE_ALLOW_LIST],
                        config_manager=config_manager,
                        shared_memory_name=message[MESSAGE_SHARED_MEMORY_NAME],
                    )
                )
            except ConnectionError as e:
                exception = f"Connection error extracting metadata: '{e.args}'"
                self._logger.exception(
                    exception,
                    exc_info=True,
                )
                extracted_meta_data = {"exception": exception}
            except Exception as e:
                exception = (
                    f"Unknown exception from extracting metadata: '{e.args}'. "
                    f"{''.join(traceback.format_exception(None, e, e.__traceback__))}"
                )
                self._logger.exception(
                    exception,
                    exc_info=True,
                )
                extracted_meta_data = {"exception": exception}

        extracted_meta_data.update(
            {
                "time_for_extraction": get_utc_now() - starting_extraction,
                **website_manager.get_website_data_to_log(),
            }
        )

        website_manager.reset()
        return extracted_meta_data
