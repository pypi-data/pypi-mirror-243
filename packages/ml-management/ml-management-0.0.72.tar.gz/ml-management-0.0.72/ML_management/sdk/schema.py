import sgqlc.types

my_schema = sgqlc.types.Schema()


__docformat__ = "markdown"


########################################################################
# Scalars and Enumerations
########################################################################
class AttributeType(sgqlc.types.Enum):
    """Enumeration Choices:

    * `boolean`None
    * `booleanList`None
    * `double`None
    * `doubleList`None
    * `int`None
    * `intList`None
    * `string`None
    * `stringList`None
    """

    __schema__ = my_schema
    __choices__ = ("boolean", "booleanList", "double", "doubleList", "int", "intList", "string", "stringList")


Boolean = sgqlc.types.Boolean


class CombiningAlgorithm(sgqlc.types.Enum):
    """Enumeration Choices:

    * `and`None
    * `or`None
    """

    __schema__ = my_schema
    __choices__ = ("and", "or")


class ExecutorMethodName(sgqlc.types.Enum):
    """Enumeration Choices:

    * `execute`None
    """

    __schema__ = my_schema
    __choices__ = ("execute",)


Float = sgqlc.types.Float

ID = sgqlc.types.ID

Int = sgqlc.types.Int


class JSON(sgqlc.types.Scalar):
    __schema__ = my_schema


class JobStatus(sgqlc.types.Enum):
    """Enumeration Choices:

    * `BUILDING`None
    * `EXECUTING`None
    * `FAILED`None
    * `PLANNED`None
    * `SUCCESSFUL`None
    """

    __schema__ = my_schema
    __choices__ = ("BUILDING", "EXECUTING", "FAILED", "PLANNED", "SUCCESSFUL")


class LONG(sgqlc.types.Scalar):
    """The `LONG` scalar type represents long int type."""

    __schema__ = my_schema


class Long(sgqlc.types.Scalar):
    """The `Long` scalar type represents non-fractional signed whole
    numeric values. Long can represent values between -(2^63) and 2^63
    - 1.
    """

    __schema__ = my_schema


class PeriodicType(sgqlc.types.Enum):
    """Enumeration Choices:

    * `ONCE`None
    * `PERIODIC`None
    """

    __schema__ = my_schema
    __choices__ = ("ONCE", "PERIODIC")


class RuleType(sgqlc.types.Enum):
    """Enumeration Choices:

    * `filter`None
    * `local`None
    """

    __schema__ = my_schema
    __choices__ = ("filter", "local")


String = sgqlc.types.String


class UnixTime(sgqlc.types.Scalar):
    __schema__ = my_schema


class UploadModelType(sgqlc.types.Enum):
    """Enumeration Choices:

    * `new_model`None
    * `new_version`None
    * `root`None
    """

    __schema__ = my_schema
    __choices__ = ("new_model", "new_version", "root")


########################################################################
# Input Objects
########################################################################
class AddUserGroupMembersParams(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("user_ids", "group_ids")
    user_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name="userIds")

    group_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name="groupIds")


class AttributeFilterSettings(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("id", "name")
    id = sgqlc.types.Field(String, graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")


class AttributesResultInputs(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = (
        "int_attributes",
        "string_attributes",
        "double_attributes",
        "boolean_attributes",
        "int_list_attributes",
        "string_list_attributes",
        "double_list_attributes",
        "boolean_list_attributes",
    )
    int_attributes = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null("IntAttributeResult")), graphql_name="intAttributes")

    string_attributes = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("StringAttributeResult")), graphql_name="stringAttributes"
    )

    double_attributes = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("DoubleAttributeResult")), graphql_name="doubleAttributes"
    )

    boolean_attributes = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("BooleanAttributeResult")), graphql_name="booleanAttributes"
    )

    int_list_attributes = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("IntListAttributeResult")), graphql_name="intListAttributes"
    )

    string_list_attributes = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("StringListAttributeResult")), graphql_name="stringListAttributes"
    )

    double_list_attributes = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("DoubleListAttributeResult")), graphql_name="doubleListAttributes"
    )

    boolean_list_attributes = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null("BooleanListAttributeResult")), graphql_name="booleanListAttributes"
    )


class BooleanAttributeResult(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("name", "value")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    value = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="value")


class BooleanListAttributeResult(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("name", "value")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    value = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Boolean))), graphql_name="value")


class CreateUserGroupParams(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("name", "description")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    description = sgqlc.types.Field(String, graphql_name="description")


class CreateUserParams(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = (
        "login",
        "first_name",
        "last_name",
        "fathers_name",
        "email",
        "access_level_id",
        "is_admin",
        "enabled",
        "receive_notifications",
        "receive_telegram_notifications",
        "telegram_chat_id",
    )
    login = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="login")

    first_name = sgqlc.types.Field(String, graphql_name="firstName")

    last_name = sgqlc.types.Field(String, graphql_name="lastName")

    fathers_name = sgqlc.types.Field(String, graphql_name="fathersName")

    email = sgqlc.types.Field(String, graphql_name="email")

    access_level_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="accessLevelID")

    is_admin = sgqlc.types.Field(Boolean, graphql_name="isAdmin")

    enabled = sgqlc.types.Field(Boolean, graphql_name="enabled")

    receive_notifications = sgqlc.types.Field(Boolean, graphql_name="receiveNotifications")

    receive_telegram_notifications = sgqlc.types.Field(Boolean, graphql_name="receiveTelegramNotifications")

    telegram_chat_id = sgqlc.types.Field(Long, graphql_name="telegramChatId")


class DataParamsInput(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("dataset_loader_version_choice", "collector_name", "dataset_loader_method_params", "collector_method_params")
    dataset_loader_version_choice = sgqlc.types.Field(
        sgqlc.types.non_null("ObjectVersionOptionalInput"), graphql_name="datasetLoaderVersionChoice"
    )

    collector_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="collectorName")

    dataset_loader_method_params = sgqlc.types.Field(sgqlc.types.non_null("MethodParamsInput"), graphql_name="datasetLoaderMethodParams")

    collector_method_params = sgqlc.types.Field(sgqlc.types.non_null("MethodParamsInput"), graphql_name="collectorMethodParams")


class DeleteUserGroupMemberParams(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("user_id", "group_id")
    user_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="userId")

    group_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="groupId")


class DoubleAttributeResult(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("name", "value")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    value = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name="value")


class DoubleListAttributeResult(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("name", "value")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    value = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Float))), graphql_name="value")


class ExecutorParamsInput(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("executor_version_choice", "executor_method_params")
    executor_version_choice = sgqlc.types.Field(sgqlc.types.non_null("ObjectVersionOptionalInput"), graphql_name="executorVersionChoice")

    executor_method_params = sgqlc.types.Field(sgqlc.types.non_null("MethodParamsInput"), graphql_name="executorMethodParams")


class IntAttributeResult(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("name", "value")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    value = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="value")


class IntListAttributeResult(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("name", "value")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    value = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Int))), graphql_name="value")


class JobParameters(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = (
        "executor_params",
        "list_role_model_params",
        "data_params",
        "experiment_name",
        "cron_expression",
        "periodic_type",
        "force_rebuild",
        "gpu",
    )
    executor_params = sgqlc.types.Field(sgqlc.types.non_null(ExecutorParamsInput), graphql_name="executorParams")

    list_role_model_params = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RoleModelParamsInput"))), graphql_name="listRoleModelParams"
    )

    data_params = sgqlc.types.Field(sgqlc.types.non_null(DataParamsInput), graphql_name="dataParams")

    experiment_name = sgqlc.types.Field(String, graphql_name="experimentName")

    cron_expression = sgqlc.types.Field(String, graphql_name="cronExpression")

    periodic_type = sgqlc.types.Field(PeriodicType, graphql_name="periodicType")

    force_rebuild = sgqlc.types.Field(Boolean, graphql_name="forceRebuild")

    gpu = sgqlc.types.Field(Boolean, graphql_name="gpu")


class JobSingleParameters(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = (
        "executor_params",
        "model_params",
        "data_params",
        "experiment_name",
        "cron_expression",
        "periodic_type",
        "force_rebuild",
        "gpu",
    )
    executor_params = sgqlc.types.Field(sgqlc.types.non_null(ExecutorParamsInput), graphql_name="executorParams")

    model_params = sgqlc.types.Field(sgqlc.types.non_null("ModelParamsInput"), graphql_name="modelParams")

    data_params = sgqlc.types.Field(sgqlc.types.non_null(DataParamsInput), graphql_name="dataParams")

    experiment_name = sgqlc.types.Field(String, graphql_name="experimentName")

    cron_expression = sgqlc.types.Field(String, graphql_name="cronExpression")

    periodic_type = sgqlc.types.Field(PeriodicType, graphql_name="periodicType")

    force_rebuild = sgqlc.types.Field(Boolean, graphql_name="forceRebuild")

    gpu = sgqlc.types.Field(Boolean, graphql_name="gpu")


class MethodParamsInput(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("method_name", "method_params")
    method_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="methodName")

    method_params = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="methodParams")


