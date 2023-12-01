from enum import Enum
from typing import Dict, List, Optional

from llama_index.bridge.pydantic import BaseModel, Field
from llama_index.schema import TextNode


class _SignatureCaptureType(BaseModel):
    """
    Unfortunately some languages need special options for how to make a signature.

    For example, html element signatures should include their closing >, there is no
    easy way to include this using an always-exclusive system.

    However, using an always-inclusive system, python decorators don't work,
    as there isn't an easy to define terminator for decorators that is inclusive
    to their signature.
    """

    type: str = Field(description="The type string to match on.")
    inclusive: bool = Field(
        description=(
            "Whether to include the text of the node matched by this type or not."
        ),
    )


class _SignatureCaptureOptions(BaseModel):
    start_signature_types: Optional[List[_SignatureCaptureType]] = Field(
        None,
        description=(
            "A list of node types any of which indicate the beginning of the signature."
            "If this is none or empty, use the start_byte of the node."
        ),
    )
    end_signature_types: Optional[List[_SignatureCaptureType]] = Field(
        None,
        description=(
            "A list of node types any of which indicate the end of the signature."
            "If this is none or empty, use the end_byte of the node."
        ),
    )
    name_identifier: str = Field(
        description=(
            "The node type to use for the signatures 'name'.If retrieving the name is"
            " more complicated than a simple type match, use a function which takes a"
            " node and returns true or false as to whether its the name or not. The"
            " first match is returned."
        )
    )


"""
Maps language -> Node Type -> SignatureCaptureOptions

The best way for a developer to discover these is to put a breakpoint at the TIP
tag in _chunk_node, and then create a unit test for some code, and then iterate
through the code discovering the node names.
"""
_DEFAULT_SIGNATURE_IDENTIFIERS: Dict[str, Dict[str, _SignatureCaptureOptions]] = {
    "python": {
        "function_definition": _SignatureCaptureOptions(
            end_signature_types=[_SignatureCaptureType(type="block", inclusive=False)],
            name_identifier="identifier",
        ),
        "class_definition": _SignatureCaptureOptions(
            end_signature_types=[_SignatureCaptureType(type="block", inclusive=False)],
            name_identifier="identifier",
        ),
    },
    "html": {
        "element": _SignatureCaptureOptions(
            start_signature_types=[_SignatureCaptureType(type="<", inclusive=True)],
            end_signature_types=[_SignatureCaptureType(type=">", inclusive=True)],
            name_identifier="tag_name",
        )
    },
    "cpp": {
        "class_specifier": _SignatureCaptureOptions(
            end_signature_types=[_SignatureCaptureType(type="{", inclusive=False)],
            name_identifier="type_identifier",
        ),
        "function_definition": _SignatureCaptureOptions(
            end_signature_types=[_SignatureCaptureType(type="{", inclusive=False)],
            name_identifier="function_declarator",
        ),
    },
    "typescript": {
        "interface_declaration": _SignatureCaptureOptions(
            end_signature_types=[_SignatureCaptureType(type="{", inclusive=False)],
            name_identifier="type_identifier",
        ),
        "lexical_declaration": _SignatureCaptureOptions(
            end_signature_types=[_SignatureCaptureType(type="{", inclusive=False)],
            name_identifier="identifier",
        ),
        "function_declaration": _SignatureCaptureOptions(
            end_signature_types=[_SignatureCaptureType(type="{", inclusive=False)],
            name_identifier="identifier",
        ),
        "class_declaration": _SignatureCaptureOptions(
            end_signature_types=[_SignatureCaptureType(type="{", inclusive=False)],
            name_identifier="type_identifier",
        ),
        "method_definition": _SignatureCaptureOptions(
            end_signature_types=[_SignatureCaptureType(type="{", inclusive=False)],
            name_identifier="property_identifier",
        ),
    },
}


class _ScopeMethod(Enum):
    INDENTATION = "INDENTATION"
    BRACKETS = "BRACKETS"
    HTML_END_TAGS = "HTML_END_TAGS"


class _CommentOptions(BaseModel):
    comment_template: str
    scope_method: _ScopeMethod


_COMMENT_OPTIONS: Dict[str, _CommentOptions] = {
    "cpp": _CommentOptions(
        comment_template="// {}", scope_method=_ScopeMethod.BRACKETS
    ),
    "html": _CommentOptions(
        comment_template="<!-- {} -->", scope_method=_ScopeMethod.HTML_END_TAGS
    ),
    "python": _CommentOptions(
        comment_template="# {}", scope_method=_ScopeMethod.INDENTATION
    ),
    "typescript": _CommentOptions(
        comment_template="// {}", scope_method=_ScopeMethod.BRACKETS
    ),
}

assert all(
    language in _DEFAULT_SIGNATURE_IDENTIFIERS for language in _COMMENT_OPTIONS
), "Not all languages in _COMMENT_OPTIONS are in _DEFAULT_SIGNATURE_IDENTIFIERS"
assert all(
    language in _COMMENT_OPTIONS for language in _DEFAULT_SIGNATURE_IDENTIFIERS
), "Not all languages in _DEFAULT_SIGNATURE_IDENTIFIERS are in _COMMENT_OPTIONS"


class _ScopeItem(BaseModel):
    """Like a Node from tree_sitter, but with only the str information we need."""

    name: str
    type: str
    signature: str


class _ChunkNodeOutput(BaseModel):
    """The output of a chunk_node call."""

    this_document: Optional[TextNode]
    upstream_children_documents: List[TextNode]
    all_documents: List[TextNode]
