"""
A module for updating docstrings in Python files based on a customized visitor implementation.

This module contains two classes: DocstringVisitor and DocstringUpdater, along with helper methods to process and update docstrings in Python files.

Classes:
    DocstringVisitor: A visitor class for processing abstract syntax trees (AST) and generating docstrings for code entities.
    DocstringUpdater: A class for updating docstrings in a Python file based on a customized visitor implementation.

Methods (DocstringVisitor):
    - visit_IndentedBlock: Increment the count of indented blocks and visit the indented block node.
    - leave_IndentedBlock: Decreases the count of indented blocks and returns the updated indented block node.
    - leave_Module: Leave method for processing a Module in an AST, updating docstrings if necessary.
    - leave_ClassDef: Adjust the number of indented blocks temporarily while leaving a ClassDef node.
    - leave_FunctionDef: Leave the function node after applying changes and adjusting the number of indented blocks.
    - _safe_leave: Safely calls the _leave method to update docstrings for a code entity.
    - _leave: Modify the given node by adding a docstring if it does not already have one.

Methods (DocstringUpdater):
    - __init__: Initializes the instance with a generator object.
    - update_docstrings: Updates docstrings of a Python file based on a customized visitor implementation.
"""
import logging
from textwrap import dedent
from typing import Any, Union

import libcst as cst

from zero_docs.config import ZERO_DOCS_CODE_ENTITIES
from zero_docs.docstring_generator import DocstringManager
from zero_docs.enums import CodeEntity

logger = logging.getLogger(__name__)


