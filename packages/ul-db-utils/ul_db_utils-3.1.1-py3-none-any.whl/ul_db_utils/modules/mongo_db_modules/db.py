import importlib
import logging
import os
from glob import glob
from typing import Optional, TYPE_CHECKING, Callable, TypeVar, Any, Union

from flask import Flask
from flask_pymongo import PyMongo
from flask_pymongo.wrappers import Collection

from ul_db_utils.conf import APPLICATION__DB_URI, APPLICATION__DB_DATABASE

if TYPE_CHECKING:
    from api_utils.modules.api_sdk import ApiSdk  # type: ignore
    from api_utils.modules.worker_sdk import WorkerSdk  # type: ignore


class DbWrapper(object):
    def __init__(self) -> None:
        self._wrapper = PyMongo()

    def __getattr__(self, attr: str) -> Any:
        if attr == 'session':
            assert initialized_sdk, 'must initialize db'
        return getattr(self._wrapper, attr)


db: 'PyMongo' = DbWrapper()  # type: ignore

logger = logging.getLogger(__name__)


TFn = TypeVar("TFn", bound=Callable)  # type: ignore


initialized_sdk: Optional['MongoDbConfig'] = None


class MongoDbConfig:

    def __init__(
        self,
        *,
        uri: Optional[str] = APPLICATION__DB_URI,
        db_name: Optional[str] = APPLICATION__DB_DATABASE,
        debug: bool = False,
    ) -> None:
        assert uri
        self.uri = uri
        self.db_name = db_name
        self.debug = debug

        self._flask_app: Optional[Flask] = None

    @property
    def db(self) -> Optional[Collection]:
        if db is None:
            raise OverflowError('DB instance must be initialized')
        return db.db

    def _load_route_modules(self, dir: str, file_pref: str = '') -> None:
        suf = '.py'
        files = set()
        for route in glob(os.path.join(dir, f'{file_pref}*{suf}')):
            files.add(str(route))
        for route in glob(os.path.join(dir, f'**/{file_pref}*{suf}')):
            files.add(str(route))
        for file in files:
            file_rel = os.path.relpath(file, os.getcwd())
            mdl = file_rel[:-len(suf)].replace('\\', '/').strip('/').replace('/', '.')
            if self.debug:
                logger.info('loading module %s', mdl)
            importlib.import_module(mdl)

    def _init_from_sdk_with_flask(  # PRIVATE. ONLY FOR INTERNAL API-UTILS USAGE
        self,
        sdk: Union['ApiSdk', 'WorkerSdk'],
    ) -> None:
        global initialized_sdk
        if initialized_sdk is not None:
            raise OverflowError('initialized DbConfig must be only one! Db has already initialized')
        initialized_sdk = self

        if self._flask_app is not None:
            raise OverflowError()
        self._flask_app = sdk._flask_app  # noqa

        self._attach_to_flask_app(self._flask_app, db)

    def init_with_flask(self, app_name: str) -> Flask:
        global initialized_sdk
        if initialized_sdk is not None:
            raise OverflowError('initialized DbConfig must be only one! Db has already initialized')
        initialized_sdk = self

        if self._flask_app is not None:
            raise OverflowError()
        self._flask_app = Flask(app_name)

        self._flask_app.app_context().push()  # FUCKING HACK

        self._attach_to_flask_app(self._flask_app, db)

        return self._flask_app

    def _attach_to_flask_app(self, app: Flask, db_instance: 'PyMongo') -> None:
        app.config['MONGO_URI'] = self.uri
        db_instance.init_app(app)
