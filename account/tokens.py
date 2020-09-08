from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.signing import Signer
import hashlib


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        signer = Signer()
        value = '-'.join([str(user.pk), str(timestamp), 'true' if user.profile.email_confirmed else 'false'])
        m = hashlib.sha256()
        m.update(value.encode())
        return m.digest()


account_activation_token = AccountActivationTokenGenerator()
