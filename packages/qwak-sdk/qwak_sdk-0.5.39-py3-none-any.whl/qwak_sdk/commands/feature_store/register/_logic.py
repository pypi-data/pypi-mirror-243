from typing import List, Optional, Tuple, cast

from _qwak_proto.qwak.feature_store.entities.entity_pb2 import (
    EntityDefinition as ProtoEntityDefinition,
)
from _qwak_proto.qwak.feature_store.features.feature_set_pb2 import (
    Feature as ProtoFeature,
)
from _qwak_proto.qwak.feature_store.features.feature_set_service_pb2 import (
    GetFeatureSetByNameResponse as ProtoGetFeatureSetByNameResponse,
)
from _qwak_proto.qwak.features_operator.v3.features_operator_pb2 import (
    SparkColumnDescription,
    ValidationSuccessResponse,
)
from qwak.clients.feature_store import FeatureRegistryClient
from qwak.clients.feature_store.operator_client import FeaturesOperatorClient
from qwak.exceptions import QwakException
from qwak.feature_store.data_sources.base import BaseSource
from qwak.feature_store.entities.entity import Entity
from qwak.feature_store.feature_sets.base_feature_set import BaseFeatureSet
from qwak.feature_store.validations.validation_response import (
    SuccessValidationResponse,
    ValidationResponse,
)
from tabulate import tabulate

from qwak_sdk.inner.file_registry import extract_class_objects
from qwak_sdk.inner.tools.cli_tools import ask_yesno
from qwak_sdk.tools.utils import qwak_spinner

DELIMITER = "----------------------------------------"


def _register_entities(
    qwak_python_files: List[Tuple[str, str]],
    registry: FeatureRegistryClient,
    force: bool,
):
    """
    Register Feature Store Entity Objects

    Args:
        qwak_python_files: a list of python files containing qwak package imports
        registry: FeatureRegistryClient
        force: boolean determining if to force register all encountered Entity objects
    """
    with qwak_spinner(begin_text="Finding Entities to register", print_callback=print):
        qwak_entities: List[Tuple[Entity, str]] = extract_class_objects(
            qwak_python_files, Entity
        )

    print(f"👀 Found {len(qwak_entities)} Entities")
    for entity, source_file_path in qwak_entities:
        existing_entity = registry.get_entity_by_name(entity.name)
        if existing_entity:
            if ask_yesno(
                f"Update existing Entity '{entity.name}' from source file '{source_file_path}'?",
                force,
            ):
                registry.update_entity(
                    existing_entity.entity.entity_definition.entity_id,
                    entity._to_proto(),
                )
        else:
            if ask_yesno(
                f"Create new Entity '{entity.name}' from source file '{source_file_path}'?",
                force,
            ):
                registry.create_entity(entity._to_proto())
    print(DELIMITER)


def _register_data_sources(
    qwak_python_files: List[Tuple[str, str]],
    registry: FeatureRegistryClient,
    operator_client: FeaturesOperatorClient,
    force: bool,
    no_validation: bool,
    ignore_validation_errors: bool,
):
    """
    Register Feature Store Data Source Objects

    Args:
        qwak_python_files: a list of python files containing qwak package imports
        registry: FeatureRegistryClient
        operator_client: features operator grpc client
        force: boolean determining if to force register all encountered Data Source objects
        no_validation: whether to validate entities
        ignore_validation_errors: whether to ignore and continue registering objects after encountering validation errors
    """
    with qwak_spinner(
        begin_text="Finding Data Sources to register", print_callback=print
    ):
        qwak_sources = extract_class_objects(qwak_python_files, BaseSource)

    print(f"👀 Found {len(qwak_sources)} Data Sources")
    for data_source, source_file_path in qwak_sources:
        validation_failed = False

        if no_validation:
            print("Skipping data source validation")
        else:
            try:
                _handle_data_source_validation(operator_client, data_source)
            except Exception as e:
                print(str(e))
                validation_failed = True

        if validation_failed and not ignore_validation_errors:
            print("Not continuing to registration due to failure in validation")
            exit(1)

        existing_source = registry.get_data_source_by_name(data_source.name)
        if existing_source:
            if ask_yesno(
                f"Update existing Data Source '{data_source.name}' from source file '{source_file_path}'?",
                force,
            ):
                registry.update_data_source(
                    existing_source.data_source.data_source_definition.data_source_id,
                    data_source._to_proto(),
                )
        else:
            if ask_yesno(
                f"Create Data Source '{data_source.name}' from source file '{source_file_path}'?",
                force,
            ):
                registry.create_data_source(data_source._to_proto())
    print(DELIMITER)


