import logging
from nameko.dependency_providers import DependencyProvider
from ..settings import LoggerFilter, get_data_to_log
import logging, pygelf, os


class GraylogDependency(DependencyProvider):
    """Dependency Provider para enviar logs ao Graylog"""

    def __test_provider_connection(self, logger):
        try:
            logger.info("Test message sent to Graylog")
            print("Log message sent successfully.")
        except Exception as e:
            print(f"Error sending log message: {e}")

    def setup(self):
        """
        Função para configurar a API de log relacionada ao Graylog.

        Coleta configurações do graylog contidas no config.yml:
        - Host e Porta do graylog
        - Nível de logs a serem enviados.
        """
        logger = logging.getLogger()

        #: Configuando o graylog
        HOST = os.environ.get("GRAYLOG_HOST")
        PORT = int(os.environ.get("GRAYLOG_PORT"))
        LOG_LEVEL = os.environ.get("GRAYLOG_LOG_LEVEL")
        FACILITY = os.environ.get("GRAYLOG_FACILITY")
        logger.setLevel(LOG_LEVEL)
        handler = pygelf.GelfUdpHandler(host=HOST, port=PORT, facility=FACILITY)
        logger.info("=" * 50)
        logger.info("Configurando Graylog")
        logger.info(
            f"""\
    host: {HOST}
    port: {PORT}
    log_level: {LOG_LEVEL}
    facility: {FACILITY}\
    """
        )
        logger.addHandler(handler)

        # Adicionando o filtro para todos os handlers de log
        for h in logging.root.handlers:
            h.addFilter(LoggerFilter())
        self.__test_provider_connection(logger)
        logger.info("=" * 50)

    def get_dependency(self, worker_ctx):
        return logging.getLogger()
