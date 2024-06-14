import sys
import nameko.cli
import eventlet

eventlet.monkey_patch()
sys.argv.extend(["--config", "src/config.yaml", "src.service"])
nameko.cli.run()
