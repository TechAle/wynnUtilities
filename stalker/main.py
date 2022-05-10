from stalker.core import stalkerCore
from stalker.utils import logUtils


if __name__ == "__main__":
    app = logUtils.createLogger()
    stalker = stalkerCore(app)
    stalker.askInformations()
    stalker.startStalking()
