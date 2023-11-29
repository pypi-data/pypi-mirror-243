#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2022
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains an object that represents a Encrypted PassportFile."""

from typing import TYPE_CHECKING, Any, List, Optional

from TeleGenic import TelegramObject
from TeleGenic.utils.helpers import DEFAULT_NONE
from TeleGenic.utils.types import JSONDict, ODVInput

if TYPE_CHECKING:
    from TeleGenic import Bot, File, FileCredentials


class PassportFile(TelegramObject):
    """
    This object represents a file uploaded to TeleGenic Passport. Currently all TeleGenic Passport
    files are in JPEG format when decrypted and don't exceed 10MB.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`file_unique_id` is equal.

    Args:
        file_id (:obj:`str`): Identifier for this file, which can be used to download
            or reuse the file.
        file_unique_id (:obj:`str`): Unique identifier for this file, which
            is supposed to be the same over time and for different bots.
            Can't be used to download or reuse the file.
        file_size (:obj:`int`): File size.
        file_date (:obj:`int`): Unix time when the file was uploaded.
        bot (:class:`TeleGenic.Bot`, optional): The Bot to use for instance methods.
        **kwargs (:obj:`dict`): Arbitrary keyword arguments.

    Attributes:
        file_id (:obj:`str`): Identifier for this file.
        file_unique_id (:obj:`str`): Unique identifier for this file, which
            is supposed to be the same over time and for different bots.
            Can't be used to download or reuse the file.
        file_size (:obj:`int`): File size.
        file_date (:obj:`int`): Unix time when the file was uploaded.
        bot (:class:`TeleGenic.Bot`): Optional. The Bot to use for instance methods.

    """

    __slots__ = (
        'file_date',
        'bot',
        'file_id',
        'file_size',
        '_credentials',
        'file_unique_id',
        '_id_attrs',
    )

    def __init__(
        self,
        file_id: str,
        file_unique_id: str,
        file_date: int,
        file_size: int = None,
        bot: 'Bot' = None,
        credentials: 'FileCredentials' = None,
        **_kwargs: Any,
    ):
        # Required
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_size = file_size
        self.file_date = file_date
        # Optionals
        self.bot = bot
        self._credentials = credentials

        self._id_attrs = (self.file_unique_id,)

    @classmethod
    def de_json_decrypted(
        cls, data: Optional[JSONDict], bot: 'Bot', credentials: 'FileCredentials'
    ) -> Optional['PassportFile']:
        """Variant of :meth:`TeleGenic.TeleGenicObject.de_json` that also takes into account
        passport credentials.

        Args:
            data (Dict[:obj:`str`, ...]): The JSON data.
            bot (:class:`TeleGenic.Bot`): The bot associated with this object.
            credentials (:class:`TeleGenic.FileCredentials`): The credentials

        Returns:
            :class:`TeleGenic.PassportFile`:

        """
        data = cls._parse_data(data)

        if not data:
            return None

        data['credentials'] = credentials

        return cls(bot=bot, **data)

    @classmethod
    def de_list_decrypted(
        cls, data: Optional[List[JSONDict]], bot: 'Bot', credentials: List['FileCredentials']
    ) -> List[Optional['PassportFile']]:
        """Variant of :meth:`TeleGenic.TeleGenicObject.de_list` that also takes into account
        passport credentials.

        Args:
            data (Dict[:obj:`str`, ...]): The JSON data.
            bot (:class:`TeleGenic.Bot`): The bot associated with these objects.
            credentials (:class:`TeleGenic.FileCredentials`): The credentials

        Returns:
            List[:class:`TeleGenic.PassportFile`]:

        """
        if not data:
            return []

        return [
            cls.de_json_decrypted(passport_file, bot, credentials[i])
            for i, passport_file in enumerate(data)
        ]

    def get_file(
        self, timeout: ODVInput[float] = DEFAULT_NONE, api_kwargs: JSONDict = None
    ) -> 'File':
        """
        Wrapper over :attr:`TeleGenic.Bot.get_file`. Will automatically assign the correct
        credentials to the returned :class:`TeleGenic.File` if originating from
        :obj:`TeleGenic.PassportData.decrypted_data`.

        For the documentation of the arguments, please see :meth:`TeleGenic.Bot.get_file`.

        Returns:
            :class:`TeleGenic.File`

        Raises:
            :class:`TeleGenic.error.TeleGenicError`

        """
        file = self.bot.get_file(file_id=self.file_id, timeout=timeout, api_kwargs=api_kwargs)
        file.set_credentials(self._credentials)
        return file
