# This file is part of django-ca (https://github.com/mathiasertl/django-ca).
#
# django-ca is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# django-ca is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along with django-ca. If not, see
# <http://www.gnu.org/licenses/>.

"""Django form fields related to django-ca."""

import abc
import typing
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple, Type, Union

from cryptography import x509
from cryptography.x509.oid import AuthorityInformationAccessOID

from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django_ca import ca_settings, constants, utils, widgets
from django_ca.constants import (
    EXTENDED_KEY_USAGE_HUMAN_READABLE_NAMES,
    EXTENDED_KEY_USAGE_NAMES,
    KEY_USAGE_NAMES,
    REVOCATION_REASONS,
)
from django_ca.extensions import get_extension_name
from django_ca.typehints import CRLExtensionTypeTypeVar, ExtensionTypeTypeVar
from django_ca.utils import parse_general_name
from django_ca.widgets import KeyValueWidget, SubjectWidget

if typing.TYPE_CHECKING:
    from django_ca.modelfields import LazyCertificateSigningRequest

_EXTENDED_KEY_USAGE_CHOICES = sorted(
    [(EXTENDED_KEY_USAGE_NAMES[oid], name) for oid, name in EXTENDED_KEY_USAGE_HUMAN_READABLE_NAMES.items()],
    key=lambda t: t[1],
)
_EXTENDED_KEY_USAGE_MAPPING = {serialized: oid for oid, serialized in EXTENDED_KEY_USAGE_NAMES.items()}


class CertificateSigningRequestField(forms.CharField):
    """A form field for `~cg:cryptography.x509.CertificateSigningRequest` encoded as PEM."""

    start = "-----BEGIN CERTIFICATE REQUEST-----"
    end = "-----END CERTIFICATE REQUEST-----"
    simple_validation_error = _(
        "Could not parse PEM-encoded CSR. They usually look like this: <pre>%(start)s\n...\n%(end)s</pre>"
    ) % {"start": start, "end": end}

    def __init__(self, **kwargs: Any) -> None:
        # COVERAGE NOTE: Below condition is never false, as we never pass a custom help text.
        if not kwargs.get("help_text"):  # pragma: no branch
            kwargs["help_text"] = _(
                """The Certificate Signing Request (CSR) in PEM format. To create a new one:
<span class="shell">openssl genrsa -out priv.pem 4096
openssl req -new -key priv.pem -out csr.pem -utf8 -batch -subj '/CN=example.com'
</span>"""
            )
        if not kwargs.get("widget"):  # pragma: no branch # we never pass a custom widget
            kwargs["widget"] = forms.Textarea
        super().__init__(**kwargs)
        self.widget.attrs.update({"cols": "64"})

    def prepare_value(self, value: Optional[Union[str, "LazyCertificateSigningRequest"]]) -> str:
        """Prepare a value to a form that can be shown in HTML.

        Unfortunately this function is not documented by Django at all but is called when a form is rendered.

        This function receives ``None`` when viewing an initial form for a new instance. If form validation
        fails, it receives the string as posted by the user (which might be an invalid string). When viewing
        an existing certificate, it will receive the LazyField instance of the object.
        """
        if value is None:  # for new objects
            return ""
        if isinstance(value, str):  # when form validation fails
            return value

        # COVERAGE NOTE: This would happen if the field is editable, but is always read-only.
        return value.pem  # pragma: no cover

    # TYPE NOTE: django-stubs typehints this as Optional[Any], but we only ever observed receiving ``str``.
    def to_python(self, value: str) -> x509.CertificateSigningRequest:  # type: ignore[override]
        """Coerce given str to correct data type, raises ValidationError if not possible.

        This function is called during form validation.
        """
        if not value.startswith(self.start) or not value.strip().endswith(self.end):
            raise forms.ValidationError(mark_safe(self.simple_validation_error))
        try:
            return x509.load_pem_x509_csr(value.encode("utf-8"))
        except ValueError as ex:
            raise forms.ValidationError(str(ex)) from ex


class ObjectIdentifierField(forms.CharField):
    """A form field for a :py:class:`~cg:cryptography.x509.ObjectIdentifier`."""

    default_error_messages = {"invalid-oid": _("%(value)s: The given OID is invalid.")}

    def to_python(self, value: str) -> Optional[x509.ObjectIdentifier]:  # type: ignore[override]
        if not value:
            return None

        try:
            return x509.ObjectIdentifier(value)
        except ValueError as ex:
            raise forms.ValidationError(
                self.error_messages["invalid-oid"], code="invalid-oid", params={"value": value}
            ) from ex


class KeyValueField(forms.MultiValueField):
    """Dynamic Key/Value field."""

    widget_class = KeyValueWidget

    def __init__(self, key_choices: Sequence[Tuple[str, str]], **kwargs: Any) -> None:
        fields = [
            forms.JSONField(required=True),
            # These two just serve as template for key/value rows
            forms.ChoiceField(choices=key_choices, required=False),
            forms.CharField(required=False),
        ]

        kwargs["require_all_fields"] = False  # ... or we'd require values in the template

        super().__init__(fields, **kwargs)
        self.widget = self.widget_class(key_choices=key_choices, attrs={"class": "key-value-input"})

    def compress(
        self, data_list: Tuple[List[Dict[str, str]], str, str]
    ) -> Optional[List[Dict[str, str]]]:  # pragma: no cover  # This class is never used directly so far
        if not data_list or not data_list[0]:
            return None
        return data_list[0]


class SubjectField(KeyValueField):
    """Specialized version of KeyValue field for a certificate subject."""

    widget_class = SubjectWidget

    def __init__(self, **kwargs: Any) -> None:
        key_choices = [(oid.dotted_string, name) for oid, name in constants.NAME_OID_DISPLAY_NAMES.items()]
        super().__init__(key_choices=key_choices, **kwargs)

    def compress(  # type: ignore[override]
        self, data_list: Tuple[List[Dict[str, str]], str, str]
    ) -> x509.Name:
        # Empty list happens when you press submit on a completely empty form
        if not data_list or not data_list[0]:
            return x509.Name([])

        values = data_list[0]
        errors = []
        attributes: List[x509.NameAttribute] = []
        found_oids: Set[x509.ObjectIdentifier] = set()
        for oid_dict in values:
            try:
                oid = x509.ObjectIdentifier(oid_dict["key"])

                # Check for duplicate OIDs that should not occur more than once
                if oid in found_oids and oid not in utils.MULTIPLE_OIDS:
                    oid_name = constants.NAME_OID_DISPLAY_NAMES[oid]
                    errors.append(_("%(attr)s: Attribute cannot occur more then once.") % {"attr": oid_name})
                else:
                    found_oids.add(oid)

                attr = x509.NameAttribute(oid=oid, value=oid_dict["value"])
            except Exception as ex:  # pylint: disable=broad-exception-caught  # docs don't specify class
                # Creating the NameAttribute failed (e.g. a country code that does *not* have two characters)
                errors.append(str(ex))
            else:
                attributes.append(attr)

        if errors:
            raise forms.ValidationError(errors)

        name = x509.Name(attributes)
        return name


class GeneralNamesField(forms.CharField):
    """MultipleChoice field for :py:class:`~cg:cryptography.x509.RelativeDistinguishedName`."""

    widget = widgets.GeneralNamesWidget
    default_error_messages = {
        "invalid": _("Unparsable General Name: %(error)s"),
    }

    def to_python(  # type: ignore[override]  # superclass uses Any for str, violates inheritance (in theory)
        self, value: str
    ) -> Optional[List[x509.GeneralName]]:
        if not value:
            return None

        values = []
        for line in value.splitlines():
            line = line.strip()
            if not line:
                continue

            try:
                values.append(parse_general_name(line))
            except ValueError as ex:
                raise forms.ValidationError(
                    self.error_messages["invalid"], params={"error": ex}, code="invalid"
                )
        if not values:
            return None

        return values


class RelativeDistinguishedNameField(forms.CharField):
    """MultipleChoice field for :py:class:`~cg:cryptography.x509.RelativeDistinguishedName`."""

    def to_python(  # type: ignore[override]  # superclass uses Any for str, violates inheritance (in theory)
        self, value: str
    ) -> Optional[x509.RelativeDistinguishedName]:
        if not value:
            return None

        rdns = x509.Name.from_rfc4514_string(value).rdns
        attributes = [attr for rdn in rdns for attr in rdn]
        return x509.RelativeDistinguishedName(attributes=attributes)


