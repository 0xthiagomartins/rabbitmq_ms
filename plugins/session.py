from nameko.dependency_providers import DependencyProvider
import logging


class SessionDataDependency(DependencyProvider):

    def get_dependency(self, worker_ctx):
        try:
            session_data = worker_ctx.data["session_data"]
        except KeyError:
            session_data = None
        except AttributeError:
            session_data = None
        logging.info("SessionDataDependency")
        logging.info(session_data)
        return session_data
