#
# Product:   Macal
# Author:    Marco Caspers
# Email:     SamaDevTeam@westcon.com
# License:   MIT License
# Date:      24-10-2023
#
# Copyright 2023 Westcon-Comstor
#

# This is the expression node for the AST.

from __future__ import annotations

from typing import Any, Optional

from .ast_node_expression import AstNodeExpression
from .ast_nodetype import AstNodetype
from .lex_token import LexToken
from .macal_conversions import convertToValue
from .bytecode_register import BytecodeRegister


class AstNodeRegisterExpression(AstNodeExpression):
    def __init__(
        self, token: LexToken, register: BytecodeRegister
    ) -> AstNodeRegisterExpression:
        super().__init__(token)
        self.expr_type = AstNodetype.REGISTER_EXPRESSION
        self.register: BytecodeRegister = register

    def __str__(self) -> str:
        return f"AstNodeRegisterExpression({self.register.name})"

    def __repr__(self) -> str:
        return self.__str__()

    def tree(self, indent: str = "") -> None:
        print(f"{indent}RegisterExpression:")
        print(f"{indent}    {self.register.name}")
