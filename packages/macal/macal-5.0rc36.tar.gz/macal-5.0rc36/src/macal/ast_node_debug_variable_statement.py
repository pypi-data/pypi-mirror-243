#
# Product:   Macal
# Author:    Marco Caspers
# Email:     SamaDevTeam@westcon.com
# License:   MIT License
# Date:      24-10-2023
#
# Copyright 2023 Westcon-Comstor
#

# This is the ast node for the debug variable statement.

from __future__ import annotations

from typing import Optional

from .ast_node_expression import AstNodeExpression
from .ast_node_statement import AstNodeStatement
from .ast_nodetype import AstNodetype
from .lex_token import LexToken


class AstNodeDebugVariableStatement(AstNodeStatement):
    def __init__(self, token: LexToken) -> AstNodeDebugVariableStatement:
        super().__init__(token)
        self.expr_type = AstNodetype.DEBUG_VARIABLE_STATEMENT
        self.expr: Optional[AstNodeExpression] = None

    def __str__(self) -> str:
        return f"DebugVariableStatement({self.expr})"

    def __repr__(self) -> str:
        return self.__str__()

    def tree(self, indent: str = "") -> None:
        print(f"{indent}DebugVariableStatement:")
        self.expr.tree(indent + "    ")