class ModelParamsInput(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("model_version_choice", "list_model_method_params", "new_model_name")
    model_version_choice = sgqlc.types.Field(sgqlc.types.non_null("ModelVersionChoice"), graphql_name="modelVersionChoice")

    list_model_method_params = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MethodParamsInput))), graphql_name="listModelMethodParams"
    )

    new_model_name = sgqlc.types.Field(String, graphql_name="newModelName")


class ModelVersionChoice(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("name", "version", "choice_criteria", "metric_name", "optimal_min")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    version = sgqlc.types.Field(Int, graphql_name="version")

    choice_criteria = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="choiceCriteria")

    metric_name = sgqlc.types.Field(String, graphql_name="metricName")

    optimal_min = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="optimalMin")


class ObjectVersionInput(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("name", "version")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="version")


class ObjectVersionOptionalInput(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("name", "version")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    version = sgqlc.types.Field(Int, graphql_name="version")


class PolicyParameterArg(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("param", "parameter_type")
    param = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="param")

    parameter_type = sgqlc.types.Field(sgqlc.types.non_null(AttributeType), graphql_name="parameterType")


class RoleModelParamsInput(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("role", "model_params")
    role = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="role")

    model_params = sgqlc.types.Field(sgqlc.types.non_null(ModelParamsInput), graphql_name="modelParams")


class RoleModelVersionInput(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("role", "model")
    role = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="role")

    model = sgqlc.types.Field(sgqlc.types.non_null(ObjectVersionInput), graphql_name="model")


class SecurityPolicyArg(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("id", "name", "target", "params", "security_entity_idlist", "combining_algorithm")
    id = sgqlc.types.Field(Long, graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    target = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="target")

    params = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(PolicyParameterArg))), graphql_name="params")

    security_entity_idlist = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Long))), graphql_name="securityEntityIDList"
    )

    combining_algorithm = sgqlc.types.Field(sgqlc.types.non_null(CombiningAlgorithm), graphql_name="combiningAlgorithm")


class SecurityRuleArg(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("id", "name", "target", "rule_type", "rule", "params", "source")
    id = sgqlc.types.Field(Long, graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    target = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="target")

    rule_type = sgqlc.types.Field(sgqlc.types.non_null(RuleType), graphql_name="ruleType")

    rule = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="rule")

    params = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(PolicyParameterArg))), graphql_name="params")

    source = sgqlc.types.Field(String, graphql_name="source")


class StringAttributeResult(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("name", "value")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="value")


class StringListAttributeResult(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("name", "value")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    value = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name="value")


class TimestampInterval(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("start", "end")
    start = sgqlc.types.Field(UnixTime, graphql_name="start")

    end = sgqlc.types.Field(UnixTime, graphql_name="end")


class UpdateCurrentUserParams(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = (
        "first_name",
        "last_name",
        "fathers_name",
        "email",
        "password",
        "receive_notifications",
        "receive_telegram_notifications",
        "telegram_chat_id",
    )
    first_name = sgqlc.types.Field(String, graphql_name="firstName")

    last_name = sgqlc.types.Field(String, graphql_name="lastName")

    fathers_name = sgqlc.types.Field(String, graphql_name="fathersName")

    email = sgqlc.types.Field(String, graphql_name="email")

    password = sgqlc.types.Field(String, graphql_name="password")

    receive_notifications = sgqlc.types.Field(Boolean, graphql_name="receiveNotifications")

    receive_telegram_notifications = sgqlc.types.Field(Boolean, graphql_name="receiveTelegramNotifications")

    telegram_chat_id = sgqlc.types.Field(Long, graphql_name="telegramChatId")


class UpdateUserGroupParams(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("name", "description")
    name = sgqlc.types.Field(String, graphql_name="name")

    description = sgqlc.types.Field(String, graphql_name="description")


class UpdateUserParams(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = (
        "first_name",
        "last_name",
        "fathers_name",
        "email",
        "access_level_id",
        "is_admin",
        "enabled",
        "receive_notifications",
        "receive_telegram_notifications",
        "telegram_chat_id",
    )
    first_name = sgqlc.types.Field(String, graphql_name="firstName")

    last_name = sgqlc.types.Field(String, graphql_name="lastName")

    fathers_name = sgqlc.types.Field(String, graphql_name="fathersName")

    email = sgqlc.types.Field(String, graphql_name="email")

    access_level_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="accessLevelID")

    is_admin = sgqlc.types.Field(Boolean, graphql_name="isAdmin")

    enabled = sgqlc.types.Field(Boolean, graphql_name="enabled")

    receive_notifications = sgqlc.types.Field(Boolean, graphql_name="receiveNotifications")

    receive_telegram_notifications = sgqlc.types.Field(Boolean, graphql_name="receiveTelegramNotifications")

    telegram_chat_id = sgqlc.types.Field(Long, graphql_name="telegramChatId")


class UserAttributeInput(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("id", "json_value")
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="id")

    json_value = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="jsonValue")


class UserFilterSettings(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = (
        "query",
        "user_id",
        "login",
        "first_name",
        "last_name",
        "fathers_name",
        "email",
        "enabled",
        "group_ids",
        "creator",
        "last_updater",
        "creation_date",
        "update_date",
    )
    query = sgqlc.types.Field(String, graphql_name="query")

    user_id = sgqlc.types.Field(ID, graphql_name="userId")

    login = sgqlc.types.Field(String, graphql_name="login")

    first_name = sgqlc.types.Field(String, graphql_name="firstName")

    last_name = sgqlc.types.Field(String, graphql_name="lastName")

    fathers_name = sgqlc.types.Field(String, graphql_name="fathersName")

    email = sgqlc.types.Field(String, graphql_name="email")

    enabled = sgqlc.types.Field(Boolean, graphql_name="enabled")

    group_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name="groupIds")

    creator = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name="creator")

    last_updater = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name="lastUpdater")

    creation_date = sgqlc.types.Field(TimestampInterval, graphql_name="creationDate")
    """Creation date [start; end]"""

    update_date = sgqlc.types.Field(TimestampInterval, graphql_name="updateDate")
    """Latest update date [start; end]"""


class UserGroupFilterSettings(sgqlc.types.Input):
    __schema__ = my_schema
    __field_names__ = ("query", "name", "description", "user_ids", "creator", "last_updater", "creation_date", "update_date")
    query = sgqlc.types.Field(String, graphql_name="query")

    name = sgqlc.types.Field(String, graphql_name="name")

    description = sgqlc.types.Field(String, graphql_name="description")

    user_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name="userIds")

    creator = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name="creator")

    last_updater = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name="lastUpdater")

    creation_date = sgqlc.types.Field(TimestampInterval, graphql_name="creationDate")
    """Creation date [start; end]"""

    update_date = sgqlc.types.Field(TimestampInterval, graphql_name="updateDate")
    """Latest update date [start; end]"""


########################################################################
# Output Objects and Interfaces
########################################################################
class RecordInterface(sgqlc.types.Interface):
    """Common part of all records"""

    __schema__ = my_schema
    __field_names__ = ("system_registration_date", "system_update_date", "creator", "last_updater")
    system_registration_date = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name="systemRegistrationDate")

    system_update_date = sgqlc.types.Field(UnixTime, graphql_name="systemUpdateDate")

    creator = sgqlc.types.Field(sgqlc.types.non_null("User"), graphql_name="creator")

    last_updater = sgqlc.types.Field("User", graphql_name="lastUpdater")


class AccessLevel(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("id", "name", "order")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    order = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name="order")


class Attribute(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("id", "name", "value_type", "params_schema")
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    value_type = sgqlc.types.Field(sgqlc.types.non_null(AttributeType), graphql_name="valueType")

    params_schema = sgqlc.types.Field(sgqlc.types.non_null("ParamsSchema"), graphql_name="paramsSchema")


class AttributePagination(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("list_attribute", "total")
    list_attribute = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Attribute))), graphql_name="listAttribute"
    )

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class BooleanListValue(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("value",)
    value = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Boolean))), graphql_name="value")


class BooleanResultGQL(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("id", "value")
    id = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name="id")

    value = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="value")


class BooleanValue(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("value",)
    value = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="value")


class ConflictsState(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("user_conflicts", "group_conflicts")
    user_conflicts = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Boolean)), graphql_name="userConflicts")

    group_conflicts = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Boolean)), graphql_name="groupConflicts")


class DataParams(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "dataset_loader_name",
        "dataset_loader_version",
        "collector_name",
        "dataset_loader_method_params",
        "collector_method_params",
    )
    dataset_loader_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="datasetLoaderName")

    dataset_loader_version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="datasetLoaderVersion")

    collector_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="collectorName")

    dataset_loader_method_params = sgqlc.types.Field(sgqlc.types.non_null("MethodParams"), graphql_name="datasetLoaderMethodParams")

    collector_method_params = sgqlc.types.Field(sgqlc.types.non_null("MethodParams"), graphql_name="collectorMethodParams")


