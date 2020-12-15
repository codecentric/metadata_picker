import asyncio
import multiprocessing
from itertools import repeat

from features.accessibility import Accessibility
from features.config_manager import ConfigManager
from features.cookies import Cookies
from features.extract_from_files import ExtractFromFiles
from features.gdpr import GDPR
from features.html_based import (
    Advertisement,
    AntiAdBlock,
    ContentSecurityPolicy,
    CookiesInHtml,
    EasylistAdult,
    EasylistGermany,
    EasyPrivacy,
    FanboyAnnoyance,
    FanboyNotification,
    FanboySocialMedia,
    IETracker,
    IFrameEmbeddable,
    LogInOut,
    Paywalls,
    PopUp,
    RegWall,
)
from features.javascript import Javascript
from features.malicious_extensions import MaliciousExtensions
from features.metadata_base import MetadataBase, MetadataBaseException
from features.website_manager import Singleton, WebsiteManager
from lib.constants import MESSAGE_ALLOW_LIST
from lib.logger import create_logger
from lib.timing import get_utc_now


def _create_and_setup(extractor_class, logger) -> MetadataBase:
    extractor: MetadataBase = extractor_class(logger)
    extractor.setup()
    return extractor


@Singleton
class MetadataManager:
    metadata_extractors: list = []

    def __init__(self):
        self._logger = create_logger()
        self._create_extractors()

    def _create_extractors(self) -> None:

        extractors = [
            Advertisement,
            EasyPrivacy,
            MaliciousExtensions,
            ExtractFromFiles,
            IETracker,
            CookiesInHtml,
            FanboyAnnoyance,
            FanboyNotification,
            FanboySocialMedia,
            AntiAdBlock,
            EasylistGermany,
            EasylistAdult,
            Paywalls,
            ContentSecurityPolicy,
            IFrameEmbeddable,
            PopUp,
            RegWall,
            LogInOut,
            Accessibility,
            Cookies,
            GDPR,
            Javascript,
        ]

        pool = multiprocessing.Pool(processes=6)
        self.metadata_extractors = pool.starmap(
            _create_and_setup, zip(extractors, repeat(self._logger))
        )

    async def _extract_meta_data(
        self, allow_list: dict, config_manager: ConfigManager
    ) -> dict:
        data = {}
        tasks = []

        for metadata_extractor in self.metadata_extractors:
            metadata_extractor: MetadataBase
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
                elif metadata_extractor.call_async:
                    tasks.append(metadata_extractor.astart())
                else:
                    extracted_metadata = metadata_extractor.start()
                    data.update(extracted_metadata)

        extracted_metadata = await asyncio.gather(*tasks)
        [data.update(metadata) for metadata in extracted_metadata]
        return data

    def start(self, message: dict) -> dict:

        website_manager = WebsiteManager.get_instance()
        website_manager.load_raw_data(message=message)

        config_manager = ConfigManager.get_instance()
        config_manager.top_level_domain = (
            website_manager.website_data.top_level_domain
        )

        starting_extraction = get_utc_now()
        try:
            extracted_meta_data = asyncio.run(
                self._extract_meta_data(
                    message[MESSAGE_ALLOW_LIST], config_manager
                )
            )
        except MetadataBaseException as e:
            exception = f"Extracting metadata raised: '{e.args}'"
            self._logger.exception(
                exception,
                exc_info=True,
            )
            extracted_meta_data = {"exception": exception}
        except Exception as e:
            exception = (
                f"Unknown exception from extracting metadata: '{e.args}'"
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
