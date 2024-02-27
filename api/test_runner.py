from django.conf import settings
from django.test.runner import DiscoverRunner


class FastTestRunner(DiscoverRunner):
    def setup_test_environment(self):
        super(FastTestRunner, self).setup_test_environment()

        settings.DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'

        settings.PASSWORD_HASHERS = (
            'django.contrib.auth.hashers.MD5PasswordHasher',
        )
        del settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']
        del settings.REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES']
