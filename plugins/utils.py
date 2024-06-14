from nameko.exceptions import ConfigurationError


def validate_env_vars(*required_vars):
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ConfigurationError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )
