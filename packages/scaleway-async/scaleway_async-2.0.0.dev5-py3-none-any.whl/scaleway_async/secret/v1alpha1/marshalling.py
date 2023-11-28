# This file was automatically generated. DO NOT EDIT.
# If you have any remark or suggestion do not hesitate to open an issue.

from typing import Any, Dict
from dateutil import parser

from scaleway_core.profile import ProfileDefaults
from .types import (
    Folder,
    SecretVersion,
    Secret,
    AccessSecretVersionResponse,
    ListFoldersResponse,
    ListSecretVersionsResponse,
    ListSecretsResponse,
    ListTagsResponse,
    AddSecretOwnerRequest,
    CreateFolderRequest,
    CreateSecretRequest,
    PasswordGenerationParams,
    CreateSecretVersionRequest,
    GeneratePasswordRequest,
    UpdateSecretRequest,
    UpdateSecretVersionRequest,
)


def unmarshal_Folder(data: Any) -> Folder:
    if not isinstance(data, dict):
        raise TypeError(
            "Unmarshalling the type 'Folder' failed as data isn't a dictionary."
        )

    args: Dict[str, Any] = {}

    field = data.get("id", None)
    args["id"] = field

    field = data.get("project_id", None)
    args["project_id"] = field

    field = data.get("name", None)
    args["name"] = field

    field = data.get("path", None)
    args["path"] = field

    field = data.get("region", None)
    args["region"] = field

    field = data.get("created_at", None)
    args["created_at"] = parser.isoparse(field) if isinstance(field, str) else field

    return Folder(**args)


def unmarshal_SecretVersion(data: Any) -> SecretVersion:
    if not isinstance(data, dict):
        raise TypeError(
            "Unmarshalling the type 'SecretVersion' failed as data isn't a dictionary."
        )

    args: Dict[str, Any] = {}

    field = data.get("revision", None)
    args["revision"] = field

    field = data.get("secret_id", None)
    args["secret_id"] = field

    field = data.get("status", None)
    args["status"] = field

    field = data.get("is_latest", None)
    args["is_latest"] = field

    field = data.get("created_at", None)
    args["created_at"] = parser.isoparse(field) if isinstance(field, str) else field

    field = data.get("updated_at", None)
    args["updated_at"] = parser.isoparse(field) if isinstance(field, str) else field

    field = data.get("description", None)
    args["description"] = field

    return SecretVersion(**args)


def unmarshal_Secret(data: Any) -> Secret:
    if not isinstance(data, dict):
        raise TypeError(
            "Unmarshalling the type 'Secret' failed as data isn't a dictionary."
        )

    args: Dict[str, Any] = {}

    field = data.get("id", None)
    args["id"] = field

    field = data.get("project_id", None)
    args["project_id"] = field

    field = data.get("name", None)
    args["name"] = field

    field = data.get("status", None)
    args["status"] = field

    field = data.get("tags", None)
    args["tags"] = field

    field = data.get("version_count", None)
    args["version_count"] = field

    field = data.get("is_managed", None)
    args["is_managed"] = field

    field = data.get("is_protected", None)
    args["is_protected"] = field

    field = data.get("type_", None)
    args["type_"] = field

    field = data.get("path", None)
    args["path"] = field

    field = data.get("ephemeral_action", None)
    args["ephemeral_action"] = field

    field = data.get("region", None)
    args["region"] = field

    field = data.get("created_at", None)
    args["created_at"] = parser.isoparse(field) if isinstance(field, str) else field

    field = data.get("updated_at", None)
    args["updated_at"] = parser.isoparse(field) if isinstance(field, str) else field

    field = data.get("description", None)
    args["description"] = field

    field = data.get("expires_at", None)
    args["expires_at"] = parser.isoparse(field) if isinstance(field, str) else field

    return Secret(**args)


def unmarshal_AccessSecretVersionResponse(data: Any) -> AccessSecretVersionResponse:
    if not isinstance(data, dict):
        raise TypeError(
            "Unmarshalling the type 'AccessSecretVersionResponse' failed as data isn't a dictionary."
        )

    args: Dict[str, Any] = {}

    field = data.get("secret_id", None)
    args["secret_id"] = field

    field = data.get("revision", None)
    args["revision"] = field

    field = data.get("data", None)
    args["data"] = field

    field = data.get("data_crc32", None)
    args["data_crc32"] = field

    return AccessSecretVersionResponse(**args)


def unmarshal_ListFoldersResponse(data: Any) -> ListFoldersResponse:
    if not isinstance(data, dict):
        raise TypeError(
            "Unmarshalling the type 'ListFoldersResponse' failed as data isn't a dictionary."
        )

    args: Dict[str, Any] = {}

    field = data.get("folders", None)
    args["folders"] = (
        [unmarshal_Folder(v) for v in field] if field is not None else None
    )

    field = data.get("total_count", None)
    args["total_count"] = field

    return ListFoldersResponse(**args)


def unmarshal_ListSecretVersionsResponse(data: Any) -> ListSecretVersionsResponse:
    if not isinstance(data, dict):
        raise TypeError(
            "Unmarshalling the type 'ListSecretVersionsResponse' failed as data isn't a dictionary."
        )

    args: Dict[str, Any] = {}

    field = data.get("versions", None)
    args["versions"] = (
        [unmarshal_SecretVersion(v) for v in field] if field is not None else None
    )

    field = data.get("total_count", None)
    args["total_count"] = field

    return ListSecretVersionsResponse(**args)


