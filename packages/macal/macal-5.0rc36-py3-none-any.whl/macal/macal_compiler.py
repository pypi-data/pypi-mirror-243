#
# Product:   Macal
# Author:    Marco Caspers
# Email:     SamaDevTeam@westcon.com
# License:   MIT License
# Date:      24-10-2023
#
# Copyright 2023 Westcon-Comstor
#

# This is the new Macal Compiler, it will compile the AST from the parser into "bytecode" for the VM.

from __future__ import annotations

import os
from typing import Optional

from .ast_node_assignment import AstNodeAssignmentStatement
from .ast_node_binary_expression import AstNodeBinaryExpression
from .ast_node_block import AstNodeBlock
from .ast_node_break_statement import AstNodeBreakStatement
from .ast_node_case_statement import AstNodeCaseStatement
from .ast_node_continue_statement import AstNodeContinueStatement
from .ast_node_elif_statement import AstNodeElifStatement
from .ast_node_expression import AstNodeExpression
from .ast_node_foreach_statement import AstNodeForeachStatement
from .ast_node_function_call_statement import AstNodeFunctionCallStatement
from .ast_node_function_call_expression import AstNodeFunctionCallExpression
from .ast_node_function_definition import AstNodeFunctionDefinition
from .ast_node_halt_statement import AstNodeHaltStatement
from .ast_node_if_statement import AstNodeIfStatement
from .ast_node_istype import AstNodeIsType
from .ast_node_include_statement import AstNodeIncludeStatement
from .ast_node_indexed_variable_expression import AstNodeIndexedVariableExpression
from .ast_node_literal_expression import AstNodeLiteralExpression
from .ast_node_print_statement import AstNodePrintStatement
from .ast_node_program import AstNodeProgram
from .ast_node_return_statement import AstNodeReturnStatement
from .ast_node_select_statement import AstNodeSelectStatement
from .ast_node_statement import AstNodeStatement
from .ast_node_switch_statement import AstNodeSwitchStatement
from .ast_node_type_statement import AstNodeTypeStatement
from .ast_node_unary_expression import AstNodeUnaryExpression
from .ast_node_variable_expression import AstNodeVariableExpression
from .ast_node_variable_function_call_expression import AstNodeVariableFunctionCallExpression
from .ast_node_while_statement import AstNodeWhileStatement
from .ast_nodetype import AstNodetype
from .config import SearchPath
from .macal_compiler_scope import NewScope
from .macal_lexer import Lexer
from .macal_opcode import *
from .macal_parser import Parser
from .macal_variable import MacalVariable

class MacalCompiler:
    def __init__(self, verbose: bool):
        self.program: Optional[AstNodeProgram] = None
        self.output: str = None
        self.verbose: bool = verbose
        self.reserved: list[str] = []

    def compile(self, program: AstNodeProgram, reserved: list[str]) -> list:
        self.program = program
        self.reserved = reserved
        scope = NewScope("root")
        instructions = [(Opcode_NEW_SCOPE, "root")]
        for var in reserved:
            scope.new_variable(var.strip())
            instructions.append((Opcode_NEW_VARIABLE, var.strip()))
        self.compile_program(self.program, scope, instructions)
        instructions.append((Opcode_LEAVE_SCOPE, "root"))
        instructions.append((Opcode_HALT, [(Opcode_LOAD_CONSTANT, 0)])) # not really needed, but for clarity and completeness.
        if self.verbose:
            for instruction in instructions:
                print(instruction[0], " ", instruction[1:])
        return instructions

    def compile_program(self, program: AstNodeProgram, scope: NewScope, instructions: list):
        for statement in program.statements:
            self.compile_statement(statement, scope, instructions)

    def compile_statement(self, statement: AstNodeStatement, scope: NewScope, instructions: list):
        if statement.expr_type == AstNodetype.ASSIGNMENT_STATEMENT:
            self.compile_assignment_statement(statement, scope, instructions)
        elif statement.expr_type == AstNodetype.PRINT_STATEMENT:
            self.compile_print_statement(statement, scope, instructions)
        elif statement.expr_type == AstNodetype.FUNCTION_DEFINITION:
            self.compile_function_definition(statement, scope, instructions)
        elif statement.expr_type == AstNodetype.RETURN_STATEMENT:
            self.compile_return_statement(statement, scope, instructions)
        elif statement.expr_type == AstNodetype.FUNCTION_CALL:
            self.compile_function_call_statement(statement, scope, instructions)
        elif statement.expr_type == AstNodetype.FUNCTION_CALL_EXPRESSION:
            self.compile_function_call_expression(statement, scope, instructions)
        elif statement.expr_type == AstNodetype.HALT_STATEMENT:
            self.compile_halt_statement(statement, scope, instructions)
        elif statement.expr_type == AstNodetype.BREAK_STATEMENT:
            self.compile_break_statement(statement, scope, instructions)
        elif statement.expr_type == AstNodetype.CONTINUE_STATEMENT:
            self.compile_continue_statement(statement, scope, instructions)
        elif statement.expr_type == AstNodetype.IF_STATEMENT:
            self.compile_if_statement(statement, scope, instructions)
        elif statement.expr_type == AstNodetype.WHILE_STATEMENT:
            self.compile_while_statement(statement, scope, instructions)
        elif statement.expr_type == AstNodetype.FOREACH_STATEMENT:
            self.compile_foreach_statement(statement, scope, instructions)
        elif statement.expr_type == AstNodetype.SWITCH_STATEMENT:
            self.compile_switch_statement(statement, scope, instructions)
        elif statement.expr_type == AstNodetype.INCLUDE_STATEMENT:
            self.compile_include_statement(statement, scope, instructions)
        elif statement.expr_type == AstNodetype.SELECT_STATEMENT:
            self.compile_select_statement(statement, scope, instructions)
        else:
            raise Exception(f"Unknown statement type {statement.expr_type} @ {statement.line}:{statement.column}")

    def compile_block(self, statement: AstNodeBlock, scope: NewScope, instructions: list):
        if statement.expr_type != AstNodetype.BLOCK:
            raise Exception(f"Expected block, got {statement.expr_type} @ {statement.line}:{statement.column}")
        #child = scope.new_child("block")
        #instructions.append((Opcode_NEW_SCOPE, child.name))
        for statement in statement.statements:
            self.compile_statement(statement, scope, instructions)
        #instructions.append((Opcode_LEAVE_SCOPE, child.name))

    # statement fucntions

    def compile_print_statement(self, statement: AstNodePrintStatement, scope: NewScope, instructions: list):
        if statement.expr_type != AstNodetype.PRINT_STATEMENT:
            raise Exception(f"Expected print statement, got {statement.expr_type} @ {statement.line}:{statement.column}")
        args = []
        for arg in statement.args:
            self.compile_expression(arg, scope, args)
        instructions.append((Opcode_PRINT, len(statement.args), args))

    def compile_function_definition(self, statement: AstNodeFunctionDefinition, scope: NewScope, instructions: list):
        if statement.expr_type != AstNodetype.FUNCTION_DEFINITION:
            raise Exception(f"Expected function definition, got {statement.expr_type} @ {statement.line}:{statement.column}")
        child = scope.new_child(statement.name)
        scope.functions.append(child)
        child.is_function = True
        params = []
        for param in statement.parameters:
            params.append((Opcode_NEW_VARIABLE, param.name))
            child.variables.append(MacalVariable(param.name, child))

        fndef = None
        if statement.body is not None:
            blk = []
            self.compile_block(statement.body, child, blk)
            fndef = (Opcode_FUNCTION_DEFINITION, child.name, params, blk)

        if statement.external:
            fndef = (Opcode_EXTERN_FUNCTION_DEFINITION, statement.name, params, statement.module, statement.function)
            child.is_extern_function_definition = True

        if fndef is None:
            raise Exception(f"Function definition without body @ {statement.line}:{statement.column}")
        
        child.function_definition.append(fndef)
        instructions.append(fndef)
       
    def compile_assignment_statement(self, statement: AstNodeAssignmentStatement, scope: NewScope, instructions: list):
        if statement.expr_type != AstNodetype.ASSIGNMENT_STATEMENT:
            raise Exception(f"Expected assignment statement, got {statement.expr_type} @ {statement.line}:{statement.column}")
        var = scope.get_variable(statement.lhs.name)
        if var is None:
            instructions.append((Opcode_NEW_VARIABLE, statement.lhs.name))
            scope.variables.append(MacalVariable(statement.lhs.name, scope))
        lhs = []
        self.compile_expression(statement.lhs, scope, lhs)
        op = statement.operator
        rhs = []
        self.compile_expression(statement.rhs, scope, rhs)
        if op == "=":
            instructions.append((Opcode_STORE_VARIABLE, lhs, rhs, statement.append))
            return
        if statement.append:
            raise Exception(f"Operator {op} not supported for append to array @ {statement.line}:{statement.column}")
        opcode = 0
        if op == "+=":
            opcode = Opcode_ADD
        elif op == "-=":
            opcode = Opcode_SUB
        elif op == "*=":
            opcode = Opcode_MUL
        elif op == "/=":
            opcode = Opcode_DIV
        elif op == "%=":
            opcode = Opcode_MOD
        elif op == "^=":
            opcode = Opcode_POW
        else:
            raise Exception(f"Unknown assignment operator {op} @ {statement.line}:{statement.column}")
        instructions.append((Opcode_STORE_VARIABLE, lhs, [(opcode, lhs, rhs)]))

    def compile_return_statement(self, statement: AstNodeReturnStatement, scope: NewScope, instructions: list):
        if statement.expr_type != AstNodetype.RETURN_STATEMENT:
            raise Exception(f"Expected return statement, got {statement.expr_type} @ {statement.line}:{statement.column}")
        value = []
        if statement.expr is not None:
            self.compile_expression(statement.expr, scope, value)
        instructions.append((Opcode_RET, value))

    def compile_halt_statement(self, statement: AstNodeHaltStatement, scope: NewScope, instructions: list):
        if statement.expr_type != AstNodetype.HALT_STATEMENT:
            raise Exception(f"Expected halt statement, got {statement.expr_type} @ {statement.line}:{statement.column}")
        value = []
        if statement.expr is not None:
            self.compile_expression(statement.expr, scope, value)
        instructions.append((Opcode_HALT, value))

    def compile_break_statement(self, statement: AstNodeBreakStatement, scope: NewScope, instructions: list):
        if statement.expr_type != AstNodetype.BREAK_STATEMENT:
            raise Exception(f"Expected break statement, got {statement.expr_type} @ {statement.line}:{statement.column}")
        instructions.append((Opcode_BREAK,))

    def compile_continue_statement(self, statement: AstNodeContinueStatement, scope: NewScope, instructions: list):
        if statement.expr_type != AstNodetype.CONTINUE_STATEMENT:
            raise Exception(f"Expected continue statement, got {statement.expr_type} @ {statement.line}:{statement.column}")
        instructions.append((Opcode_CONTINUE,))

    def compile_if_statement(self, statement: AstNodeIfStatement, scope: NewScope, instructions: list):
        if statement.expr_type != AstNodetype.IF_STATEMENT:
            raise Exception(f"Expected if statement, got {statement.expr_type} @ {statement.line}:{statement.column}")
        expr = []
        self.compile_expression(statement.condition, scope, expr)
        blk = []
        self.compile_block(statement.block, scope, blk)
        elifs = []
        for elif_statement in statement.elif_block_list:
            self.compile_elif_statement(elif_statement, scope, elifs)
        elseblk = []
        if statement.else_block is not None:
            block = statement.else_block
            block.expr_type = AstNodetype.BLOCK
            self.compile_block(statement.else_block, scope, elseblk)
        instructions.append((Opcode_IF, expr, blk, elifs, (Opcode_ELSE, elseblk)))

    def compile_elif_statement(self, statement: AstNodeElifStatement, scope: NewScope, instructions: list):
        if statement.expr_type != AstNodetype.ELIF_STATEMENT:
            raise Exception(f"Expected elif statement, got {statement.expr_type} @ {statement.line}:{statement.column}")
        expr = []
        self.compile_expression(statement.condition, scope, expr)
        blk = []
        self.compile_block(statement.block, scope, blk)
        instructions.append((Opcode_ELIF, expr, blk))

    def compile_foreach_statement(self, statement: AstNodeForeachStatement, scope: NewScope, instructions: list):
        if statement.expr_type != AstNodetype.FOREACH_STATEMENT:
            raise Exception(f"Expected foreach statement, got {statement.expr_type} @ {statement.line}:{statement.column}")
        expr = []
        self.compile_expression(statement.expr, scope, expr)
        blk = []
        fescope = scope.new_child("foreach")
        fescope.new_variable("it")
        self.compile_block(statement.block, fescope, blk)
        scope.discard_child(fescope)
        instructions.append((Opcode_FOREACH, expr, blk))

    def compile_while_statement(self, statement: AstNodeWhileStatement, scope: NewScope, instructions: list):
        if statement.expr_type != AstNodetype.WHILE_STATEMENT:
            raise Exception(f"Expected while statement, got {statement.expr_type} @ {statement.line}:{statement.column}")
        expr = []
        self.compile_expression(statement.condition, scope, expr)
        blk = []
        self.compile_block(statement.block, scope, blk)
        instructions.append((Opcode_WHILE, expr, blk))

    def compile_switch_statement(self, statement: AstNodeSwitchStatement, scope: NewScope, instructions: list):
        if statement.expr_type != AstNodetype.SWITCH_STATEMENT:
            raise Exception(f"Expected select statement, got {statement.expr_type} @ {statement.line}:{statement.column}")
        expr = []
        self.compile_expression(statement.expr, scope, expr)
        
        switch = {}
        for case in statement.cases:
            csw = []
            self.compile_case_statement(case, scope, csw)
            if csw[0][1] in switch.keys():
                raise Exception(f"Duplicate case statement {csw[0][1]} @ {statement.line}:{statement.column}")
            switch[csw[0][1]] = csw[0][2]
        default = []
        if statement.default is not None:
            self.compile_block(statement.default.block, scope, default)
        instructions.append((Opcode_SWITCH, expr, switch, default))

    def compile_case_statement(self, statement: AstNodeCaseStatement, scope: NewScope, instructions: list):
        if statement.expr_type != AstNodetype.CASE_STATEMENT:
            raise Exception(f"Expected case statement, got {statement.expr_type} @ {statement.line}:{statement.column}")
        expr = []
        self.compile_expression(statement.expr, scope, expr)
        if expr[0][0] != Opcode_LOAD_CONSTANT:
            raise Exception(f"Case expression must be a constant, got {expr[0][0]} @ {statement.line}:{statement.column}")
        blk = []
        self.compile_block(statement.block, scope, blk)
        instructions.append((Opcode_CASE, expr[0][1], blk))

    def compile_select_statement(self, statement: AstNodeSelectStatement, scope: NewScope, instructions: list):
        if statement.expr_type != AstNodetype.SELECT_STATEMENT:
            raise Exception(f"Expected select statement, got {statement.expr_type} @ {statement.line}:{statement.column}")
        fields = {}
        for field in statement.Fields:
            fields[field.fieldname] = field.altfieldname
        from_expr = []    
        self.compile_expression(statement.From, scope, from_expr)
        where_expr = []
        if statement.Where is not None:
            self.compile_expression(statement.Where, scope, where_expr, True)
        into_expr = []
        self.compile_expression(statement.Into, scope, into_expr, True)
        instructions.append((Opcode_SELECT, fields, from_expr, where_expr, statement.distinct, statement.merge, into_expr))

    def compile_function_call_statement(self, statement: AstNodeFunctionCallStatement, scope: NewScope, instructions: list):
        if statement.expr_type != AstNodetype.FUNCTION_CALL:
            raise Exception(f"Expected function call, got {statement.expr_type} @ {statement.line}:{statement.column}")
        func = scope.get_function(statement.name)
        if func is None:
            raise Exception(f"Unknown function {statement.name} @ {statement.line}:{statement.column}")
        args = []
        for arg in statement.args:
            self.compile_expression(arg, scope, args)
        instructions.append((Opcode_CALL, statement.name, len(statement.args), args))

    def compile_is_type_statement(self, statement: AstNodeIsType, scope: NewScope, instructions: list):
        if statement.expr_type != AstNodetype.IS_TYPE_STATEMENT:
            raise Exception(f"Expected is type statement, got {statement.expr_type} @ {statement.line}:{statement.column}")
        expr = []
        self.compile_expression(statement.expr, scope, expr)
        instructions.append((Opcode_IS_TYPE, expr, statement.TypeToCheck))

    def compile_type_statement(self, statement: AstNodeTypeStatement, scope: NewScope, instructions: list):
        if statement.expr_type != AstNodetype.TYPE_STATEMENT:
            raise Exception(f"Expected type statement, got {statement.expr_type} @ {statement.line}:{statement.column}")
        expr = []
        self.compile_expression(statement.expr, scope, expr)
        instructions.append((Opcode_TYPE_STATEMENT, expr))

    # Include implementation

    def find_library(self, name: str) -> Optional[str]:
        for path in SearchPath:
            lib_path = os.path.join(path, f"{name}.mcl")
            if os.path.exists(lib_path):
                return lib_path
        return None

    def load_library(self, path: str) -> Optional[str]:
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            return f.read()

    def compile_include_statement(self, statement: AstNodeIncludeStatement, scope: NewScope, instructions: list) -> None:
        for lib in statement.libraries:
            if lib.name in scope.libraries:
                continue
            lib_path = self.find_library(lib.name)
            if lib_path is None:
                raise Exception(f"Library {lib.name} not found at {lib.line}:{lib.column}")
            source = self.load_library(lib_path)
            if source is None:
                raise Exception(f"Library {lib.name} not found at {lib.line}:{lib.column}")
            
            scope.libraries.append(lib.name)
            lib_scope = scope.new_child(lib.name)
            lib_scope.is_library = True
            instructions.append((Opcode_NEW_SCOPE, lib.name))
            lex = Lexer(source)
            tokens = lex.tokenize()
            parser = Parser(tokens, lib_path)
            ast = parser.parse()
            self.compile_program(ast, lib_scope, instructions)

    # expression functions.

    def compile_function_call_expression(self, expression: AstNodeFunctionCallExpression, scope: NewScope, instructions: list):
        if expression.expr_type != AstNodetype.FUNCTION_CALL_EXPRESSION:
            raise Exception(f"Expected function call expression, got {expression.expr_type} @ {expression.line}:{expression.column}")
        args = []
        func = scope.get_function(expression.name)
        if func is None:
            raise Exception(f"Unknown function {expression.name} @ {expression.line}:{expression.column}")
        for arg in expression.args:
            self.compile_expression(arg, scope, args)
        instructions.append((Opcode_CALL, expression.name, len(expression.args), args))

    def compile_expression(self, expression: AstNodeExpression, scope: NewScope, instructions: list, allow_new_variable: bool = False):
        if expression.expr_type == AstNodetype.BINARY_EXPRESSION:
            self.compile_binary_expression(expression, scope, instructions, allow_new_variable=allow_new_variable)
        elif expression.expr_type == AstNodetype.LITERAL_EXPRESSION:
            self.compile_literal_expression(expression, scope, instructions)
        elif expression.expr_type == AstNodetype.UNARY_EXPRESSION:
            self.compile_unary_expression(expression, scope, instructions)
        elif expression.expr_type == AstNodetype.VARIABLE_EXPRESSION:
            self.compile_variable_expression(expression, scope, instructions, allow_new_variable=allow_new_variable)
        elif expression.expr_type == AstNodetype.FUNCTION_CALL_EXPRESSION:
            self.compile_function_call_expression(expression, scope, instructions)
        elif expression.expr_type == AstNodetype.INDEXED_VARIABLE_EXPRESSION:
            self.compile_indexed_variable_expression(expression, scope, instructions)
        elif expression.expr_type == AstNodetype.VARIABLE_FUNCTION_CALL_EXPRESSION:
            self.compile_variable_function_call_expression(expression, scope, instructions)
        elif expression.expr_type == AstNodetype.IS_TYPE_STATEMENT:
            self.compile_is_type_statement(expression, scope, instructions)
        elif expression.expr_type == AstNodetype.TYPE_STATEMENT:
            self.compile_type_statement(expression, scope, instructions)
        else:
            raise Exception(f"Unknown expression type {expression.expr_type} @ {expression.line}:{expression.column}")

    def compile_binary_expression(self, expression: AstNodeBinaryExpression, scope: NewScope, instructions: list, allow_new_variable: bool = False):
        if expression.expr_type != AstNodetype.BINARY_EXPRESSION:
            raise Exception(f"Expected binary expression, got {expression.expr_type} @ {expression.line}:{expression.column}")
        lhs = []
        self.compile_expression(expression.left, scope, lhs, allow_new_variable=allow_new_variable)
        rhs = []
        self.compile_expression(expression.right, scope, rhs, allow_new_variable=allow_new_variable)
        op = expression.operator
        if op == "+=" or op == "+":
            instructions.append((Opcode_ADD, lhs, rhs))
        elif op == "-=" or op == "-":
            instructions.append((Opcode_SUB, lhs, rhs))
        elif op == "*=" or op == "*":
            instructions.append((Opcode_MUL, lhs, rhs))
        elif op == "/=" or op == "/":
            instructions.append((Opcode_DIV, lhs, rhs))
        elif op == "%=" or op == "%":
            instructions.append((Opcode_MOD, lhs, rhs))
        elif op == "^=" or op == "^":
            instructions.append((Opcode_POW, lhs, rhs))
        elif op == ">=":
            instructions.append((Opcode_GTE, lhs, rhs))
        elif op == "<=":
            instructions.append((Opcode_LTE, lhs, rhs))
        elif op == "==":
            instructions.append((Opcode_EQ, lhs, rhs))
        elif op == "!=":
            instructions.append((Opcode_NEQ, lhs, rhs))
        elif op == ">":
            instructions.append((Opcode_GT, lhs, rhs))
        elif op == "<":
            instructions.append((Opcode_LT, lhs, rhs))
        elif op == "and":
            instructions.append((Opcode_AND, lhs, rhs))
        elif op == "or":
            instructions.append((Opcode_OR, lhs, rhs))
        elif op == "xor":
            instructions.append((Opcode_XOR, lhs, rhs))
        elif op == "not":
            instructions.append((Opcode_NOT, lhs, rhs))
        elif op == "&&":
            instructions.append((Opcode_AND, lhs, rhs))
        elif op == "||":
            instructions.append((Opcode_OR, lhs, rhs))
        elif op == "^^":
            instructions.append((Opcode_XOR, lhs, rhs))
        else:
            raise Exception(f"Unknown binary operator {op} @ {expression.line}:{expression.column}")

    def compile_literal_expression(self, expression: AstNodeLiteralExpression, scope: NewScope, instructions: list):
        if expression.expr_type != AstNodetype.LITERAL_EXPRESSION:
            raise Exception(f"Expected literal expression, got {expression.expr_type} @ {expression.line}:{expression.column}")
        instructions.append((Opcode_LOAD_CONSTANT, expression.value))

    def compile_variable_expression(self, expression: AstNodeVariableExpression, scope: NewScope, instructions: list, allow_new_variable: bool = False):
        if expression.expr_type != AstNodetype.VARIABLE_EXPRESSION:
            raise Exception(f"Expected variable expression, got {expression.expr_type} @ {expression.line}:{expression.column}")
        var = scope.get_variable(expression.name)
        if var is None and allow_new_variable:
            var = scope.new_variable(expression.name)
        if var is None:
            raise Exception(f"Unknown variable {expression.name} @ {expression.line}:{expression.column}")
        else:
            instructions.append((Opcode_LOAD_VARIABLE, expression.name))

    def compile_indexed_variable_expression(self, expression: AstNodeIndexedVariableExpression, scope: NewScope, instructions: list):
        if expression.expr_type != AstNodetype.INDEXED_VARIABLE_EXPRESSION:
            raise Exception(f"Expected indexed variable expression, got {expression.expr_type} @ {expression.line}:{expression.column}")
        var = scope.get_variable(expression.name)
        if var is None:
            raise Exception(f"Unknown variable {expression.name} @ {expression.line}:{expression.column}")
        var_index = []
        for index in expression.index:
            self.compile_expression(index, scope, var_index)
        instructions.append((Opcode_LOAD_VARIABLE, expression.name, var_index))        

    def compile_variable_function_call_expression(self, expression: AstNodeVariableFunctionCallExpression, scope: NewScope, instructions: list):
        print("compile_variable_function_call_expression")
        if expression.expr_type != AstNodetype.VARIABLE_FUNCTION_CALL_EXPRESSION:
            raise Exception(f"Expected variable function call expression, got {expression.expr_type} @ {expression.line}:{expression.column}")
        print(expression.name)
        for arg in expression.args:
            self.compile_expression(arg, scope, instructions)
        raise Exception("variable function call expression Not implemented")

    def compile_unary_expression(self, expression: AstNodeUnaryExpression, scope: NewScope, instructions: list):
        if self.verbose:
            print("compile_unary_expression")
        if expression.expr_type != AstNodetype.UNARY_EXPRESSION:
            raise Exception(f"Expected unary expression, got {expression.expr_type} @ {expression.line}:{expression.column}")
        if self.verbose:
            print(expression.operator)
        op = expression.operator
        rhs = []
        self.compile_expression(expression.expr, scope, rhs)
        if op == "-":
            instructions.append((Opcode_SUB, rhs))
        elif op == "+":
            instructions.append((Opcode_ADD, rhs))
        elif op == "not":
            instructions.append((Opcode_NOT, rhs))
        else:
            raise Exception(f"Unknown unary operator {op} @ {expression.line}:{expression.column}")