def _handle_data_source_validation(
    operator_client: FeaturesOperatorClient,
    data_source: BaseSource,
):
    print(f"Validating '{data_source.name}' data source")
    with qwak_spinner(begin_text="", print_callback=print):
        result = operator_client.validate_data_source_blocking(
            data_source_spec=data_source._to_proto(), num_samples=10
        )

    response = getattr(result, result.WhichOneof("type"))
    if isinstance(response, ValidationSuccessResponse):
        print_validation_outputs(response.outputs.stdout, response.outputs.stderr)
        print("✅ Validation completed successfully, got data source columns:")

        table = [
            (x.column_name, x.spark_type) for x in response.spark_column_description
        ]
        print(tabulate(table, headers=["column name", "type"]))
    else:
        raise QwakException(f"🧨 Validation failed: \n{response}")


def _register_features_sets(
    qwak_python_files: List[Tuple[str, str]],
    registry: FeatureRegistryClient,
    force: bool,
    git_commit: str,
    no_validation: bool,
    ignore_validation_errors: bool,
):
    """
    Register Feature Store Feature Set Objects

    Args:
        qwak_python_files: a list of python files containing qwak package imports
        registry: FeatureRegistryClient
        force: boolean determining if to force register all encountered Feature Set objects
        git_commit: the git commit of the parent folder
        no_validation: whether to validate entities
        ignore_validation_errors: whether to ignore and continue registering objects after encountering validation errors
    """
    with qwak_spinner(
        begin_text="Finding Feature Sets to register", print_callback=print
    ):
        qwak_feature_sets = extract_class_objects(qwak_python_files, BaseFeatureSet)

    print(f"👀 Found {len(qwak_feature_sets)} Feature Set(s)")

    for featureset, source_file_path in qwak_feature_sets:
        featureset = cast(BaseFeatureSet, featureset)
        existing_feature_set: ProtoGetFeatureSetByNameResponse = (
            registry.get_feature_set_by_name(featureset.name)
        )

        registration: bool = False
        if existing_feature_set:
            # Provide entity information of registered feature set before any other operation
            if featureset.key:
                featureset.entity = (
                    existing_feature_set.feature_set.feature_set_definition.feature_set_spec.entity.entity_spec.name
                )

            registration = ask_yesno(
                f"Update existing feature set '{featureset.name}' from source file '{source_file_path}'?",  # nosec B608
                force,
            )
        else:
            registration = ask_yesno(
                f"Create new feature set '{featureset.name}' from source file '{source_file_path}'?",
                force,
            )

        if registration:
            features: Optional[List[ProtoFeature]] = []
            artifact_url: Optional[str] = None

            features, artifact_url = _validate_featureset(
                featureset=featureset,
                no_validation=no_validation,
            )

            proto_feature_set, _ = featureset._to_proto(
                git_commit=git_commit,
                features=features,
                feature_registry=registry,
                artifact_url=artifact_url,
            )

            if existing_feature_set:
                registry.update_feature_set(
                    existing_feature_set.feature_set.feature_set_definition.feature_set_id,
                    proto_feature_set,
                )
            else:
                _register_new_feature_set(
                    new_feature_set=featureset,
                    entity_key=proto_feature_set.entity,
                    registry=registry,
                    git_commit=git_commit,
                    features=features,
                    artifact_url=artifact_url,
                )