def unmarshal_ListSecretsResponse(data: Any) -> ListSecretsResponse:
    if not isinstance(data, dict):
        raise TypeError(
            "Unmarshalling the type 'ListSecretsResponse' failed as data isn't a dictionary."
        )

    args: Dict[str, Any] = {}

    field = data.get("secrets", None)
    args["secrets"] = (
        [unmarshal_Secret(v) for v in field] if field is not None else None
    )

    field = data.get("total_count", None)
    args["total_count"] = field

    return ListSecretsResponse(**args)


def unmarshal_ListTagsResponse(data: Any) -> ListTagsResponse:
    if not isinstance(data, dict):
        raise TypeError(
            "Unmarshalling the type 'ListTagsResponse' failed as data isn't a dictionary."
        )

    args: Dict[str, Any] = {}

    field = data.get("tags", None)
    args["tags"] = field

    field = data.get("total_count", None)
    args["total_count"] = field

    return ListTagsResponse(**args)


def marshal_AddSecretOwnerRequest(
    request: AddSecretOwnerRequest,
    defaults: ProfileDefaults,
) -> Dict[str, Any]:
    output: Dict[str, Any] = {}

    if request.product_name is not None:
        output["product_name"] = request.product_name

    if request.product is not None:
        output["product"] = str(request.product)

    return output


def marshal_CreateFolderRequest(
    request: CreateFolderRequest,
    defaults: ProfileDefaults,
) -> Dict[str, Any]:
    output: Dict[str, Any] = {}

    if request.name is not None:
        output["name"] = request.name

    if request.project_id is not None:
        output["project_id"] = request.project_id or defaults.default_project_id

    if request.path is not None:
        output["path"] = request.path

    return output


def marshal_CreateSecretRequest(
    request: CreateSecretRequest,
    defaults: ProfileDefaults,
) -> Dict[str, Any]:
    output: Dict[str, Any] = {}

    if request.name is not None:
        output["name"] = request.name

    if request.project_id is not None:
        output["project_id"] = request.project_id or defaults.default_project_id

    if request.tags is not None:
        output["tags"] = request.tags

    if request.description is not None:
        output["description"] = request.description

    if request.type_ is not None:
        output["type"] = str(request.type_)

    if request.path is not None:
        output["path"] = request.path

    if request.expires_at is not None:
        output["expires_at"] = request.expires_at

    if request.ephemeral_action is not None:
        output["ephemeral_action"] = str(request.ephemeral_action)

    return output


def marshal_PasswordGenerationParams(
    request: PasswordGenerationParams,
    defaults: ProfileDefaults,
) -> Dict[str, Any]:
    output: Dict[str, Any] = {}

    if request.length is not None:
        output["length"] = request.length

    if request.no_lowercase_letters is not None:
        output["no_lowercase_letters"] = request.no_lowercase_letters

    if request.no_uppercase_letters is not None:
        output["no_uppercase_letters"] = request.no_uppercase_letters

    if request.no_digits is not None:
        output["no_digits"] = request.no_digits

    if request.additional_chars is not None:
        output["additional_chars"] = request.additional_chars

    return output


def marshal_CreateSecretVersionRequest(
    request: CreateSecretVersionRequest,
    defaults: ProfileDefaults,
) -> Dict[str, Any]:
    output: Dict[str, Any] = {}

    if request.data is not None:
        output["data"] = request.data

    if request.description is not None:
        output["description"] = request.description

    if request.disable_previous is not None:
        output["disable_previous"] = request.disable_previous

    if request.password_generation is not None:
        output["password_generation"] = (
            marshal_PasswordGenerationParams(request.password_generation, defaults),
        )

    if request.data_crc32 is not None:
        output["data_crc32"] = request.data_crc32

    return output


def marshal_GeneratePasswordRequest(
    request: GeneratePasswordRequest,
    defaults: ProfileDefaults,
) -> Dict[str, Any]:
    output: Dict[str, Any] = {}

    if request.length is not None:
        output["length"] = request.length

    if request.description is not None:
        output["description"] = request.description

    if request.disable_previous is not None:
        output["disable_previous"] = request.disable_previous

    if request.no_lowercase_letters is not None:
        output["no_lowercase_letters"] = request.no_lowercase_letters

    if request.no_uppercase_letters is not None:
        output["no_uppercase_letters"] = request.no_uppercase_letters

    if request.no_digits is not None:
        output["no_digits"] = request.no_digits

    if request.additional_chars is not None:
        output["additional_chars"] = request.additional_chars

    return output


def marshal_UpdateSecretRequest(
    request: UpdateSecretRequest,
    defaults: ProfileDefaults,
) -> Dict[str, Any]:
    output: Dict[str, Any] = {}

    if request.name is not None:
        output["name"] = request.name

    if request.tags is not None:
        output["tags"] = request.tags

    if request.description is not None:
        output["description"] = request.description

    if request.path is not None:
        output["path"] = request.path

    return output


def marshal_UpdateSecretVersionRequest(
    request: UpdateSecretVersionRequest,
    defaults: ProfileDefaults,
) -> Dict[str, Any]:
    output: Dict[str, Any] = {}

    if request.description is not None:
        output["description"] = request.description

    return output
