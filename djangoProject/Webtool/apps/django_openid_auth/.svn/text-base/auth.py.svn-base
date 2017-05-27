#coding=utf-8
# django-openid-auth -  OpenID integration for django.contrib.auth
#
# Copyright (C) 2008-2010 Canonical Ltd.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Glue between OpenID and django.contrib.auth."""

__metaclass__ = type

import logging
from django.conf import settings
from django.contrib.auth.models import User, Group
from openid.consumer.consumer import SUCCESS
from openid.extensions import ax, sreg, pape

from apps.django_openid_auth import teams
#from django_openid_auth.models import UserOpenID
from apps.django_openid_auth.exceptions import (
    IdentityAlreadyClaimed,
    DuplicateUsernameViolation,
    MissingUsernameViolation,
    MissingPhysicalMultiFactor,
    RequiredAttributeNotReturned,
)


class OpenIDBackend:
    """A django.contrib.auth backend that authenticates the user based on
    an OpenID response."""
    supports_inactive_user = False
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, **kwargs):
        """Authenticate the user based on an OpenID response."""
        # Require that the OpenID response be passed in as a keyword
        # argument, to make sure we don't match the username/password
        # calling conventions of authenticate.

        openid_response = kwargs.get('openid_response')
        if openid_response is None:
            return None

        if openid_response.status != SUCCESS:
            return None
        sreg_response = sreg.SRegResponse.fromSuccessResponse(openid_response)
        if sreg_response:
            nickname = sreg_response.get('nickname')
            fullname = sreg_response.get('fullname')
            email = sreg_response.get('email')
        else:
            return None
        username = nickname
        first_name = fullname if fullname else nickname
        user = User.objects.filter(username = nickname)
        data = {
            "id": username,
            "firstName": first_name,
            "lastName": first_name,
            "email": email,
            "password": username
        }
        if len(user) == 0:
            user = User.objects.create_user(username, email, password=None)
            user.first_name = fullname
            user.save()
        
        try:
            user = User.objects.get(username__iexact=nickname)
        except User.DoesNotExist:
            return None

        return user