class DataSchema(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("dataset_loader_method_schema", "collector_method_schema")
    dataset_loader_method_schema = sgqlc.types.Field(sgqlc.types.non_null("MethodSchema"), graphql_name="datasetLoaderMethodSchema")

    collector_method_schema = sgqlc.types.Field(sgqlc.types.non_null("MethodSchema"), graphql_name="collectorMethodSchema")


class DatasetLoader(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "name",
        "description",
        "tags",
        "creation_timestamp",
        "last_updated_timestamp",
        "owner",
        "latest_dataset_loader_version",
        "init_dataset_loader_version",
        "list_dataset_loader_version",
        "pagination_dataset_loader_version",
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="name")

    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="description")

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="tags")

    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="creationTimestamp")

    last_updated_timestamp = sgqlc.types.Field(LONG, graphql_name="lastUpdatedTimestamp")

    owner = sgqlc.types.Field(sgqlc.types.non_null("User"), graphql_name="owner")

    latest_dataset_loader_version = sgqlc.types.Field(
        sgqlc.types.non_null("DatasetLoaderVersion"), graphql_name="latestDatasetLoaderVersion"
    )

    init_dataset_loader_version = sgqlc.types.Field(sgqlc.types.non_null("DatasetLoaderVersion"), graphql_name="initDatasetLoaderVersion")

    list_dataset_loader_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("DatasetLoaderVersion"))), graphql_name="listDatasetLoaderVersion"
    )

    pagination_dataset_loader_version = sgqlc.types.Field(
        sgqlc.types.non_null("DatasetLoaderVersionPagination"),
        graphql_name="paginationDatasetLoaderVersion",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """


class DatasetLoaderPagination(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("list_dataset_loader", "total")
    list_dataset_loader = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DatasetLoader))), graphql_name="listDatasetLoader"
    )

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class DatasetLoaderVersion(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "name",
        "version",
        "source_path",
        "tags",
        "description",
        "status",
        "status_message",
        "creation_timestamp",
        "last_updated_timestamp",
        "dataset_loader_method_schema",
        "dataset_loader_method_schema_name",
        "run",
        "dataset_loader",
        "data_json_schema",
        "list_deployed_jobs",
        "pagination_deployed_jobs",
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="version")

    source_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="sourcePath")

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="tags")

    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="description")

    status = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="status")

    status_message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="statusMessage")

    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="creationTimestamp")

    last_updated_timestamp = sgqlc.types.Field(LONG, graphql_name="lastUpdatedTimestamp")

    dataset_loader_method_schema = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="datasetLoaderMethodSchema")

    dataset_loader_method_schema_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="datasetLoaderMethodSchemaName")

    run = sgqlc.types.Field(sgqlc.types.non_null("Run"), graphql_name="run")

    dataset_loader = sgqlc.types.Field(sgqlc.types.non_null(DatasetLoader), graphql_name="datasetLoader")

    data_json_schema = sgqlc.types.Field(
        sgqlc.types.non_null(DataSchema),
        graphql_name="dataJsonSchema",
        args=sgqlc.types.ArgDict(
            (("collector_name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="collectorName", default=None)),)
        ),
    )
    """Arguments:

    * `collector_name` (`String!`)None
    """

    list_deployed_jobs = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Job"))), graphql_name="listDeployedJobs"
    )

    pagination_deployed_jobs = sgqlc.types.Field(
        sgqlc.types.non_null("JobPagination"),
        graphql_name="paginationDeployedJobs",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """


class DatasetLoaderVersionPagination(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("list_dataset_loader_version", "total")
    list_dataset_loader_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DatasetLoaderVersion))), graphql_name="listDatasetLoaderVersion"
    )

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class DoubleListValue(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("value",)
    value = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Float))), graphql_name="value")


class DoubleValue(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("value",)
    value = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name="value")


class EvaluationResultGQL(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("node_list",)
    node_list = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("EvaluationNodeGQL"))), graphql_name="nodeList"
    )


