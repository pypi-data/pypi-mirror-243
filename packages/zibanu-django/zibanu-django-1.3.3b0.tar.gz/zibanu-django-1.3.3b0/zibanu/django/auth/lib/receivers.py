# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

from typing import Any

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         9/11/23 17:03
# Project:      Zibanu - Django
# Module Name:  receivers
# Description:
# ****************************************************************
# Default imports
from django.apps import apps
from django.contrib.auth.models import Group
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.db.models.signals import post_save
from django.dispatch import receiver

from zibanu.django.auth.models import GroupLevel
from zibanu.django.utils import get_ip_address
from .enums import GroupLevelEnum
from .signals import on_change_password, on_request_password


@receiver(post_save, sender=Group)
def group_post_save_receiver(sender, instance, created, **kwargs) -> None:
    """
    Receiver for post_save signal from Group entity; this receiver create a GroupLevel record with its default values
    Parameters
    ----------
    sender : Sender class of signal
    instance : Instance of sender class
    created : True if the event is a record create, otherwise False
    kwargs : Dictionary of arguments

    Returns
    -------
    None
    """
    if created:
        group_level = GroupLevel(group=instance, level=GroupLevelEnum.OPERATOR)
        group_level.save()


@receiver(on_change_password, dispatch_uid="on_change_password")
@receiver(on_request_password, dispatch_uid="on_request_password")
@receiver(user_logged_in, dispatch_uid="on_user_logged_in")
@receiver(user_login_failed, dispatch_uid="on_user_login_failed")
def auth_receiver(sender: Any, user: Any = None, **kwargs) -> None:
    """
    Receiver for signals on_change_password, on_request_password, user_logged_in, user_login_failed

    Parameters
    ----------
    sender: Sender class of signal
    user: User object to get data
    kwargs: Dictionary with fields and parametes

    Returns
    -------
    None
    """
    # Set detail field
    detail = kwargs.get("detail", "")
    if kwargs.get("credentials", None) is not None:
        detail = kwargs.get("credentials").get("username", "")

    if isinstance(sender, str):
        class_name = sender
    else:
        class_name = sender.__name__
    ip_address = get_ip_address(kwargs.get("request", None))
    # Try to capture receiver name from receivers pool.
    try:
        receivers = kwargs.get("signal").receivers
        receiver_id = receivers[len(receivers) - 1][0][0]
        if isinstance(receiver_id, str):
            action = receiver_id
        else:
            action = "zb_auth_event"
        # If username context var exists.
    except:
        action = "zb_auth_event"

    if apps.is_installed("zibanu.django.logging"):
        from zibanu.django.logging.models import Log
        log = Log(user=user, sender=class_name, action=action, ip_address=ip_address, detail=detail)
        log.save()
