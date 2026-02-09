from rest_framework.throttling import SimpleRateThrottle

class LoginRateThrottle(SimpleRateThrottle):
    # This string 'login' is a key we will use in settings.py
    # to define the actual limit (e.g., "5/min").
    scope = "login"

    def get_cache_key(self, request, view):
        # get_ident(request) gets the user's IP address.
        # It handles headers like X-Forwarded-For automatically.
        ident = self.get_ident(request)

        # This returns the unique key to track in the cache (Redis/Memory).
        # Example key: 'throttle_login_192.168.1.50'
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
    
"""
If you throttled by username or email, a hacker could intentionally lock you out of your own account by spamming wrong passwords.
By throttling by IP, you block the attacker's computer, leaving the real user's account safe.
"""