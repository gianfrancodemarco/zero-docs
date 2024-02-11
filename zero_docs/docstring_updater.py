"""
Initialize the DocstringProcessor with a DocstringManager instance. Increments the count of indented blocks by 1 and visits the indented block node. Return the updated indented block after decrementing the number of indented blocks. Leave module node if specified code entity is not present in the code entities list; otherwise, call the parent method to leave the module. Generate docstring for leave_ClassDef function. Generate docstring for leave_FunctionDef method. Generate and return a docstring for the _leave method. Initialize the class with a generator attribute. Update docstrings in the specified Python file using a custom visitor object to parse and modify the file's code. Update docstrings in the specified Python file using a custom visitor object to parse and modify the file's code.
"""
import logging
from typing import Any, Union

import libcst as cst

from zero_docs.config import ZERO_DOCS_CODE_ENTITIES
from zero_docs.docstring_generator import DocstringManager
from zero_docs.enums import CodeEntity

logger = logging.getLogger(__name__)


class DocstringVisitor(cst.CSTTransformer):
    """
    Initialize the DocstringProcessor with a DocstringManager instance.
    
    Increments the count of indented blocks by 1 and visits the indented block node.
    
    Return the updated indented block after decrementing the number of indented blocks.
    
    Leave module node if specified code entity is not present in the code entities list; otherwise, call the parent method to leave the module.
    
    Generate docstring for leave_ClassDef function.
    
    Generate docstring for leave_FunctionDef method.
    
    Generate and return a docstring for the _leave method.
    """

    def __init__(
        self,
        docstring_manager: DocstringManager
    ):
        """
        Initialize the DocstringProcessor with a DocstringManager instance.
        """
        self.docstring_manager = docstring_manager
        self.num_indented_blocks = 0

    def visit_IndentedBlock(self, node: cst.IndentedBlock) -> None:
        """
        Increments the count of indented blocks by 1 and visits the indented block node.
        """
        self.num_indented_blocks += 1
        return super().visit_IndentedBlock(node)

    def leave_IndentedBlock(self, original_node: cst.IndentedBlock, updated_node: cst.IndentedBlock) -> cst.IndentedBlock:
        """
        Return the updated indented block after decrementing the number of indented blocks.
        """
        self.num_indented_blocks -= 1
        return updated_node

    def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> None:
        """
        Leave module node if specified code entity is not present in the code entities list; otherwise, call the parent method to leave the module.
        """
        if CodeEntity.MODULE.value not in ZERO_DOCS_CODE_ENTITIES:
            return super().leave_Module(original_node, updated_node)
        return self._leave(original_node, updated_node, CodeEntity.MODULE)

    def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.ClassDef:
        """
        Generate docstring for leave_ClassDef function.
        """
        # We are generating docstrings for the class after we leave it, so we should temporarily add
        # one indentation level to the number of indented blocks.
        # We should generate the docstring when we enter the class, so we can simplify this logic
        if CodeEntity.CLASS.value not in ZERO_DOCS_CODE_ENTITIES:
            return super().leave_classDef(original_node, updated_node)
        self.num_indented_blocks += 1
        new_leave = self._leave(original_node, updated_node, CodeEntity.CLASS)
        self.num_indented_blocks -= 1
        return new_leave

    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef) -> cst.FunctionDef:
        """
        Generate docstring for leave_FunctionDef method.
        """
        # We are generating docstrings for the function after we leave it, so we should temporarily add
        # one indentation level to the number of indented blocks.
        # We should generate the docstring when we enter the function , so we can simplify this logic
        if CodeEntity.FUNCTION.value not in ZERO_DOCS_CODE_ENTITIES:
            return super().leave_FunctionDef(original_node, updated_node)
        self.num_indented_blocks += 1
        new_leave = self._leave(original_node, updated_node, CodeEntity.FUNCTION)
        self.num_indented_blocks -= 1
        return new_leave

    def _leave(
        self,
        original_node: Union[cst.ClassDef, cst.FunctionDef, cst.Module],
        updated_node: Union[cst.ClassDef, cst.FunctionDef, cst.Module],
        code_entity: CodeEntity
    ) -> Any:
        """
        Generate and return a docstring for the _leave method.
        """
        if not updated_node.get_docstring():
            updated_node_code = cst.parse_module("").code_for_node(updated_node)

            docstring_value = self.docstring_manager.generate(
                code=updated_node_code,
                code_entity=code_entity,
            )
            docstring_value = self.docstring_manager.polish(
                docstring_value, num_indented_blocks=self.num_indented_blocks)

            simple_string = cst.SimpleString(
                value=docstring_value
            )
            expr = cst.Expr(simple_string)

            simple_stmt_line = cst.SimpleStatementLine(
                body=[expr]
            )

            try:
                # Works for FunctionDef and ClassDef
                original_body = updated_node.body.body
                new_body = cst.IndentedBlock(
                    [simple_stmt_line, *original_body])
            except AttributeError:
                # Works for Module
                original_body = updated_node.body
                new_body = [simple_stmt_line, *original_body]

            # Replace the body of the node with the modified body
            return updated_node.with_changes(body=new_body)
        return updated_node


class DocstringUpdater:
    """
    Initialize the class with a generator attribute. Update docstrings in the specified Python file using a custom visitor object to parse and modify the file's code.
    """
    def __init__(self, generator):
        """
        Initialize the class with a generator attribute.
        """
        self.generator = generator

    def update_docstrings(self, filename: str):
        """
        Update docstrings in the specified Python file using a custom visitor object to parse and modify the file's code.
        """
        logger.info(f"Updating docstrings in file: {filename}")
        with open(filename, "r") as f:
            content = f.read()

        module = cst.parse_module(content)

        # Apply changes using the visitor
        module = module.visit(DocstringVisitor(self.generator))

        # Convert the modified CST back to source code
        modified_code = module.code

        # Write the modified code back to the file
        with open(filename, "w") as f:
            f.write(modified_code)
