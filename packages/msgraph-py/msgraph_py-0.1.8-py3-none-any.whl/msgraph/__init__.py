import logging

from .devices import (  # noqa: F401
    delete_device,
    get_device,
)
from .groups import (  # noqa: F401
    add_group_member,
    get_group,
    list_group_members,
    remove_group_member,
)
from .identity import (  # noqa: F401
    delete_auth_method,
    get_user,
    get_user_risk,
    list_auth_methods,
    reset_strong_auth,
    revoke_refresh_tokens,
)
from .mail import (  # noqa: F401
    send_mail,
)

logging.getLogger(__name__).addHandler(logging.NullHandler())
