"""Tests enforcing parity between proto definitions and Pydantic models.

The proto definitions in cq-proto are the source of truth for the data
schema. The Pydantic models in models.py must stay in sync. These tests
introspect the generated _pb2 descriptors and assert that the Pydantic
models have matching fields and enum values. If someone runs
`make generate` after a proto change without updating models.py,
these tests fail.
"""

from cq.cqpb import knowledge_unit_pb2 as ku_pb
from cq.models import (
    Context,
    Evidence,
    Flag,
    FlagReason,
    Insight,
    KnowledgeUnit,
    Tier,
)


def _proto_field_names(descriptor) -> set[str]:
    """Extract field names from a protobuf message descriptor."""
    return {f.name for f in descriptor.fields}


def _proto_enum_values(descriptor) -> set[str]:
    """Extract enum value names from a protobuf enum descriptor."""
    return {v.name for v in descriptor.values}


def _pydantic_field_names(model) -> set[str]:
    """Extract field names from a Pydantic model."""
    return set(model.model_fields.keys())


class TestKnowledgeUnitFieldParity:
    """Every proto field must have a corresponding Pydantic field."""

    def test_all_proto_fields_present_in_pydantic(self):
        proto_fields = _proto_field_names(ku_pb.KnowledgeUnit.DESCRIPTOR)
        pydantic_fields = _pydantic_field_names(KnowledgeUnit)
        missing = proto_fields - pydantic_fields
        assert not missing, f"Proto fields missing from KnowledgeUnit model: {missing}"

    def test_no_extra_pydantic_fields(self):
        proto_fields = _proto_field_names(ku_pb.KnowledgeUnit.DESCRIPTOR)
        pydantic_fields = _pydantic_field_names(KnowledgeUnit)
        extra = pydantic_fields - proto_fields
        assert not extra, f"Pydantic fields not in proto: {extra}"


class TestInsightFieldParity:
    def test_all_proto_fields_present_in_pydantic(self):
        proto_fields = _proto_field_names(ku_pb.Insight.DESCRIPTOR)
        pydantic_fields = _pydantic_field_names(Insight)
        missing = proto_fields - pydantic_fields
        assert not missing, f"Proto fields missing from Insight model: {missing}"

    def test_no_extra_pydantic_fields(self):
        proto_fields = _proto_field_names(ku_pb.Insight.DESCRIPTOR)
        pydantic_fields = _pydantic_field_names(Insight)
        extra = pydantic_fields - proto_fields
        assert not extra, f"Pydantic fields not in proto: {extra}"


class TestContextFieldParity:
    def test_all_proto_fields_present_in_pydantic(self):
        proto_fields = _proto_field_names(ku_pb.Context.DESCRIPTOR)
        pydantic_fields = _pydantic_field_names(Context)
        missing = proto_fields - pydantic_fields
        assert not missing, f"Proto fields missing from Context model: {missing}"

    def test_no_extra_pydantic_fields(self):
        proto_fields = _proto_field_names(ku_pb.Context.DESCRIPTOR)
        pydantic_fields = _pydantic_field_names(Context)
        extra = pydantic_fields - proto_fields
        assert not extra, f"Pydantic fields not in proto: {extra}"


class TestEvidenceFieldParity:
    def test_all_proto_fields_present_in_pydantic(self):
        proto_fields = _proto_field_names(ku_pb.Evidence.DESCRIPTOR)
        pydantic_fields = _pydantic_field_names(Evidence)
        missing = proto_fields - pydantic_fields
        assert not missing, f"Proto fields missing from Evidence model: {missing}"

    def test_no_extra_pydantic_fields(self):
        proto_fields = _proto_field_names(ku_pb.Evidence.DESCRIPTOR)
        pydantic_fields = _pydantic_field_names(Evidence)
        extra = pydantic_fields - proto_fields
        assert not extra, f"Pydantic fields not in proto: {extra}"


class TestFlagFieldParity:
    def test_all_proto_fields_present_in_pydantic(self):
        proto_fields = _proto_field_names(ku_pb.Flag.DESCRIPTOR)
        pydantic_fields = _pydantic_field_names(Flag)
        missing = proto_fields - pydantic_fields
        assert not missing, f"Proto fields missing from Flag model: {missing}"

    def test_no_extra_pydantic_fields(self):
        proto_fields = _proto_field_names(ku_pb.Flag.DESCRIPTOR)
        pydantic_fields = _pydantic_field_names(Flag)
        extra = pydantic_fields - proto_fields
        assert not extra, f"Pydantic fields not in proto: {extra}"


class TestTierEnumParity:
    """Tier StrEnum values must match proto enum value names exactly."""

    def test_all_proto_values_present(self):
        proto_values = _proto_enum_values(ku_pb.Tier.DESCRIPTOR)
        pydantic_values = {member.value for member in Tier}
        missing = proto_values - pydantic_values
        assert not missing, f"Proto Tier values missing from StrEnum: {missing}"

    def test_no_extra_pydantic_values(self):
        proto_values = _proto_enum_values(ku_pb.Tier.DESCRIPTOR)
        pydantic_values = {member.value for member in Tier}
        extra = pydantic_values - proto_values
        assert not extra, f"StrEnum Tier values not in proto: {extra}"


class TestFlagReasonEnumParity:
    """FlagReason StrEnum values must match proto enum value names exactly."""

    def test_all_proto_values_present(self):
        proto_values = _proto_enum_values(ku_pb.FlagReason.DESCRIPTOR)
        pydantic_values = {member.value for member in FlagReason}
        missing = proto_values - pydantic_values
        assert not missing, f"Proto FlagReason values missing from StrEnum: {missing}"

    def test_no_extra_pydantic_values(self):
        proto_values = _proto_enum_values(ku_pb.FlagReason.DESCRIPTOR)
        pydantic_values = {member.value for member in FlagReason}
        extra = pydantic_values - proto_values
        assert not extra, f"StrEnum FlagReason values not in proto: {extra}"