def _register_new_feature_set(
    new_feature_set: BaseFeatureSet,
    entity_key: ProtoEntityDefinition,
    registry: FeatureRegistryClient,
    git_commit: str,
    features: Optional[List[ProtoFeature]],
    artifact_url: Optional[str] = None,
):
    # Create entity for the defined key and set it as the fs's entity
    if new_feature_set.key:
        new_entity: Entity = Entity._from_proto(proto=entity_key)
        try:
            new_entity.register()
        except QwakException:
            raise QwakException(
                f"Failed to create key for {new_feature_set.name}, "
                f"aborting feature set creation"
            )
        new_feature_set.entity = new_entity.name

    # this is done to retrieve the entities metadata
    proto_feature_set, _ = new_feature_set._to_proto(
        git_commit, features, registry, artifact_url=artifact_url
    )

    try:
        registry.create_feature_set(proto_feature_set)
    # rollback entity creation in case fs registration failed
    except QwakException as e1:
        try:
            if new_feature_set.key:
                registry.delete_entity(entity_id=proto_feature_set.entity.entity_id)
        except QwakException:
            raise e1
        raise e1


def _handle_featureset_validation(
    featureset: BaseFeatureSet,
) -> Tuple[List[ProtoFeature], Optional[str]]:
    print(f"Validating '{featureset.name}' feature set")
    with qwak_spinner(begin_text="", print_callback=print):
        from qwak.feature_store.validations.validator import FeaturesOperatorValidator

        v = FeaturesOperatorValidator()
        response: ValidationResponse
        artifact_url: Optional[str]

        response, artifact_url = v.validate_featureset(featureset=featureset)
    if isinstance(response, SuccessValidationResponse):
        print_validation_outputs(response.stdout, response.stderr)
        print("✅ Validation completed successfully, got data source columns:")
        table = [(x.feature_name, x.feature_type) for x in response.features]
        print(tabulate(table, headers=["column name", "type"]))
        return response.features, artifact_url
    else:
        raise QwakException(f"🧨 Validation failed: \n{response}")


def _get_features_from_spark_columns_description(
    spark_columns_description: List[SparkColumnDescription],
) -> Optional[List[ProtoFeature]]:
    if spark_columns_description:
        spark_features = []
        for spark_column in spark_columns_description:
            feature_col_name_list = str(spark_column.column_name).split(".")
            feature_name = (
                feature_col_name_list[1]
                if feature_col_name_list.__len__() == 2
                else spark_column.column_name
            )
            spark_features.append(
                ProtoFeature(
                    feature_name=feature_name,
                    feature_type=spark_column.spark_type,
                )
            )
        return spark_features
    else:
        return None


def _validate_featureset(
    featureset: BaseFeatureSet,
    no_validation: bool,
) -> Tuple[List[ProtoFeature], Optional[str]]:
    """
    Validates featureset transformation
    Args:
        featureset: BaseFeatureSet featureset
        no_validation: skip validation
        operator: Operator client
        registry: Registry client
    Returns:
        Optional list of features returned from validation
    """
    features: List[ProtoFeature] = []
    artifact_url: Optional[str] = None
    if not no_validation:
        try:
            features, artifact_url = _handle_featureset_validation(
                featureset=featureset
            )
        except Exception as e:
            print(str(e))
            print("Not continuing to registration due to failure in validation")
            exit(1)
    else:
        print(f"Skipping validation for '{featureset.name}' feature set")
    return features, artifact_url


def print_validation_outputs(stdout: str, stderr: str) -> bool:
    did_print = False

    if stdout or stderr:
        message = "Validation outputs: "

        if stdout:
            message += f"stdout: {stdout}\n "

        if stderr:
            message += f"stderr: {stderr}"

        print(message)
        did_print = True

    return did_print
