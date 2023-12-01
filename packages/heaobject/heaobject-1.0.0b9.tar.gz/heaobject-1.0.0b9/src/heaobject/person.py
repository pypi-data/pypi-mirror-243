from .root import AbstractDesktopObject
from typing import Optional
from email_validator import validate_email, EmailNotValidError  # Leave this here for other modules to use
from functools import partial


class Person(AbstractDesktopObject):
    """
    Represents a Person
    """

    def __init__(self) -> None:
        super().__init__()
        # id is a super field
        # name is inherited in super
        self.__preferred_name: Optional[str] = None
        self.__first_name: Optional[str] = None
        self.__last_name: Optional[str] = None
        self.__title: Optional[str] = None
        self.__email: Optional[str] = None
        self.__phone_number: Optional[str] = None
        self.__id_labs_manage: Optional[list] = None
        self.__id_labs_member: Optional[list] = None
        self.__id_labs_collaborator: Optional[list] = None
        self.__id_projects_collaborator: Optional[list] = None
        self.__display_name: Optional[str] = None

    @property
    def preferred_name(self) -> Optional[str]:
        """
        The Person's preferred name (Optional).
        """
        return self.__preferred_name

    @preferred_name.setter
    def preferred_name(self, preferred_name: Optional[str]) -> None:
        self.__preferred_name = str(preferred_name) if preferred_name is not None else None

    @property
    def first_name(self) -> Optional[str]:
        """
        The Person's first name or given name (Optional).
        """
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name: Optional[str]) -> None:
        self.__first_name = str(first_name) if first_name is not None else None
        self.__update_display_name()

    @property
    def last_name(self) -> Optional[str]:
        """
          The Person's last name (Optional).
        """
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name: Optional[str]) -> None:
        self.__last_name = str(last_name) if last_name is not None else None
        self.__update_display_name()

    @property
    def title(self) -> Optional[str]:
        """
          The Person's title (Optional).
        """
        return self.__title

    @title.setter
    def title(self, title: Optional[str]) -> None:
        self.__title = str(title) if title is not None else None

    @property
    def email(self) -> Optional[str]:
        """
        The person's email (Optional). Must be a valid e-mail address or None.
        """
        return self.__email

    @email.setter
    def email(self, email: Optional[str]) -> None:
        self.__email = _validate_email(str(email)).email if email is not None else None

    @property
    def phone_number(self) -> Optional[str]:
        """
          The Person's phone number (Optional).
        """
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, phone_number: Optional[str]) -> None:
        self.__phone_number = str(phone_number) if phone_number is not None else None

    @property
    def id_labs_manage(self) -> Optional[list]:
        """
          The Person's list of labs they manage (Optional).
        """
        return self.__id_labs_manage

    @id_labs_manage.setter
    def id_labs_manage(self, id_labs_manage: Optional[list]) -> None:
        if id_labs_manage is None:
            self.__id_labs_manage = None
        else:
            self.__id_labs_manage = [str(item) for item in id_labs_manage if item is not None]

    @property
    def id_labs_member(self) -> Optional[list]:
        """
          The Person's list of labs they are a member of (Optional).
        """
        return self.__id_labs_member

    @id_labs_member.setter
    def id_labs_member(self, id_labs_member: Optional[list]) -> None:
        if id_labs_member is None:
            self.__id_labs_member = None
        else:
            self.__id_labs_member = [str(item) for item in id_labs_member if item is not None]

    @property
    def id_labs_collaborator(self) -> Optional[list]:
        """
          The Person's list of labs they are listed as a collaborator of (Optional).
        """
        return self.__id_labs_collaborator

    @id_labs_collaborator.setter
    def id_labs_collaborator(self, id_labs_collaborator: Optional[list]):
        if id_labs_collaborator is None:
            self.__id_labs_collaborator = None
        else:
            self.__id_labs_collaborator = [str(item) for item in id_labs_collaborator if item is not None]

    @property
    def id_projects_collaborator(self) -> Optional[list]:
        """
          The Person's list of projects they are listed as a collaborator of (Optional).
        """
        return self.__id_projects_collaborator

    @id_projects_collaborator.setter
    def id_projects_collaborator(self, id_projects_collaborator: Optional[list]):
        if id_projects_collaborator is None:
            self.__id_projects_collaborator = None
        else:
            self.__id_projects_collaborator = [str(item) for item in id_projects_collaborator if item is not None]

    def __update_display_name(self):
        fname = self.first_name if self.first_name else ""
        lname = self.last_name if self.last_name else ""
        if fname or lname:
            self.display_name = f"{fname}{' ' if fname and lname else ''}{lname}"
        else:
            self.display_name = None


_validate_email = partial(validate_email, check_deliverability=False)