class Executor(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "name",
        "description",
        "tags",
        "creation_timestamp",
        "last_updated_timestamp",
        "owner",
        "latest_executor_version",
        "init_executor_version",
        "list_executor_version",
        "pagination_executor_version",
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="name")

    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="description")

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="tags")

    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="creationTimestamp")

    last_updated_timestamp = sgqlc.types.Field(LONG, graphql_name="lastUpdatedTimestamp")

    owner = sgqlc.types.Field(sgqlc.types.non_null("User"), graphql_name="owner")

    latest_executor_version = sgqlc.types.Field(sgqlc.types.non_null("ExecutorVersion"), graphql_name="latestExecutorVersion")

    init_executor_version = sgqlc.types.Field(sgqlc.types.non_null("ExecutorVersion"), graphql_name="initExecutorVersion")

    list_executor_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ExecutorVersion"))), graphql_name="listExecutorVersion"
    )

    pagination_executor_version = sgqlc.types.Field(
        sgqlc.types.non_null("ExecutorVersionPagination"),
        graphql_name="paginationExecutorVersion",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """


class ExecutorPagination(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("list_executor", "total")
    list_executor = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Executor))), graphql_name="listExecutor"
    )

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class ExecutorParams(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("name", "version", "executor_method_params")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="version")

    executor_method_params = sgqlc.types.Field(sgqlc.types.non_null("MethodParams"), graphql_name="executorMethodParams")


class ExecutorVersion(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "name",
        "version",
        "source_path",
        "tags",
        "description",
        "status",
        "status_message",
        "creation_timestamp",
        "last_updated_timestamp",
        "executor_method_schema",
        "executor_method_schema_name",
        "desired_model_methods",
        "upload_model_modes",
        "desired_model_patterns",
        "run",
        "executor",
        "list_deployed_jobs",
        "pagination_deployed_jobs",
        "job_json_schema",
        "available_model_versions",
        "pagination_available_model_versions",
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="version")

    source_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="sourcePath")

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="tags")

    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="description")

    status = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="status")

    status_message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="statusMessage")

    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="creationTimestamp")

    last_updated_timestamp = sgqlc.types.Field(LONG, graphql_name="lastUpdatedTimestamp")

    executor_method_schema = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="executorMethodSchema")

    executor_method_schema_name = sgqlc.types.Field(sgqlc.types.non_null(ExecutorMethodName), graphql_name="executorMethodSchemaName")

    desired_model_methods = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="desiredModelMethods")

    upload_model_modes = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="uploadModelModes")

    desired_model_patterns = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="desiredModelPatterns")

    run = sgqlc.types.Field(sgqlc.types.non_null("Run"), graphql_name="run")

    executor = sgqlc.types.Field(sgqlc.types.non_null(Executor), graphql_name="executor")

    list_deployed_jobs = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Job"))), graphql_name="listDeployedJobs"
    )

    pagination_deployed_jobs = sgqlc.types.Field(
        sgqlc.types.non_null("JobPagination"),
        graphql_name="paginationDeployedJobs",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    job_json_schema = sgqlc.types.Field(
        sgqlc.types.non_null("JobSchema"),
        graphql_name="jobJsonSchema",
        args=sgqlc.types.ArgDict(
            (
                (
                    "models",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(RoleModelVersionInput))),
                        graphql_name="models",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `models` (`[RoleModelVersionInput!]!`)None
    """

    available_model_versions = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ModelVersion"))),
        graphql_name="availableModelVersions",
        args=sgqlc.types.ArgDict((("role", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="role", default=None)),)),
    )
    """Arguments:

    * `role` (`String!`)None
    """

    pagination_available_model_versions = sgqlc.types.Field(
        sgqlc.types.non_null("ModelVersionPagination"),
        graphql_name="paginationAvailableModelVersions",
        args=sgqlc.types.ArgDict(
            (
                ("role", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="role", default=None)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `role` (`String!`)None
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """


class ExecutorVersionPagination(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("list_executor_version", "total")
    list_executor_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ExecutorVersion))), graphql_name="listExecutorVersion"
    )

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class Experiment(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("name", "experiment_id", "artifact_location", "lifecycle_stage", "list_run", "pagination_run", "tags")
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    experiment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="experimentId")

    artifact_location = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="artifactLocation")

    lifecycle_stage = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="lifecycleStage")

    list_run = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Run"))), graphql_name="listRun")

    pagination_run = sgqlc.types.Field(
        sgqlc.types.non_null("RunPagination"),
        graphql_name="paginationRun",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="tags")


class ExperimentPagination(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("list_experiment", "total")
    list_experiment = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Experiment))), graphql_name="listExperiment"
    )

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class FilterResultGQL(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("id", "rule", "params", "source")
    id = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name="id")

    rule = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="rule")

    params = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("PolicyParameterGQL"))), graphql_name="params")

    source = sgqlc.types.Field(String, graphql_name="source")


class GraphNode(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "run_id",
        "name",
        "version",
        "source_run_id",
        "source_name",
        "source_version",
        "root_run_id",
        "upload_model_type",
        "list_next_node",
    )
    run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="runId")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="version")

    source_run_id = sgqlc.types.Field(ID, graphql_name="sourceRunId")

    source_name = sgqlc.types.Field(String, graphql_name="sourceName")

    source_version = sgqlc.types.Field(String, graphql_name="sourceVersion")

    root_run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="rootRunId")

    upload_model_type = sgqlc.types.Field(sgqlc.types.non_null(UploadModelType), graphql_name="uploadModelType")

    list_next_node = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null("GraphNode")), graphql_name="listNextNode")


class IntListValue(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("value",)
    value = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Int))), graphql_name="value")


class IntValue(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("value",)
    value = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="value")


class Job(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "name",
        "periodic_type",
        "status",
        "registration_timestamp",
        "start_timestamp",
        "end_timestamp",
        "start_build_timestamp",
        "end_build_timestamp",
        "exception",
        "params",
        "run",
        "experiment",
        "list_init_role_model_version",
        "dataset_loader_version",
        "executor_version",
        "list_result_model_version",
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="name")

    periodic_type = sgqlc.types.Field(sgqlc.types.non_null(PeriodicType), graphql_name="periodicType")

    status = sgqlc.types.Field(sgqlc.types.non_null(JobStatus), graphql_name="status")

    registration_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="registrationTimestamp")

    start_timestamp = sgqlc.types.Field(LONG, graphql_name="startTimestamp")

    end_timestamp = sgqlc.types.Field(LONG, graphql_name="endTimestamp")

    start_build_timestamp = sgqlc.types.Field(LONG, graphql_name="startBuildTimestamp")

    end_build_timestamp = sgqlc.types.Field(LONG, graphql_name="endBuildTimestamp")

    exception = sgqlc.types.Field(String, graphql_name="exception")

    params = sgqlc.types.Field(sgqlc.types.non_null("JobParams"), graphql_name="params")

    run = sgqlc.types.Field("Run", graphql_name="run")

    experiment = sgqlc.types.Field(Experiment, graphql_name="experiment")

    list_init_role_model_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RoleModelVersion"))), graphql_name="listInitRoleModelVersion"
    )

    dataset_loader_version = sgqlc.types.Field(sgqlc.types.non_null(DatasetLoaderVersion), graphql_name="datasetLoaderVersion")

    executor_version = sgqlc.types.Field(sgqlc.types.non_null(ExecutorVersion), graphql_name="executorVersion")

    list_result_model_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ModelVersion"))), graphql_name="listResultModelVersion"
    )


class JobPagination(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("list_job", "total")
    list_job = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Job))), graphql_name="listJob")

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class JobParams(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "name",
        "experiment_name",
        "cron_expression",
        "periodic_type",
        "executor_params",
        "list_role_model_method_params",
        "data_params",
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    experiment_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="experimentName")

    cron_expression = sgqlc.types.Field(String, graphql_name="cronExpression")

    periodic_type = sgqlc.types.Field(sgqlc.types.non_null(PeriodicType), graphql_name="periodicType")

    executor_params = sgqlc.types.Field(sgqlc.types.non_null(ExecutorParams), graphql_name="executorParams")

    list_role_model_method_params = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RoleModelMethodParams"))), graphql_name="listRoleModelMethodParams"
    )

    data_params = sgqlc.types.Field(sgqlc.types.non_null(DataParams), graphql_name="dataParams")


class JobSchema(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("executor_method_schema", "list_role_model_method_schemas")
    executor_method_schema = sgqlc.types.Field(sgqlc.types.non_null("MethodSchema"), graphql_name="executorMethodSchema")

    list_role_model_method_schemas = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RoleMethodSchema"))), graphql_name="listRoleModelMethodSchemas"
    )


class MethodParams(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("method_name", "method_params")
    method_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="methodName")

    method_params = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="methodParams")


class MethodSchema(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("schema_name", "json_schema")
    schema_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="schemaName")

    json_schema = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="jsonSchema")


class Metric(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("key", "value", "step", "timestamp")
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="key")

    value = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name="value")

    step = sgqlc.types.Field(Int, graphql_name="step")

    timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="timestamp")


class Model(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "name",
        "description",
        "tags",
        "creation_timestamp",
        "last_updated_timestamp",
        "owner",
        "latest_model_version",
        "init_model_version",
        "list_model_version",
        "pagination_model_version",
        "best_model_version",
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="name")

    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="description")

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="tags")

    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="creationTimestamp")

    last_updated_timestamp = sgqlc.types.Field(LONG, graphql_name="lastUpdatedTimestamp")

    owner = sgqlc.types.Field(sgqlc.types.non_null("User"), graphql_name="owner")

    latest_model_version = sgqlc.types.Field(sgqlc.types.non_null("ModelVersion"), graphql_name="latestModelVersion")

    init_model_version = sgqlc.types.Field("ModelVersion", graphql_name="initModelVersion")

    list_model_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ModelVersion"))), graphql_name="listModelVersion"
    )

    pagination_model_version = sgqlc.types.Field(
        sgqlc.types.non_null("ModelVersionPagination"),
        graphql_name="paginationModelVersion",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    best_model_version = sgqlc.types.Field(
        sgqlc.types.non_null("ModelVersion"),
        graphql_name="bestModelVersion",
        args=sgqlc.types.ArgDict(
            (
                ("metric", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="metric", default=None)),
                ("optimal_min", sgqlc.types.Arg(Boolean, graphql_name="optimalMin", default=False)),
            )
        ),
    )
    """Arguments:

    * `metric` (`String!`)None
    * `optimal_min` (`Boolean`)None (default: `false`)
    """


class ModelPagination(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("list_model", "total")
    list_model = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Model))), graphql_name="listModel")

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class ModelVersion(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "name",
        "version",
        "source_path",
        "tags",
        "description",
        "status",
        "status_message",
        "creation_timestamp",
        "last_updated_timestamp",
        "upload_model_type",
        "model_method_schemas",
        "list_deployed_jobs",
        "pagination_deployed_jobs",
        "list_eval_run",
        "pagination_eval_run",
        "run",
        "group_job_run",
        "group_job_run_id",
        "source_run",
        "root_run",
        "model",
        "available_executor_versions",
        "pagination_available_executor_versions",
        "available_dataset_loaders",
        "available_collectors",
        "list_next_graph_nodes",
        "list_next_model_version",
        "list_new_model_from_version",
        "list_new_version_from_version",
        "pagination_next_model_version",
        "pagination_new_model_from_version",
        "pagination_new_version_from_version",
        "source_model_version",
        "source_executor_version",
        "root_model_version",
        "list_lineage_model_version",
        "pagination_lineage_model_version",
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="version")

    source_path = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="sourcePath")

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="tags")

    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="description")

    status = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="status")

    status_message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="statusMessage")

    creation_timestamp = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="creationTimestamp")

    last_updated_timestamp = sgqlc.types.Field(LONG, graphql_name="lastUpdatedTimestamp")

    upload_model_type = sgqlc.types.Field(sgqlc.types.non_null(UploadModelType), graphql_name="uploadModelType")

    model_method_schemas = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="modelMethodSchemas")

    list_deployed_jobs = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Job))), graphql_name="listDeployedJobs"
    )

    pagination_deployed_jobs = sgqlc.types.Field(
        sgqlc.types.non_null(JobPagination),
        graphql_name="paginationDeployedJobs",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    list_eval_run = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("Run"))), graphql_name="listEvalRun")

    pagination_eval_run = sgqlc.types.Field(
        sgqlc.types.non_null("RunPagination"),
        graphql_name="paginationEvalRun",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    run = sgqlc.types.Field(sgqlc.types.non_null("Run"), graphql_name="run")

    group_job_run = sgqlc.types.Field("Run", graphql_name="groupJobRun")

    group_job_run_id = sgqlc.types.Field(String, graphql_name="groupJobRunId")

    source_run = sgqlc.types.Field("Run", graphql_name="sourceRun")

    root_run = sgqlc.types.Field(sgqlc.types.non_null("Run"), graphql_name="rootRun")

    model = sgqlc.types.Field(sgqlc.types.non_null(Model), graphql_name="model")

    available_executor_versions = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ExecutorVersion))), graphql_name="availableExecutorVersions"
    )

    pagination_available_executor_versions = sgqlc.types.Field(
        sgqlc.types.non_null(ExecutorVersionPagination),
        graphql_name="paginationAvailableExecutorVersions",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    available_dataset_loaders = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DatasetLoader))), graphql_name="availableDatasetLoaders"
    )

    available_collectors = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name="availableCollectors"
    )

    list_next_graph_nodes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(GraphNode))), graphql_name="listNextGraphNodes"
    )

    list_next_model_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ModelVersion"))), graphql_name="listNextModelVersion"
    )

    list_new_model_from_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ModelVersion"))), graphql_name="listNewModelFromVersion"
    )

    list_new_version_from_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ModelVersion"))), graphql_name="listNewVersionFromVersion"
    )

    pagination_next_model_version = sgqlc.types.Field(
        sgqlc.types.non_null("ModelVersionPagination"),
        graphql_name="paginationNextModelVersion",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    pagination_new_model_from_version = sgqlc.types.Field(
        sgqlc.types.non_null("ModelVersionPagination"),
        graphql_name="paginationNewModelFromVersion",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    pagination_new_version_from_version = sgqlc.types.Field(
        sgqlc.types.non_null("ModelVersionPagination"),
        graphql_name="paginationNewVersionFromVersion",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    source_model_version = sgqlc.types.Field("ModelVersion", graphql_name="sourceModelVersion")

    source_executor_version = sgqlc.types.Field(ExecutorVersion, graphql_name="sourceExecutorVersion")

    root_model_version = sgqlc.types.Field(sgqlc.types.non_null("ModelVersion"), graphql_name="rootModelVersion")

    list_lineage_model_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("ModelVersion"))), graphql_name="listLineageModelVersion"
    )

    pagination_lineage_model_version = sgqlc.types.Field(
        sgqlc.types.non_null("ModelVersionPagination"),
        graphql_name="paginationLineageModelVersion",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """


class ModelVersionPagination(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("list_model_version", "total")
    list_model_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ModelVersion))), graphql_name="listModelVersion"
    )

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class Mutation(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "rename_experiment",
        "add_ml_job",
        "add_ml_job_single_model",
        "delete_model",
        "set_model_tag",
        "delete_model_tag",
        "set_model_description",
        "delete_model_version_from_name_version",
        "set_model_version_tag",
        "delete_model_version_tag",
        "set_model_version_description",
        "delete_dataset_loader",
        "set_dataset_loader_tag",
        "delete_dataset_loader_tag",
        "set_dataset_loader_description",
        "delete_dataset_loader_version_from_name_version",
        "set_dataset_loader_version_tag",
        "delete_dataset_loader_version_tag",
        "set_dataset_loader_version_description",
        "delete_executor",
        "set_executor_tag",
        "delete_executor_tag",
        "set_executor_description",
        "delete_executor_version_from_name_version",
        "set_executor_version_tag",
        "delete_executor_version_tag",
        "set_executor_version_description",
        "add_user",
        "update_user_password",
        "update_current_user_password",
        "update_current_user",
        "update_user",
        "update_user_attributes",
        "update_user_activity",
        "delete_user",
        "update_tree",
        "add_tree",
        "delete_tree",
        "delete_entity",
        "set_kvstore_item",
        "delete_kvstore_item",
        "add_user_group",
        "update_user_group",
        "update_user_group_attributes",
        "delete_user_group",
        "add_user_group_members",
        "delete_user_group_members",
    )
    rename_experiment = sgqlc.types.Field(
        sgqlc.types.non_null(Experiment),
        graphql_name="renameExperiment",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("new_name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="newName", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `new_name` (`String!`)None
    """

    add_ml_job = sgqlc.types.Field(
        sgqlc.types.non_null(Job),
        graphql_name="addMlJob",
        args=sgqlc.types.ArgDict((("form", sgqlc.types.Arg(sgqlc.types.non_null(JobParameters), graphql_name="form", default=None)),)),
    )
    """Arguments:

    * `form` (`JobParameters!`)None
    """

    add_ml_job_single_model = sgqlc.types.Field(
        sgqlc.types.non_null(Job),
        graphql_name="addMlJobSingleModel",
        args=sgqlc.types.ArgDict(
            (("form", sgqlc.types.Arg(sgqlc.types.non_null(JobSingleParameters), graphql_name="form", default=None)),)
        ),
    )
    """Arguments:

    * `form` (`JobSingleParameters!`)None
    """

    delete_model = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="deleteModel",
        args=sgqlc.types.ArgDict((("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)),
    )
    """Arguments:

    * `name` (`String!`)None
    """

    set_model_tag = sgqlc.types.Field(
        sgqlc.types.non_null(Model),
        graphql_name="setModelTag",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
                ("value", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="value", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `key` (`String!`)None
    * `value` (`String!`)None
    """

    delete_model_tag = sgqlc.types.Field(
        sgqlc.types.non_null(Model),
        graphql_name="deleteModelTag",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `key` (`String!`)None
    """

    set_model_description = sgqlc.types.Field(
        sgqlc.types.non_null(Model),
        graphql_name="setModelDescription",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("description", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="description", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `description` (`String!`)None
    """

    delete_model_version_from_name_version = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="deleteModelVersionFromNameVersion",
        args=sgqlc.types.ArgDict(
            (("model_version", sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="modelVersion", default=None)),)
        ),
    )
    """Arguments:

    * `model_version` (`ObjectVersionInput!`)None
    """

    set_model_version_tag = sgqlc.types.Field(
        sgqlc.types.non_null(ModelVersion),
        graphql_name="setModelVersionTag",
        args=sgqlc.types.ArgDict(
            (
                ("model_version", sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="modelVersion", default=None)),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
                ("value", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="value", default=None)),
            )
        ),
    )
    """Arguments:

    * `model_version` (`ObjectVersionInput!`)None
    * `key` (`String!`)None
    * `value` (`String!`)None
    """

    delete_model_version_tag = sgqlc.types.Field(
        sgqlc.types.non_null(ModelVersion),
        graphql_name="deleteModelVersionTag",
        args=sgqlc.types.ArgDict(
            (
                ("model_version", sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="modelVersion", default=None)),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
            )
        ),
    )
    """Arguments:

    * `model_version` (`ObjectVersionInput!`)None
    * `key` (`String!`)None
    """

    set_model_version_description = sgqlc.types.Field(
        sgqlc.types.non_null(ModelVersion),
        graphql_name="setModelVersionDescription",
        args=sgqlc.types.ArgDict(
            (
                ("model_version", sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="modelVersion", default=None)),
                ("description", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="description", default=None)),
            )
        ),
    )
    """Arguments:

    * `model_version` (`ObjectVersionInput!`)None
    * `description` (`String!`)None
    """

    delete_dataset_loader = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="deleteDatasetLoader",
        args=sgqlc.types.ArgDict((("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)),
    )
    """Arguments:

    * `name` (`String!`)None
    """

    set_dataset_loader_tag = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoader),
        graphql_name="setDatasetLoaderTag",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
                ("value", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="value", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `key` (`String!`)None
    * `value` (`String!`)None
    """

    delete_dataset_loader_tag = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoader),
        graphql_name="deleteDatasetLoaderTag",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `key` (`String!`)None
    """

    set_dataset_loader_description = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoader),
        graphql_name="setDatasetLoaderDescription",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("description", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="description", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `description` (`String!`)None
    """

    delete_dataset_loader_version_from_name_version = sgqlc.types.Field(
        Boolean,
        graphql_name="deleteDatasetLoaderVersionFromNameVersion",
        args=sgqlc.types.ArgDict(
            (
                (
                    "dataset_loader_version",
                    sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="datasetLoaderVersion", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `dataset_loader_version` (`ObjectVersionInput!`)None
    """

    set_dataset_loader_version_tag = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoaderVersion),
        graphql_name="setDatasetLoaderVersionTag",
        args=sgqlc.types.ArgDict(
            (
                (
                    "dataset_loader_version",
                    sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="datasetLoaderVersion", default=None),
                ),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
                ("value", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="value", default=None)),
            )
        ),
    )
    """Arguments:

    * `dataset_loader_version` (`ObjectVersionInput!`)None
    * `key` (`String!`)None
    * `value` (`String!`)None
    """

    delete_dataset_loader_version_tag = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoaderVersion),
        graphql_name="deleteDatasetLoaderVersionTag",
        args=sgqlc.types.ArgDict(
            (
                (
                    "dataset_loader_version",
                    sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="datasetLoaderVersion", default=None),
                ),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
            )
        ),
    )
    """Arguments:

    * `dataset_loader_version` (`ObjectVersionInput!`)None
    * `key` (`String!`)None
    """

    set_dataset_loader_version_description = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoaderVersion),
        graphql_name="setDatasetLoaderVersionDescription",
        args=sgqlc.types.ArgDict(
            (
                (
                    "dataset_loader_version",
                    sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="datasetLoaderVersion", default=None),
                ),
                ("description", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="description", default=None)),
            )
        ),
    )
    """Arguments:

    * `dataset_loader_version` (`ObjectVersionInput!`)None
    * `description` (`String!`)None
    """

    delete_executor = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="deleteExecutor",
        args=sgqlc.types.ArgDict((("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)),
    )
    """Arguments:

    * `name` (`String!`)None
    """

    set_executor_tag = sgqlc.types.Field(
        sgqlc.types.non_null(Executor),
        graphql_name="setExecutorTag",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
                ("value", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="value", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `key` (`String!`)None
    * `value` (`String!`)None
    """

    delete_executor_tag = sgqlc.types.Field(
        sgqlc.types.non_null(Executor),
        graphql_name="deleteExecutorTag",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `key` (`String!`)None
    """

    set_executor_description = sgqlc.types.Field(
        sgqlc.types.non_null(Executor),
        graphql_name="setExecutorDescription",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                ("description", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="description", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `description` (`String!`)None
    """

    delete_executor_version_from_name_version = sgqlc.types.Field(
        Boolean,
        graphql_name="deleteExecutorVersionFromNameVersion",
        args=sgqlc.types.ArgDict(
            (("executor_version", sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="executorVersion", default=None)),)
        ),
    )
    """Arguments:

    * `executor_version` (`ObjectVersionInput!`)None
    """

    set_executor_version_tag = sgqlc.types.Field(
        sgqlc.types.non_null(ExecutorVersion),
        graphql_name="setExecutorVersionTag",
        args=sgqlc.types.ArgDict(
            (
                (
                    "executor_version",
                    sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="executorVersion", default=None),
                ),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
                ("value", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="value", default=None)),
            )
        ),
    )
    """Arguments:

    * `executor_version` (`ObjectVersionInput!`)None
    * `key` (`String!`)None
    * `value` (`String!`)None
    """

    delete_executor_version_tag = sgqlc.types.Field(
        sgqlc.types.non_null(ExecutorVersion),
        graphql_name="deleteExecutorVersionTag",
        args=sgqlc.types.ArgDict(
            (
                (
                    "executor_version",
                    sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="executorVersion", default=None),
                ),
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
            )
        ),
    )
    """Arguments:

    * `executor_version` (`ObjectVersionInput!`)None
    * `key` (`String!`)None
    """

    set_executor_version_description = sgqlc.types.Field(
        sgqlc.types.non_null(ExecutorVersion),
        graphql_name="setExecutorVersionDescription",
        args=sgqlc.types.ArgDict(
            (
                (
                    "executor_version",
                    sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="executorVersion", default=None),
                ),
                ("description", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="description", default=None)),
            )
        ),
    )
    """Arguments:

    * `executor_version` (`ObjectVersionInput!`)None
    * `description` (`String!`)None
    """

    add_user = sgqlc.types.Field(
        "User",
        graphql_name="addUser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "create_user_params",
                    sgqlc.types.Arg(sgqlc.types.non_null(CreateUserParams), graphql_name="createUserParams", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `create_user_params` (`CreateUserParams!`)None
    """

    update_user_password = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="updateUserPassword",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name="id", default=None)),
                ("password", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="password", default=None)),
            )
        ),
    )
    """Arguments:

    * `id` (`ID!`)None
    * `password` (`String!`)None
    """

    update_current_user_password = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="updateCurrentUserPassword",
        args=sgqlc.types.ArgDict(
            (
                ("old_password", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="oldPassword", default=None)),
                ("password", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="password", default=None)),
            )
        ),
    )
    """Arguments:

    * `old_password` (`String!`)None
    * `password` (`String!`)None
    """

    update_current_user = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="updateCurrentUser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "update_current_user_params",
                    sgqlc.types.Arg(sgqlc.types.non_null(UpdateCurrentUserParams), graphql_name="updateCurrentUserParams", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `update_current_user_params` (`UpdateCurrentUserParams!`)None
    """

    update_user = sgqlc.types.Field(
        "User",
        graphql_name="updateUser",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name="id", default=None)),
                (
                    "update_user_params",
                    sgqlc.types.Arg(sgqlc.types.non_null(UpdateUserParams), graphql_name="updateUserParams", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID!`)None
    * `update_user_params` (`UpdateUserParams!`)None
    """

    update_user_attributes = sgqlc.types.Field(
        sgqlc.types.non_null("UserWithError"),
        graphql_name="updateUserAttributes",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name="id", default=None)),
                (
                    "attributes",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(UserAttributeInput))),
                        graphql_name="attributes",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID!`)None
    * `attributes` (`[UserAttributeInput!]!`)None
    """

    update_user_activity = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="updateUserActivity",
        args=sgqlc.types.ArgDict(
            (
                (
                    "ids",
                    sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name="ids", default=None),
                ),
                ("is_enabled", sgqlc.types.Arg(sgqlc.types.non_null(Boolean), graphql_name="isEnabled", default=None)),
            )
        ),
    )
    """Arguments:

    * `ids` (`[ID!]!`)None
    * `is_enabled` (`Boolean!`)None
    """

    delete_user = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="deleteUser",
        args=sgqlc.types.ArgDict((("id", sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name="id", default=None)),)),
    )
    """Arguments:

    * `id` (`ID!`)None
    """

    update_tree = sgqlc.types.Field(
        sgqlc.types.non_null("SecurityTreeGQL"),
        graphql_name="updateTree",
        args=sgqlc.types.ArgDict(
            (
                (
                    "policies",
                    sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(SecurityPolicyArg)), graphql_name="policies", default=None),
                ),
                ("rules", sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(SecurityRuleArg)), graphql_name="rules", default=None)),
                ("security_tree_id", sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name="securityTreeID", default=None)),
                ("parent_policy_id", sgqlc.types.Arg(ID, graphql_name="parentPolicyID", default=None)),
            )
        ),
    )
    """Arguments:

    * `policies` (`[SecurityPolicyArg!]`)None
    * `rules` (`[SecurityRuleArg!]`)None
    * `security_tree_id` (`ID!`)None
    * `parent_policy_id` (`ID`)None
    """

    add_tree = sgqlc.types.Field(
        sgqlc.types.non_null("SecurityTreeGQL"),
        graphql_name="addTree",
        args=sgqlc.types.ArgDict(
            (
                ("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),
                (
                    "policies",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(SecurityPolicyArg))),
                        graphql_name="policies",
                        default=None,
                    ),
                ),
                ("rules", sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(SecurityRuleArg)), graphql_name="rules", default=None)),
            )
        ),
    )
    """Arguments:

    * `name` (`String!`)None
    * `policies` (`[SecurityPolicyArg!]!`)None
    * `rules` (`[SecurityRuleArg!]`)None
    """

    delete_tree = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="deleteTree",
        args=sgqlc.types.ArgDict(
            (("security_tree_id", sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name="securityTreeID", default=None)),)
        ),
    )
    """Arguments:

    * `security_tree_id` (`ID!`)None
    """

    delete_entity = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="deleteEntity",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name="id", default=None)),
                ("security_tree_id", sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name="securityTreeID", default=None)),
                ("parent_policy_id", sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name="parentPolicyID", default=None)),
            )
        ),
    )
    """Arguments:

    * `id` (`ID!`)None
    * `security_tree_id` (`ID!`)None
    * `parent_policy_id` (`ID!`)None
    """

    set_kvstore_item = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="setKVStoreItem",
        args=sgqlc.types.ArgDict(
            (
                ("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),
                ("value", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="value", default=None)),
            )
        ),
    )
    """Arguments:

    * `key` (`String!`)None
    * `value` (`String!`)None
    """

    delete_kvstore_item = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="deleteKVStoreItem",
        args=sgqlc.types.ArgDict((("key", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="key", default=None)),)),
    )
    """Arguments:

    * `key` (`String!`)None
    """

    add_user_group = sgqlc.types.Field(
        "UserGroup",
        graphql_name="addUserGroup",
        args=sgqlc.types.ArgDict(
            (
                (
                    "create_user_group_params",
                    sgqlc.types.Arg(sgqlc.types.non_null(CreateUserGroupParams), graphql_name="createUserGroupParams", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `create_user_group_params` (`CreateUserGroupParams!`)None
    """

    update_user_group = sgqlc.types.Field(
        sgqlc.types.non_null("UserGroup"),
        graphql_name="updateUserGroup",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name="id", default=None)),
                (
                    "update_user_group_params",
                    sgqlc.types.Arg(sgqlc.types.non_null(UpdateUserGroupParams), graphql_name="updateUserGroupParams", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID!`)None
    * `update_user_group_params` (`UpdateUserGroupParams!`)None
    """

    update_user_group_attributes = sgqlc.types.Field(
        sgqlc.types.non_null("UserGroupWithError"),
        graphql_name="updateUserGroupAttributes",
        args=sgqlc.types.ArgDict(
            (
                ("id", sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name="id", default=None)),
                (
                    "attributes",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(UserAttributeInput))),
                        graphql_name="attributes",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `id` (`ID!`)None
    * `attributes` (`[UserAttributeInput!]!`)None
    """

    delete_user_group = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="deleteUserGroup",
        args=sgqlc.types.ArgDict((("id", sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name="id", default=None)),)),
    )
    """Arguments:

    * `id` (`ID!`)None
    """

    add_user_group_members = sgqlc.types.Field(
        sgqlc.types.non_null("StateWithError"),
        graphql_name="addUserGroupMembers",
        args=sgqlc.types.ArgDict(
            (
                (
                    "add_user_group_members_params",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AddUserGroupMembersParams), graphql_name="addUserGroupMembersParams", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `add_user_group_members_params`
      (`AddUserGroupMembersParams!`)None
    """

    delete_user_group_members = sgqlc.types.Field(
        sgqlc.types.non_null(Boolean),
        graphql_name="deleteUserGroupMembers",
        args=sgqlc.types.ArgDict(
            (
                (
                    "delete_user_group_member_params",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(DeleteUserGroupMemberParams), graphql_name="deleteUserGroupMemberParams", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `delete_user_group_member_params`
      (`DeleteUserGroupMemberParams!`)None
    """


class NodeResultGQL(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("id", "child_id_list", "combining_algorithm")
    id = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name="id")

    child_id_list = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Long))), graphql_name="childIdList")

    combining_algorithm = sgqlc.types.Field(sgqlc.types.non_null(CombiningAlgorithm), graphql_name="combiningAlgorithm")