class ReasonsField(forms.MultipleChoiceField):
    """MultipleChoice field for :py:class:`~cg:cryptography.x509.ReasonFlags`.

    .. note::

       This field does NOT convert to x509.ReasonFlags itself but uses string values instead. The choice
       field always returns invalid choice errors otherwise.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(choices=REVOCATION_REASONS, **kwargs)


class ExtensionField(forms.MultiValueField, typing.Generic[ExtensionTypeTypeVar], metaclass=abc.ABCMeta):
    """Base class for form fields that serialize to a :py:class:`~cg:cryptography.Extension`."""

    extension_type: Type[ExtensionTypeTypeVar]
    # TYPEHINT NOTE: the value can be handled by the get_fields() method.
    fields: Optional[Tuple[forms.Field, ...]] = None  # type: ignore[assignment]

    def __init__(self, **kwargs: Any) -> None:
        fields = self.get_fields() + (forms.BooleanField(required=False, initial=True),)
        kwargs.setdefault("label", get_extension_name(self.extension_type.oid))
        super().__init__(fields=fields, require_all_fields=False, **kwargs)

    def compress(self, data_list: List[Any]) -> Optional[x509.Extension[ExtensionTypeTypeVar]]:
        if not data_list:
            return None

        *value, critical = data_list
        ext_value = self.get_value(*value)
        if ext_value is None:
            return None
        return x509.Extension(critical=critical, oid=self.extension_type.oid, value=ext_value)

    def get_fields(self) -> Tuple[forms.Field, ...]:
        """Get the form fields used for this extension.

        Note that the `critical` input field is automatically appended.
        """
        if self.fields is not None:  # pragma: no branch
            return self.fields
        raise ValueError(  # pragma: no cover
            "ExtensionField must either set fields or implement get_fields()."
        )

    @abc.abstractmethod
    def get_value(self, *value: Any) -> Optional[ExtensionTypeTypeVar]:
        """Get the extension value from the "compressed" form representation.

        Return `None` if no value was set and the extension should **not** be added.
        """


class MultipleChoiceExtensionField(ExtensionField[ExtensionTypeTypeVar]):
    """Base class for extensions that are basically a multiple choice field (plus critical)."""

    choices = Tuple[Tuple[str, str], ...]
    widget: Type[widgets.MultipleChoiceExtensionWidget]

    def __init__(self, **kwargs: Any) -> None:
        kwargs["widget"] = self.widget(choices=self.choices)
        super().__init__(**kwargs)

    def get_fields(self) -> Tuple[forms.MultipleChoiceField]:
        return (forms.MultipleChoiceField(choices=self.choices, required=False),)

    def get_value(self, value: List[str]) -> Optional[ExtensionTypeTypeVar]:
        if not value:
            return None
        return self.get_values(value)

    @abc.abstractmethod
    def get_values(self, value: List[str]) -> Optional[ExtensionTypeTypeVar]:
        """Get the ExtensionType instance from the selected values."""


class DistributionPointField(ExtensionField[CRLExtensionTypeTypeVar]):
    """Base class for extensions with DistributionPoints."""

    default_error_messages = {
        "full-and-relative-name": _("You cannot provide both full_name and relative_name."),
        "no-dp-or-issuer": _("A DistributionPoint needs at least a full or relative name or a crl issuer."),
    }
    fields = (
        GeneralNamesField(required=False),  # full_name
        RelativeDistinguishedNameField(required=False),  # relative_name
        GeneralNamesField(required=False),  # crl_issuer
        ReasonsField(required=False),  # reasons
    )

    def get_value(
        self,
        full_name: List[x509.GeneralName],
        relative_distinguished_name: Optional[x509.RelativeDistinguishedName],
        crl_issuer: List[x509.GeneralName],
        reasons: Optional[Iterable[str]],
    ) -> Optional[CRLExtensionTypeTypeVar]:
        if not full_name:
            # TYPEHINT NOTE: Field returns empty list, which x509.DistributionPoint() treats different from
            #   None. Any other solution is less efficient, so we don't use them just for mypy.
            full_name = None  # type: ignore[assignment]
        if not crl_issuer:
            crl_issuer = None  # type: ignore[assignment]  # same as above for full_name

        if reasons:
            parsed_reasons = frozenset(x509.ReasonFlags[flag] for flag in reasons)
        else:
            parsed_reasons = None

        if full_name and relative_distinguished_name:
            raise forms.ValidationError(
                self.error_messages["full-and-relative-name"], code="full-and-relative-name"
            )

        if not full_name and not relative_distinguished_name and not crl_issuer:
            if reasons:
                # NOTE: cryptography does not yet validate this on its own:
                #   https://github.com/pyca/cryptography/pull/7710
                raise forms.ValidationError(self.error_messages["no-dp-or-issuer"], code="no-dp-or-issuer")
            return None  # nothing was entered at all

        distribution_point = x509.DistributionPoint(
            full_name=full_name,
            relative_name=relative_distinguished_name,
            crl_issuer=crl_issuer,
            reasons=parsed_reasons,
        )
        return self.extension_type(distribution_points=[distribution_point])


class AuthorityInformationAccessField(ExtensionField[x509.AuthorityInformationAccess]):
    """Form field for a :py:class:`~cg:cryptography.x509.AuthorityInformationAccess` extension."""

    extension_type = x509.AuthorityInformationAccess
    fields = (GeneralNamesField(required=False), GeneralNamesField(required=False))
    widget = widgets.AuthorityInformationAccessWidget

    def get_value(
        self, ca_issuers: List[x509.GeneralName], ocsp: List[x509.GeneralName]
    ) -> Optional[x509.AuthorityInformationAccess]:
        if not ca_issuers and not ocsp:
            return None
        descriptions = []
        if ocsp:
            descriptions += [
                x509.AccessDescription(access_method=AuthorityInformationAccessOID.OCSP, access_location=name)
                for name in ocsp
            ]
        if ca_issuers:
            descriptions += [
                x509.AccessDescription(
                    access_method=AuthorityInformationAccessOID.CA_ISSUERS, access_location=name
                )
                for name in ca_issuers
            ]
        return x509.AuthorityInformationAccess(descriptions=descriptions)


class CertificatePoliciesField(ExtensionField[x509.CertificatePolicies]):
    """Form field for a :py:class:`~cg:cryptography.x509.CertificatePolicies` extension."""

    extension_type = x509.CertificatePolicies
    fields = (
        ObjectIdentifierField(required=False),  # Policy Identifier
        forms.CharField(required=False),
        forms.CharField(required=False),
    )
    widget = widgets.CertificatePoliciesWidget

    def get_value(
        self, policy_identifier: x509.ObjectIdentifier, practice_statements: str, explicit_text: str
    ) -> Optional[x509.CertificatePolicies]:
        if not policy_identifier or not (practice_statements or explicit_text):
            return None

        policy_qualifiers = typing.cast(List[Union[str, x509.UserNotice]], practice_statements.splitlines())
        if explicit_text:
            policy_qualifiers.append(x509.UserNotice(notice_reference=None, explicit_text=explicit_text))

        policy_information = x509.PolicyInformation(
            policy_identifier=policy_identifier, policy_qualifiers=policy_qualifiers
        )
        return x509.CertificatePolicies([policy_information])


class CRLDistributionPointField(DistributionPointField[x509.CRLDistributionPoints]):
    """Form field for a :py:class:`~cg:cryptography.x509.CRLDistributionPoints` extension."""

    extension_type = x509.CRLDistributionPoints
    widget = widgets.CRLDistributionPointsWidget


class ExtendedKeyUsageField(MultipleChoiceExtensionField[x509.ExtendedKeyUsage]):
    """Form field for a :py:class:`~cg:cryptography.x509.ExtendedKeyUsage` extension."""

    extension_type = x509.ExtendedKeyUsage
    choices = _EXTENDED_KEY_USAGE_CHOICES
    widget = widgets.ExtendedKeyUsageWidget

    def get_values(self, value: List[str]) -> Optional[x509.ExtendedKeyUsage]:
        return x509.ExtendedKeyUsage(usages=[_EXTENDED_KEY_USAGE_MAPPING[name] for name in value])


class FreshestCRLField(DistributionPointField[x509.FreshestCRL]):
    """Form field for a :py:class:`~cg:cryptography.x509.CRLDistributionPoints` extension."""

    extension_type = x509.FreshestCRL
    widget = widgets.FreshestCRLWidget


class IssuerAlternativeNameField(ExtensionField[x509.IssuerAlternativeName]):
    """Form field for a :py:class:`~cg:cryptography.x509.IssuerAlternativeName` extension."""

    extension_type = x509.IssuerAlternativeName
    fields = (GeneralNamesField(required=False),)
    widget = widgets.IssuerAlternativeNameWidget

    def get_value(self, value: List[x509.GeneralName]) -> Optional[x509.IssuerAlternativeName]:
        if not value:
            return None
        return x509.IssuerAlternativeName(general_names=value)


class KeyUsageField(MultipleChoiceExtensionField[x509.KeyUsage]):
    """Form field for a :py:class:`~cg:cryptography.x509.KeyUsage` extension."""

    choices = sorted(KEY_USAGE_NAMES.items(), key=lambda t: t[1])

    extension_type = x509.KeyUsage
    widget = widgets.KeyUsageWidget

    def get_values(self, value: List[str]) -> Optional[x509.KeyUsage]:
        values = {choice: choice in value for choice in KEY_USAGE_NAMES}
        return x509.KeyUsage(**values)


class OCSPNoCheckField(ExtensionField[x509.OCSPNoCheck]):
    """Form field for a :py:class:`~cg:cryptography.x509.OCSPNoCheck` extension."""

    extension_type = x509.OCSPNoCheck
    fields = (forms.BooleanField(required=False),)
    widget = widgets.OCSPNoCheckWidget

    def get_value(self, value: bool) -> Optional[x509.OCSPNoCheck]:
        if value is True:
            return self.extension_type()
        return None


class SubjectAlternativeNameField(ExtensionField[x509.SubjectAlternativeName]):
    """Form field for a :py:class:`~cg:cryptography.x509.SubjectAlternativeName` extension."""

    extension_type = x509.SubjectAlternativeName
    fields = (
        GeneralNamesField(required=False),
        forms.BooleanField(required=False),
    )
    widget = widgets.SubjectAlternativeNameWidget

    def compress(  # type: ignore[override]  # this is a special case
        self, data_list: List[Any]
    ) -> Tuple[Optional[x509.Extension[ExtensionTypeTypeVar]], bool]:
        default_cn_in_san = ca_settings.CA_PROFILES[ca_settings.CA_DEFAULT_PROFILE]["cn_in_san"]
        if not data_list:  # pragma: no cover
            return None, default_cn_in_san

        *value, critical = data_list
        ext_value, cn_in_san = self.get_value(*value)
        if ext_value is None:
            return None, cn_in_san
        ext = x509.Extension(critical=critical, oid=self.extension_type.oid, value=ext_value)
        # TYPE NOTE: mypy complains about the non-generic type being returned
        return ext, cn_in_san  # type: ignore[return-value]

    def get_value(  # type: ignore[override]
        self, names: List[x509.GeneralName], cn_in_san: bool
    ) -> Tuple[Optional[x509.SubjectAlternativeName], bool]:
        if not names:
            return None, cn_in_san
        return x509.SubjectAlternativeName(general_names=names), cn_in_san


class TLSFeatureField(MultipleChoiceExtensionField[x509.TLSFeature]):
    """Form field for a :py:class:`~cg:cryptography.x509.TLSFeature` extension."""

    extension_type = x509.TLSFeature
    choices = (
        (x509.TLSFeatureType.status_request.name, "status_request (OCSPMustStaple)"),
        (x509.TLSFeatureType.status_request_v2.name, "status_request_v2 (MultipleCertStatusRequest)"),
    )  # TODO: choices can also be a function - better for testing for completeness
    widget = widgets.TLSFeatureWidget

    def get_values(self, value: List[str]) -> Optional[x509.TLSFeature]:
        # Note: sort value to get predictable output in test cases
        features = [getattr(x509.TLSFeatureType, elem) for elem in sorted(value)]
        return self.extension_type(features=features)