class DocstringVisitor(cst.CSTTransformer):
    """
    A class that defines a visitor for processing abstract syntax trees (AST) and generating docstrings for code entities.
    
    Attributes:
        - docstring_manager (DocstringManager): An instance of the DocstringManager class that manages docstrings.
        - num_indented_blocks (int): The number of indented blocks in the code.
    
    Methods:
        - visit_IndentedBlock: Increment the count of indented blocks and visit the indented block node.
        - leave_IndentedBlock: Decreases the count of indented blocks and returns the updated indented block node.
        - leave_Module: Leave method for processing a Module in an AST, updating docstrings if necessary.
        - leave_ClassDef: Adjust the number of indented blocks temporarily while leaving a ClassDef node.
        - leave_FunctionDef: Leave the function node after applying changes and adjusting the number of indented blocks.
        - _safe_leave: Safely calls the _leave method to update docstrings for a code entity.
        - _leave: Modify the given node by adding a docstring if it does not already have one.
    """

    def __init__(
        self,
        docstring_manager: DocstringManager
    ):
        """Initialize the DocstringManager.
        
        Args:
            docstring_manager (DocstringManager): An instance of the DocstringManager class.
        
        Attributes:
            docstring_manager (DocstringManager): An instance of the DocstringManager class that manages docstrings.
            num_indented_blocks (int): The number of indented blocks in the code.
        
        """
        self.docstring_manager = docstring_manager
        self.num_indented_blocks = 0

    def visit_IndentedBlock(self, node: cst.IndentedBlock) -> None:
        """Increment the count of indented blocks and visit the indented block node.
        
        Args:
            node (cst.IndentedBlock): The indented block node to be visited.
        
        Returns:
            None
        
        """
        self.num_indented_blocks += 1
        return super().visit_IndentedBlock(node)

    def leave_IndentedBlock(self, original_node: cst.IndentedBlock, updated_node: cst.IndentedBlock) -> cst.IndentedBlock:
        """Decreases the count of indented blocks and returns the updated indented block.
        
        Args:
            original_node (cst.IndentedBlock): The original indented block node.
            updated_node (cst.IndentedBlock): The updated indented block node.
        
        Returns:
            cst.IndentedBlock: The updated indented block node after decreasing the count of indented blocks.
        """
        self.num_indented_blocks -= 1
        return updated_node

    def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> None:
        """
        Leave method for processing a Module in an abstract syntax tree (AST).
        
        Args:
            original_node (cst.Module): The original Module node before any modification.
            updated_node (cst.Module): The updated Module node after processing.
        
        Returns:
            None
        
        Notes:
            This method either calls the superclass leave_Module method if the CodeEntity.MODULE value is not in ZERO_DOCS_CODE_ENTITIES, 
            or invokes the _safe_leave method passing the original_node, updated_node, and CodeEntity.MODULE parameters.
        """
        if CodeEntity.MODULE.value not in ZERO_DOCS_CODE_ENTITIES:
            return super().leave_Module(original_node, updated_node)
        return self._safe_leave(original_node, updated_node, CodeEntity.MODULE)

    def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.ClassDef:
        """Increment the number of indented blocks temporarily when leaving a ClassDef node to generate docstrings for the class.
        
        Args:
            original_node (cst.ClassDef): The original ClassDef node before modification.
            updated_node (cst.ClassDef): The updated ClassDef node after modification.
        
        Returns:
            cst.ClassDef: The modified ClassDef node with added docstrings.
        
        """
        # We are generating docstrings for the class after we leave it, so we should temporarily add
        # one indentation level to the number of indented blocks.
        # We should generate the docstring when we enter the class, so we can simplify this logic
        if CodeEntity.CLASS.value not in ZERO_DOCS_CODE_ENTITIES:
            return super().leave_ClassDef(original_node, updated_node)
        self.num_indented_blocks += 1
        new_leave = self._safe_leave(original_node, updated_node, CodeEntity.CLASS)
        self.num_indented_blocks -= 1
        return new_leave

    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef) -> cst.FunctionDef:
        """Leave the function node after applying changes and adjusting the number of indented blocks for generating docstrings.
        
        Args:
            self: The current instance of the Visitor class.
            original_node (cst.FunctionDef): The original function node before changes.
            updated_node (cst.FunctionDef): The updated function node after applying changes.
        
        Returns:
            cst.FunctionDef: The modified function node with adjusted indented blocks.
        
        Note:
            This function adjusts the number of indented blocks for generating docstrings after processing the function node.
        """
        # We are generating docstrings for the function after we leave it, so we should temporarily add
        # one indentation level to the number of indented blocks.
        # We should generate the docstring when we enter the function , so we can simplify this logic
        if CodeEntity.FUNCTION.value not in ZERO_DOCS_CODE_ENTITIES:
            return super().leave_FunctionDef(original_node, updated_node)
        self.num_indented_blocks += 1
        new_leave = self._safe_leave(original_node, updated_node, CodeEntity.FUNCTION)
        self.num_indented_blocks -= 1
        return new_leave

    def _safe_leave(
        self,
        original_node: Union[cst.ClassDef, cst.FunctionDef, cst.Module],
        updated_node: Union[cst.ClassDef, cst.FunctionDef, cst.Module],
        code_entity: CodeEntity
    ) -> Any:
        """Safely calls the _leave method to update docstrings for a code entity.
        
        This function takes the original node, updated node, and code entity as parameters. It attempts to call the _leave method with these parameters to update the docstring for the given code entity. If an exception occurs during this process, it logs an error message and returns the updated node without the docstring changes.
        
        Args:
            original_node (Union[cst.ClassDef, cst.FunctionDef, cst.Module]): The original node representing the code entity.
            updated_node (Union[cst.ClassDef, cst.FunctionDef, cst.Module]): The updated node representing the code entity.
            code_entity (CodeEntity): The code entity for which the docstring needs to be updated.
        
        Returns:
            Any: The updated node with the docstring changes if successful, otherwise the original updated node without changes.
        """
        try:
            return self._leave(original_node, updated_node, code_entity)
        except Exception as e:
            logger.error(
                f"Error updating docstring for {code_entity.value}: {e}"
            )
            return updated_node

    def _leave(
        self,
        original_node: Union[cst.ClassDef, cst.FunctionDef, cst.Module],
        updated_node: Union[cst.ClassDef, cst.FunctionDef, cst.Module],
        code_entity: CodeEntity
    ) -> Any:
        """Modify the given node by adding a docstring if it does not already have one.
        
        Args:
            original_node (Union[cst.ClassDef, cst.FunctionDef, cst.Module]): The original node before modification.
            updated_node (Union[cst.ClassDef, cst.FunctionDef, cst.Module]): The updated node to check for existing docstring and modify.
            code_entity (CodeEntity): The code entity associated with the node.
        
        Returns:
            Any: The updated node with the added docstring if necessary.
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
    """A class for updating docstrings in a Python file based on a customized visitor implementation.
    
    Attributes:
        generator (object): The generator object used for updating docstrings.
    
    Methods:
        __init__: Initializes the instance with a generator object.
        update_docstrings: Updates docstrings of a Python file based on a customized visitor implementation.
    """
    def __init__(self, generator):
        """Initialize the object with a generator.
        
        Args:
            generator (object): The generator object to be assigned to the instance variable.
        """
        self.generator = generator

    def update_docstrings(self, filename: str):
        """
        Update docstrings of a Python file based on a customized visitor implementation.
        
        Args:
            filename (str): The path of the Python file to update the docstrings in.
        
        Returns:
            None
        """
        with open(filename, "r") as f:
            content = f.read()

        logger.info(dedent(f"""
            Updating docstrings in file: {filename}

            content:
            {content}
        """))

        module = cst.parse_module(content)

        # Apply changes using the visitor
        module = module.visit(DocstringVisitor(self.generator))

        # Convert the modified CST back to source code
        modified_code = module.code

        # Write the modified code back to the file
        with open(filename, "w") as f:
            f.write(modified_code)