class ParamsSchema(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("schema", "ui_schema")
    schema = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="schema")

    ui_schema = sgqlc.types.Field(JSON, graphql_name="uiSchema")


class PolicyParameterGQL(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("param", "parameter_type")
    param = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="param")

    parameter_type = sgqlc.types.Field(sgqlc.types.non_null(AttributeType), graphql_name="parameterType")


class Query(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "graph_node",
        "list_graph_node",
        "list_subtree_graph_node",
        "run_from_run_id",
        "search_runs",
        "list_experiment",
        "pagination_experiment",
        "experiment_from_name",
        "experiment_from_id",
        "job_from_name",
        "list_job",
        "pagination_job",
        "search_job",
        "model_from_name",
        "warning_delete_model_query",
        "list_model",
        "pagination_model",
        "model_version_from_run_id",
        "model_version_from_name_version",
        "list_initial_model_version",
        "pagination_initial_model_version",
        "list_dataset_loader",
        "pagination_dataset_loader",
        "dataset_loader_from_name",
        "dataset_loader_version_from_name_version",
        "dataset_loader_version_from_run_id",
        "executor_from_name",
        "list_executor",
        "pagination_executor",
        "executor_version_from_name_version",
        "executor_version_from_run_id",
        "list_initial_executor_version",
        "current_user",
        "user_by_login",
        "pagination_attribute",
    )
    graph_node = sgqlc.types.Field(
        sgqlc.types.non_null(GraphNode),
        graphql_name="graphNode",
        args=sgqlc.types.ArgDict((("run_id", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="runId", default=None)),)),
    )
    """Arguments:

    * `run_id` (`String!`)None
    """

    list_graph_node = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(GraphNode))), graphql_name="listGraphNode"
    )

    list_subtree_graph_node = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(GraphNode))),
        graphql_name="listSubtreeGraphNode",
        args=sgqlc.types.ArgDict((("root_run_id", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="rootRunId", default=None)),)),
    )
    """Arguments:

    * `root_run_id` (`String!`)None
    """

    run_from_run_id = sgqlc.types.Field(
        sgqlc.types.non_null("Run"),
        graphql_name="runFromRunId",
        args=sgqlc.types.ArgDict((("run_id", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="runId", default=None)),)),
    )
    """Arguments:

    * `run_id` (`String!`)None
    """

    search_runs = sgqlc.types.Field(
        sgqlc.types.non_null("RunPagination"),
        graphql_name="searchRuns",
        args=sgqlc.types.ArgDict(
            (
                (
                    "experiment_ids",
                    sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="experimentIds", default=None),
                ),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
                ("filter_string", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="filterString", default="")),
                ("run_view_type", sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name="runViewType", default=1)),
                ("order_by", sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="orderBy", default=None)),
                (
                    "experiment_names",
                    sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name="experimentNames", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `experiment_ids` (`[String!]`)None (default: `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    * `filter_string` (`String!`)None (default: `""`)
    * `run_view_type` (`Int!`)None (default: `1`)
    * `order_by` (`[String!]`)None (default: `null`)
    * `experiment_names` (`[String!]`)None (default: `null`)
    """

    list_experiment = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Experiment))), graphql_name="listExperiment"
    )

    pagination_experiment = sgqlc.types.Field(
        sgqlc.types.non_null(ExperimentPagination),
        graphql_name="paginationExperiment",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    experiment_from_name = sgqlc.types.Field(
        sgqlc.types.non_null(Experiment),
        graphql_name="experimentFromName",
        args=sgqlc.types.ArgDict((("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)),
    )
    """Arguments:

    * `name` (`String!`)None
    """

    experiment_from_id = sgqlc.types.Field(
        sgqlc.types.non_null(Experiment),
        graphql_name="experimentFromId",
        args=sgqlc.types.ArgDict(
            (("experiment_id", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="experimentId", default=None)),)
        ),
    )
    """Arguments:

    * `experiment_id` (`String!`)None
    """

    job_from_name = sgqlc.types.Field(
        sgqlc.types.non_null(Job),
        graphql_name="jobFromName",
        args=sgqlc.types.ArgDict((("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)),
    )
    """Arguments:

    * `name` (`String!`)None
    """

    list_job = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Job))), graphql_name="listJob")

    pagination_job = sgqlc.types.Field(
        sgqlc.types.non_null(JobPagination),
        graphql_name="paginationJob",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    search_job = sgqlc.types.Field(
        sgqlc.types.non_null(JobPagination),
        graphql_name="searchJob",
        args=sgqlc.types.ArgDict(
            (
                ("periodic_type", sgqlc.types.Arg(PeriodicType, graphql_name="periodicType", default=None)),
                ("status", sgqlc.types.Arg(JobStatus, graphql_name="status", default=None)),
                ("init_model_version", sgqlc.types.Arg(ObjectVersionInput, graphql_name="initModelVersion", default=None)),
                ("dataset_loader_version", sgqlc.types.Arg(ObjectVersionInput, graphql_name="datasetLoaderVersion", default=None)),
                ("executor_version", sgqlc.types.Arg(ObjectVersionInput, graphql_name="executorVersion", default=None)),
                ("start_interval", sgqlc.types.Arg(TimestampInterval, graphql_name="startInterval", default=None)),
                ("end_interval", sgqlc.types.Arg(TimestampInterval, graphql_name="endInterval", default=None)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `periodic_type` (`PeriodicType`)None (default: `null`)
    * `status` (`JobStatus`)None (default: `null`)
    * `init_model_version` (`ObjectVersionInput`)None (default:
      `null`)
    * `dataset_loader_version` (`ObjectVersionInput`)None (default:
      `null`)
    * `executor_version` (`ObjectVersionInput`)None (default: `null`)
    * `start_interval` (`TimestampInterval`)None (default: `null`)
    * `end_interval` (`TimestampInterval`)None (default: `null`)
    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    model_from_name = sgqlc.types.Field(
        sgqlc.types.non_null(Model),
        graphql_name="modelFromName",
        args=sgqlc.types.ArgDict((("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)),
    )
    """Arguments:

    * `name` (`String!`)None
    """

    warning_delete_model_query = sgqlc.types.Field(
        sgqlc.types.non_null("WarningDeleteModel"),
        graphql_name="warningDeleteModelQuery",
        args=sgqlc.types.ArgDict((("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)),
    )
    """Arguments:

    * `name` (`String!`)None
    """

    list_model = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Model))), graphql_name="listModel")

    pagination_model = sgqlc.types.Field(
        sgqlc.types.non_null(ModelPagination),
        graphql_name="paginationModel",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    model_version_from_run_id = sgqlc.types.Field(
        sgqlc.types.non_null(ModelVersion),
        graphql_name="modelVersionFromRunId",
        args=sgqlc.types.ArgDict((("run_id", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="runId", default=None)),)),
    )
    """Arguments:

    * `run_id` (`String!`)None
    """

    model_version_from_name_version = sgqlc.types.Field(
        sgqlc.types.non_null(ModelVersion),
        graphql_name="modelVersionFromNameVersion",
        args=sgqlc.types.ArgDict(
            (("model_version", sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="modelVersion", default=None)),)
        ),
    )
    """Arguments:

    * `model_version` (`ObjectVersionInput!`)None
    """

    list_initial_model_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ModelVersion))), graphql_name="listInitialModelVersion"
    )

    pagination_initial_model_version = sgqlc.types.Field(
        sgqlc.types.non_null(ModelVersionPagination),
        graphql_name="paginationInitialModelVersion",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    list_dataset_loader = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DatasetLoader))), graphql_name="listDatasetLoader"
    )

    pagination_dataset_loader = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoaderPagination),
        graphql_name="paginationDatasetLoader",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    dataset_loader_from_name = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoader),
        graphql_name="datasetLoaderFromName",
        args=sgqlc.types.ArgDict((("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)),
    )
    """Arguments:

    * `name` (`String!`)None
    """

    dataset_loader_version_from_name_version = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoaderVersion),
        graphql_name="datasetLoaderVersionFromNameVersion",
        args=sgqlc.types.ArgDict(
            (
                (
                    "dataset_loader_version",
                    sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="datasetLoaderVersion", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `dataset_loader_version` (`ObjectVersionInput!`)None
    """

    dataset_loader_version_from_run_id = sgqlc.types.Field(
        sgqlc.types.non_null(DatasetLoaderVersion),
        graphql_name="datasetLoaderVersionFromRunId",
        args=sgqlc.types.ArgDict((("run_id", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="runId", default=None)),)),
    )
    """Arguments:

    * `run_id` (`String!`)None
    """

    executor_from_name = sgqlc.types.Field(
        sgqlc.types.non_null(Executor),
        graphql_name="executorFromName",
        args=sgqlc.types.ArgDict((("name", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="name", default=None)),)),
    )
    """Arguments:

    * `name` (`String!`)None
    """

    list_executor = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Executor))), graphql_name="listExecutor"
    )

    pagination_executor = sgqlc.types.Field(
        sgqlc.types.non_null(ExecutorPagination),
        graphql_name="paginationExecutor",
        args=sgqlc.types.ArgDict(
            (
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=None)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=None)),
            )
        ),
    )
    """Arguments:

    * `limit` (`Int`)None (default: `null`)
    * `offset` (`Int`)None (default: `null`)
    """

    executor_version_from_name_version = sgqlc.types.Field(
        sgqlc.types.non_null(ExecutorVersion),
        graphql_name="executorVersionFromNameVersion",
        args=sgqlc.types.ArgDict(
            (("executor_version", sgqlc.types.Arg(sgqlc.types.non_null(ObjectVersionInput), graphql_name="executorVersion", default=None)),)
        ),
    )
    """Arguments:

    * `executor_version` (`ObjectVersionInput!`)None
    """

    executor_version_from_run_id = sgqlc.types.Field(
        sgqlc.types.non_null(ExecutorVersion),
        graphql_name="executorVersionFromRunId",
        args=sgqlc.types.ArgDict((("run_id", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="runId", default=None)),)),
    )
    """Arguments:

    * `run_id` (`String!`)None
    """

    list_initial_executor_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ExecutorVersion))), graphql_name="listInitialExecutorVersion"
    )

    current_user = sgqlc.types.Field(sgqlc.types.non_null("User"), graphql_name="currentUser")

    user_by_login = sgqlc.types.Field(
        sgqlc.types.non_null("User"),
        graphql_name="userByLogin",
        args=sgqlc.types.ArgDict(
            (
                ("username", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="username", default=None)),
                ("password", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="password", default=None)),
            )
        ),
    )
    """Arguments:

    * `username` (`String!`)None
    * `password` (`String!`)None
    """

    pagination_attribute = sgqlc.types.Field(
        sgqlc.types.non_null(AttributePagination),
        graphql_name="paginationAttribute",
        args=sgqlc.types.ArgDict(
            (
                (
                    "attribute_filter_settings",
                    sgqlc.types.Arg(sgqlc.types.non_null(AttributeFilterSettings), graphql_name="attributeFilterSettings", default=None),
                ),
                ("query", sgqlc.types.Arg(String, graphql_name="query", default=None)),
                ("limit", sgqlc.types.Arg(Int, graphql_name="limit", default=20)),
                ("offset", sgqlc.types.Arg(Int, graphql_name="offset", default=0)),
            )
        ),
    )
    """Arguments:

    * `attribute_filter_settings` (`AttributeFilterSettings!`)None
    * `query` (`String`)None
    * `limit` (`Int`)None (default: `20`)
    * `offset` (`Int`)None (default: `0`)
    """


class RoleMethodSchema(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("role", "list_model_method_schemas")
    role = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="role")

    list_model_method_schemas = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MethodSchema))), graphql_name="listModelMethodSchemas"
    )


class RoleModelMethodParams(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("role", "name", "version", "params", "choice_criteria", "metric_name", "optimal_min", "new_model_name")
    role = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="role")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    version = sgqlc.types.Field(Int, graphql_name="version")

    params = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MethodParams))), graphql_name="params")

    choice_criteria = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="choiceCriteria")

    metric_name = sgqlc.types.Field(String, graphql_name="metricName")

    optimal_min = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="optimalMin")

    new_model_name = sgqlc.types.Field(String, graphql_name="newModelName")


class RoleModelVersion(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("role", "model_version")
    role = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="role")

    model_version = sgqlc.types.Field(sgqlc.types.non_null(ModelVersion), graphql_name="modelVersion")


class Run(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = (
        "run_id",
        "artifact_uri",
        "status",
        "latest_metrics",
        "experiment_id",
        "params",
        "start_time",
        "end_time",
        "lifecycle_stage",
        "parent_job",
        "list_artifacts",
        "experiment",
        "tags",
        "metric_history",
    )
    run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="runId")

    artifact_uri = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="artifactUri")

    status = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="status")

    latest_metrics = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="latestMetrics")

    experiment_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="experimentId")

    params = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="params")

    start_time = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="startTime")

    end_time = sgqlc.types.Field(sgqlc.types.non_null(LONG), graphql_name="endTime")

    lifecycle_stage = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="lifecycleStage")

    parent_job = sgqlc.types.Field(Job, graphql_name="parentJob")

    list_artifacts = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name="listArtifacts"
    )

    experiment = sgqlc.types.Field(sgqlc.types.non_null(Experiment), graphql_name="experiment")

    tags = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="tags")

    metric_history = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Metric))),
        graphql_name="metricHistory",
        args=sgqlc.types.ArgDict((("metric", sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name="metric", default=None)),)),
    )
    """Arguments:

    * `metric` (`String!`)None
    """


class RunPagination(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("list_run", "total")
    list_run = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Run))), graphql_name="listRun")

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class SecurityPolicyGQL(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("id", "name", "target", "params", "security_entity_idlist", "combining_algorithm")
    id = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    target = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="target")

    params = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(PolicyParameterGQL))), graphql_name="params")

    security_entity_idlist = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Long))), graphql_name="securityEntityIDList"
    )

    combining_algorithm = sgqlc.types.Field(sgqlc.types.non_null(CombiningAlgorithm), graphql_name="combiningAlgorithm")


class SecurityRuleGQL(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("id", "name", "target", "rule_type", "rule", "params", "source")
    id = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    target = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="target")

    rule_type = sgqlc.types.Field(sgqlc.types.non_null(RuleType), graphql_name="ruleType")

    rule = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="rule")

    params = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(PolicyParameterGQL))), graphql_name="params")

    source = sgqlc.types.Field(String, graphql_name="source")


class SecurityTreeGQL(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("id", "name", "entity_list")
    id = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    entity_list = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("SecurityEntity"))), graphql_name="entityList"
    )


class StateWithError(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("state", "info")
    state = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="state")

    info = sgqlc.types.Field(sgqlc.types.non_null(ConflictsState), graphql_name="info")


class StringListValue(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("value",)
    value = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name="value")


class StringValue(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("value",)
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="value")


class UserAttribute(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("id", "name", "value", "json_value")
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    value = sgqlc.types.Field(sgqlc.types.non_null("AttributeValue"), graphql_name="value")

    json_value = sgqlc.types.Field(sgqlc.types.non_null(JSON), graphql_name="jsonValue")


class UserGroupMetrics(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("count_user",)
    count_user = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="countUser")


class UserGroupPagination(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("list_user_group", "total")
    list_user_group = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("UserGroup"))), graphql_name="listUserGroup"
    )

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class UserGroupWithError(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("user_group", "info")
    user_group = sgqlc.types.Field(sgqlc.types.non_null("UserGroup"), graphql_name="userGroup")

    info = sgqlc.types.Field(sgqlc.types.non_null(ConflictsState), graphql_name="info")


class UserMetrics(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("count_group",)
    count_group = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="countGroup")


class UserPagination(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("list_user", "total")
    list_user = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("User"))), graphql_name="listUser")

    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name="total")


class UserWithError(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("user", "info")
    user = sgqlc.types.Field(sgqlc.types.non_null("User"), graphql_name="user")

    info = sgqlc.types.Field(sgqlc.types.non_null(ConflictsState), graphql_name="info")


class WarningDeleteModel(sgqlc.types.Type):
    __schema__ = my_schema
    __field_names__ = ("delete_possible", "list_model_version")
    delete_possible = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="deletePossible")

    list_model_version = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ModelVersion))), graphql_name="listModelVersion"
    )


class User(sgqlc.types.Type, RecordInterface):
    __schema__ = my_schema
    __field_names__ = (
        "id",
        "login",
        "first_name",
        "last_name",
        "fathers_name",
        "email",
        "is_admin",
        "enabled",
        "receive_notifications",
        "receive_telegram_notifications",
        "telegram_chat_id",
        "access_level",
        "name",
        "list_user_group",
        "metrics",
        "attributes",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    login = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="login")

    first_name = sgqlc.types.Field(String, graphql_name="firstName")

    last_name = sgqlc.types.Field(String, graphql_name="lastName")

    fathers_name = sgqlc.types.Field(String, graphql_name="fathersName")

    email = sgqlc.types.Field(String, graphql_name="email")

    is_admin = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="isAdmin")

    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="enabled")

    receive_notifications = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="receiveNotifications")

    receive_telegram_notifications = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name="receiveTelegramNotifications")

    telegram_chat_id = sgqlc.types.Field(Long, graphql_name="telegramChatId")

    access_level = sgqlc.types.Field(sgqlc.types.non_null(AccessLevel), graphql_name="accessLevel")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    list_user_group = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("UserGroup"))), graphql_name="listUserGroup"
    )

    metrics = sgqlc.types.Field(sgqlc.types.non_null(UserMetrics), graphql_name="metrics")

    attributes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(UserAttribute))),
        graphql_name="attributes",
        args=sgqlc.types.ArgDict(
            (
                ("show_default", sgqlc.types.Arg(Boolean, graphql_name="showDefault", default=False)),
                ("is_request_from_front", sgqlc.types.Arg(Boolean, graphql_name="isRequestFromFront", default=True)),
            )
        ),
    )
    """Arguments:

    * `show_default` (`Boolean`)None (default: `false`)
    * `is_request_from_front` (`Boolean`)None (default: `true`)
    """


class UserGroup(sgqlc.types.Type, RecordInterface):
    __schema__ = my_schema
    __field_names__ = ("id", "name", "description", "attributes", "list_user", "metrics")
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name="id")

    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="name")

    description = sgqlc.types.Field(String, graphql_name="description")

    attributes = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(UserAttribute))), graphql_name="attributes"
    )

    list_user = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(User))), graphql_name="listUser")

    metrics = sgqlc.types.Field(sgqlc.types.non_null(UserGroupMetrics), graphql_name="metrics")


########################################################################
# Unions
########################################################################
class AttributeValue(sgqlc.types.Union):
    __schema__ = my_schema
    __types__ = (IntValue, DoubleValue, StringValue, BooleanValue, IntListValue, DoubleListValue, StringListValue, BooleanListValue)


class EvaluationNodeGQL(sgqlc.types.Union):
    __schema__ = my_schema
    __types__ = (BooleanResultGQL, FilterResultGQL, NodeResultGQL)


class SecurityEntity(sgqlc.types.Union):
    __schema__ = my_schema
    __types__ = (SecurityPolicyGQL, SecurityRuleGQL)


########################################################################
# Schema Entry Points
########################################################################
my_schema.query_type = Query
my_schema.mutation_type = Mutation
my_schema.subscription_type = None
