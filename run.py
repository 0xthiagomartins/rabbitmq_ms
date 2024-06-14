import sys
import nameko.cli
import eventlet

eventlet.monkey_patch()
sys.argv.extend(["--config", "src/config.yml", "src.service"])
nameko.cli.run()
