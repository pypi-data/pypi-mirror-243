#
# Product:   Macal
# Author:    Marco Caspers
# Email:     SamaDevTeam@westcon.com
# License:   MIT License
# Date:      22-11-2023
#
# Copyright 2023 Westcon-Comstor
#

# This is the Macal Virtual Machine Interpreter, it will execute the Macal code.

import importlib
import importlib.util
import os
from typing import Any, Optional, Union, List, Dict

from .ast_nodetype import AstNodetype
from .config import SearchPath
from .macal_conversions import typeFromValue
from .macal_opcode import *
from .macal_variable import MacalVariable
from .macal_vm_scope import NewVMScope

from .python_module_info import ModuleInfo

class ExpressionResult:
    def __init__(self, value: Any, is_variable: bool, is_indexed: bool, index: Optional[List]):
        self.value = value
        self.is_variable = is_variable
        self.is_indexed = is_indexed
        self.index = index

    def __str__(self) -> str:
        return f"ExpressionResult({self.value}, {self.is_variable}, {self.is_indexed}, {self.index})"

class MacalVm:
    def __init__(self, verbose: Optional[bool] = None):
        self.scope: NewVMScope = None
        self.verbose = verbose
        self.exitcode = 0
        self.LoadedModules: Dict[str, ModuleInfo] = {}
        self.ReservedVariables: List[MacalVariable] = []

    def SetReservedVariable(self, name: str, value: Any) -> None:
        var = MacalVariable(name, None)
        if value is None:
            value = AstNodetype.NIL
        var.value = value
        var.value_type = typeFromValue(value)
        self.ReservedVariables.append(var)

    def _setup_reserved_variables(self, scope: NewVMScope) -> None:
        for var in self.ReservedVariables:
            var.scope = scope
            scope.variables.append(var)

    def Execute(self, instructions: List) -> None:
        self._execute_block(instructions, None)
    
    def _execute_block(self, block: List, scope: NewVMScope) -> int:
        # a block is a List of instructions.
        # instructions are tuples, where the first element is the opcode, and the rest are the arguments.
        # we split the instruction into opcode and arguments, and execute the opcode with the arguments.
        result = None
        if scope is not None:
            if scope.continuing:
                scope.continuing = False
            if scope.breaking:
                scope.breaking = False
        
        if self.verbose:
            print("execute_block: ", scope.name if scope is not None else "none")
        for instruction in block:
            op = instruction[0]
            if self.verbose:
                print(f"Block Execute (scope: {scope.name if scope is not None else 'none'}): {instruction[1:]}")
            res = self._execute_instruction(op, instruction[1:], scope)
            if op == Opcode_NEW_SCOPE or op == Opcode_LEAVE_SCOPE:
                scope = res
            if res in [Opcode_HALT, Opcode_CONTINUE, Opcode_BREAK]:
                return res
            if scope.returning:
                result = res
                break
            if scope.halting: break
            if scope.breaking: break
            if scope.continuing: break
        return result

    # Expression for value always outputs a constant value.
    def _execute_expression_for_value(self, expression, scope: NewVMScope, 
                                     expand_to_string: bool = False, 
                                     iswhere:bool = False,
                                     where_item_data: Optional[Dict] = None) -> Any:
        # Note expression needs to be an array of tuples.
        result = self._execute_expression(expression = expression,
                                         scope = scope,
                                         expand_to_string = expand_to_string,
                                         iswhere = iswhere,
                                         where_item_data = where_item_data)
        if not isinstance(result, ExpressionResult):
            raise Exception(f"Expected expression result, got {type(result)}")
        output = result.value
        if result.is_variable:
            output = result.value.value
            if result.is_indexed:
                output = self._execute_walk_index(output, result.index)
        if output == AstNodetype.NIL:
            output = "nil"
        if expand_to_string:
            output = str(output)
        return output

    # Walk index of an indexable value, output is always a constant value.
    def _execute_walk_index(self, source: Any, index_to_walk: List) -> Any:
        if source is None:
            raise ValueError("Source cannot be None")
        if not (isinstance(source, list) or isinstance(source, dict) or isinstance(source, str)):
            raise Exception(f"This variable type ({type(source)}) does not support indexing")
        if index_to_walk is None:
            raise ValueError("Index cannot be None")
        if len(index_to_walk) == 0:
            return source
        value = source
        for index in index_to_walk:
            if isinstance(value, dict):
                if not isinstance(index, str):
                    raise Exception("Record index must be a string")
                if index not in value.keys():
                    raise Exception("Index out of range")
            elif isinstance(value, list) or isinstance(value, str):
                if isinstance(index, int):
                    if index < 0 or index >= len(value):
                        raise Exception("Index out of range")
                else:
                    raise Exception("Array/string Index must be an integer")
            value = value[index]
        return value

    # Assign to index of variable
    def _execute_walk_index_for_store(self, var: MacalVariable, index_to_walk: List, value: Any) -> None:
        if not isinstance(var, MacalVariable):
            raise Exception(f"Not a variable, got: {type(var)}")
        if not (isinstance(var.value, list) or isinstance(var.value, dict) or isinstance(var.value, str)):
            raise Exception(f"This variable type ({type(var.value)}) does not support indexing")
        if index_to_walk is None:
            raise ValueError("Index cannot be None")
        if len(index_to_walk) == 0:
            var.value = value
            return
        value_to_index = var.value
        if len(index_to_walk) > 1:
            for index in index_to_walk[:-1]:
                if isinstance(value_to_index, dict):
                    if not isinstance(index, str):
                        raise Exception(f"Record index must be a string (got {type(index)})")
                    if index not in value_to_index.keys():
                        raise Exception("Index out of range")
                elif isinstance(value_to_index, list) or isinstance(value_to_index, str):
                    if isinstance(index, int):
                        if index < 0 or index >= len(value_to_index):
                            raise Exception("Index out of range")
                    else:
                        raise Exception("Array/string Index must be an integer")
                value_to_index = value_to_index[index]
        value_to_index[index_to_walk[-1]] = value       

    def _execute_expression(self, expression, 
                           scope: NewVMScope, 
                           expand_to_string: bool = False, 
                           allow_new_variable: bool = False,
                           iswhere: bool = False,
                           where_item_data: Optional[Dict] = None) -> ExpressionResult:
        # Note expression needs to be an array of tuples.
        op = expression[0][0]
        expr = expression[0][1:]
        if self.verbose:
            print("Execute expression: ", expr)
        if op == Opcode_LOAD_VARIABLE:
            new_var = False
            name = expr[0]
            var = scope.get_variable(name)
            index = None
            indexed = False
            
            if var is None and iswhere and where_item_data is not None and name in where_item_data.keys():
                return ExpressionResult(where_item_data[name], False, False, None)
            if var is None and allow_new_variable:
                var = scope.new_variable(name)
                new_var = True
            if var is None:
                raise Exception(f"Unknown variable {name}")
            if len(expr) > 1:
                if new_var is True:
                    raise Exception(f"Cannot index a new variable {name}")
                index = []
                for index_expr in expr[1:]:
                    index.append(self._execute_expression_for_value(index_expr, scope, False)) 
                indexed = True
            return ExpressionResult(var, True, indexed, index)
        elif op == Opcode_LOAD_CONSTANT:
            return ExpressionResult(expr[0], False, False, None)
        elif op == Opcode_CALL:
            result = self._execute_function_call(expr, scope)
            return ExpressionResult(result, False, False, None)
        elif op == Opcode_NOT:
            lhs = self._execute_expression_for_value(expr[0], 
                                                    scope, 
                                                    iswhere= iswhere, 
                                                    where_item_data= where_item_data)
            return ExpressionResult(not lhs, False, False, None)
        elif op == Opcode_IS_TYPE:
            var = self._execute_expression(expr[0], scope)
            if var.is_variable is False:
                raise Exception("Expected variable, got constant")
            if var.value is None:
                raise Exception(f"Unknown variable {expr[0]}")
            type_to_check = expr[1]
            var_to_check: MacalVariable = var.value
            type_to_validate = typeFromValue(var_to_check.value)
            if var.is_indexed:
                type_to_validate = typeFromValue(self._execute_walk_index(var_to_check, var.index))
            return ExpressionResult(type_to_validate == type_to_check, False, False, None)
        elif op == Opcode_TYPE_STATEMENT:
            var = self._execute_expression(expr[0], scope)
            if var.is_variable is False:
                raise Exception("Expected variable, got constant")
            if var.value is None:
                raise Exception(f"Unknown variable {expr[0]}")
            var_to_check: MacalVariable = var.value
            result = typeFromValue(var_to_check.value)
            if var.is_indexed:
                result = typeFromValue(self._execute_walk_index(var_to_check, var.index))
            return ExpressionResult(result, False, False, None)
        elif len(expr) == 2:
            return self._execute_binary_expression(expression = expression,
                                                  scope = scope,
                                                  expand_to_string = expand_to_string,
                                                  iswhere = iswhere,
                                                  where_item_data = where_item_data)
        raise Exception(f"Unknown expression opcode {op}")
    
    def _execute_binary_expression(self, expression, scope: NewVMScope, 
                                  expand_to_string: bool = False,
                                  iswhere:bool = False,
                                  where_item_data: Optional[Dict] = None) -> ExpressionResult:
        op = expression[0][0]
        expr = expression[0][1:]
        if self.verbose:
            print("Execute binary expression: ", expr)
        lhs = self._execute_expression_for_value(expression = expr[0],
                                                scope = scope,
                                                expand_to_string = expand_to_string,
                                                iswhere= iswhere,
                                                where_item_data = where_item_data)
        rhs = self._execute_expression_for_value(expression = expr[1],
                                                scope = scope,
                                                expand_to_string = expand_to_string,
                                                iswhere = iswhere,
                                                where_item_data = where_item_data)
        if expand_to_string:
            lhs = str(lhs)
            rhs = str(rhs)
        if op == Opcode_ADD:
            result = lhs + rhs
        elif op == Opcode_SUB:
            result = lhs - rhs
        elif op == Opcode_MUL:
            result = lhs * rhs
        elif op == Opcode_DIV:
            result = lhs / rhs
        elif op == Opcode_MOD:
            result = lhs % rhs
        elif op == Opcode_POW:
            result = lhs ** rhs
        elif op == Opcode_GTE:
            result = lhs >= rhs
        elif op == Opcode_LTE:
            result = lhs <= rhs
        elif op == Opcode_EQ:
            result = lhs == rhs
        elif op == Opcode_NEQ:
            result = lhs != rhs
        elif op == Opcode_GT:
            result = lhs > rhs
        elif op == Opcode_LT:
            result = lhs < rhs
        elif op == Opcode_AND:
            result = lhs and rhs
        elif op == Opcode_OR:
            result = lhs or rhs
        elif op == Opcode_XOR:
            result = lhs ^ rhs
        else:
            raise Exception(f"Unknown expression opcode {op}")
        return ExpressionResult(result, False, False, None)

    def _execute_function_call(self, function, scope: NewVMScope) -> Any:
        name = function[0]
        func_args = function[2]
        func = scope.get_function_definition(name)
        if func is None:
            raise Exception(f"Unknown function {name}")
        params = func[0]
        block  = func[1]
        module = None
        ext_function = None
        if block is None:
            module = func[2]
            ext_function = func[3]
        args = []
        funcscope = scope.new_child(name)
        for i in range(len(params)):
            param = funcscope.new_variable(params[i][1])
            arg = self._execute_expression_for_value([func_args[i]], scope)
            param.value = arg
            args.append(arg)
        if len(func_args) > len(params):
            param.value = [param.value]
            for i in range(len(params), len(func_args)):
                arg = self._execute_expression_for_value([func_args[i]], scope)
                param.value.append(arg)
                args.append(arg)
        if block is not None:
            return_value = self._execute_block(block, funcscope)
        else:
            return_value = self._run_external_function(module, ext_function, args)
        scope.discard_child(funcscope)
        if self.verbose:
            print(scope.name, "returning", return_value, scope.returning)
        return return_value

    def _execute_instruction(self, op: int, instruction, scope: NewVMScope) -> NewVMScope:
        if op == Opcode_NEW_SCOPE:
            name = instruction[0]
            if scope is None:
                scope = NewVMScope(name)
                self._setup_reserved_variables(scope)
                return scope
            child = scope.new_child(name)
            return child
        elif op == Opcode_FUNCTION_DEFINITION:
            name = instruction[0]
            params = instruction[1]
            block = instruction[2]
            scope.function_definitions[name] = (params, block)      
        elif op == Opcode_EXTERN_FUNCTION_DEFINITION:
            name = instruction[0]
            params = instruction[1]
            module = instruction[2]
            function = instruction[3]
            scope.function_definitions[name] = (params, None, module, function)
        elif op == Opcode_LEAVE_SCOPE:
            if scope.parent is not None:
                return scope.parent
        elif op == Opcode_NEW_VARIABLE:
            scope.new_variable(instruction[0])
        elif op == Opcode_STORE_VARIABLE:
            self._execute_assign(instruction, scope)
        elif op == Opcode_PRINT:
            for arg in instruction[1]:
                prnt_scope = scope.new_child("print")
                value = self._execute_expression_for_value([arg], prnt_scope, True)
                scope.discard_child(prnt_scope)
                print(value, end="")
            print()
        elif op == Opcode_RET:
            scope.returning = True
            if len(instruction[0]) > 0:
                retval = self._execute_expression_for_value(instruction[0], scope)
                return retval
            return None
        elif op == Opcode_HALT:
            scope.halting = True
            if len(instruction[0]) > 0:
                self.exitcode = self._execute_expression_for_value(instruction[0], scope)
        elif op == Opcode_BREAK:
            scope.breaking = True
        elif op == Opcode_CONTINUE:
            scope.continuing = True
        elif op == Opcode_CALL:
            return self._execute_function_call(instruction, scope)
        elif op == Opcode_IF:
            if self._execute_expression_for_value(instruction[0], scope):
                return self._execute_block(instruction[1], scope)
            if len(instruction[2]) > 0:
                for elif_statement in instruction[2]:
                    if self._execute_expression_for_value(elif_statement[1], scope):
                        return self._execute_block(elif_statement[2], scope)
            if len(instruction[3]) > 0:
                return self._execute_block(instruction[3][1], scope)
        elif op == Opcode_FOREACH:
            expr = self._execute_expression_for_value(instruction[0], scope)
            if not isinstance(expr, list) and not isinstance(expr, dict) and not isinstance(expr, str):
                raise Exception(f"Expected array, record or string, got {type(expr)}")
            foreach_scope = scope.new_child("foreach")
            it = foreach_scope.new_variable("it")
            for item in expr:
                it.value = item
                result = self._execute_block(instruction[1], foreach_scope)
                if result == Opcode_BREAK or result == Opcode_HALT:
                    break
                if result == Opcode_CONTINUE:
                    continue
            scope.discard_child(foreach_scope)
        elif op == Opcode_WHILE:
            while_scope = scope.new_child("while")
            while self._execute_expression_for_value(instruction[0], scope):
                result = self._execute_block(instruction[1], while_scope)
                if while_scope.breaking or while_scope.halting or while_scope.returning:
                    break
                if while_scope.continuing:
                    continue
            if while_scope.halting:
                scope.halting = True
            scope.discard_child(while_scope)
        elif op == Opcode_SWITCH:
            expr = self._execute_expression_for_value(instruction[0], scope)
            if expr in instruction[1].keys():
                return self._execute_block(instruction[1][expr], scope)
            if len(instruction[2]) > 0:
                return self._execute_block(instruction[2], scope)
        elif op == Opcode_SELECT:
            return self._execute_select(instruction, scope)
        else:
            raise Exception("Unknown instruction: ", op, " @ ", scope.name if scope is not None else "none", " ", instruction)
        return scope

    def _execute_assign(self, instruction, scope: NewVMScope):
        var_instruction    = instruction[0]
        rhs_instruction    = instruction[1]
        append = True if len(instruction) > 2 and instruction[2] else False
        if self.verbose:
            print()
            print("Setting up the assignment:")
            print()
            print("var_instruction    = ", var_instruction)
            print("var name:          = ", var_instruction[0][1])
            print("rhs_instruction    = ", rhs_instruction)
            print("append             = ", append)
            print()
        result = self._execute_expression(var_instruction, scope)
        if result.is_variable is False:
            raise Exception("Expected variable, got constant")
        if result.value is None:
            raise Exception(f"Unknown variable {var_instruction[0][1]}")
        variable_to_assign_to: MacalVariable = result.value            
        value_to_assign = self._execute_expression_for_value(rhs_instruction, scope)
        if self.verbose:
            print("performed the calcualtions:")
            if not result.is_indexed:
                print(f"var ({variable_to_assign_to.name}) = {value_to_assign}")
            else:
                print(f"{variable_to_assign_to.name}{result.index} = {value_to_assign}")
            print("value to be assigned = ", value_to_assign)
        if result.is_indexed:
            self._execute_walk_index_for_store(variable_to_assign_to, result.index, value_to_assign)
        else:
            if append:
                variable_to_assign_to.value.append(value_to_assign)
            else:
                variable_to_assign_to.value = value_to_assign

    def _execute_select(self, instruction, scope: NewVMScope):
        fields = instruction[0]
        where_expr = instruction[2]
        distinct = instruction[3]
        merge = instruction[4]
        destination_data = []

        # get the destination data if we do a merge:
        if merge:
            destination_data = self._execute_expression_for_value(instruction[5], scope)
        # gets the destination variable, allow creation of a new variable if we do not merge.
        into_expr_result = self._execute_expression(instruction[5], scope, allow_new_variable=not merge)
        if into_expr_result.is_variable is False:
            raise Exception("Select into expected variable, got constant")
        into_var: MacalVariable = into_expr_result.value

        # we get the source data by executing the from instruction.
        source_data = self._execute_expression_for_value(instruction[1], scope)
        if source_data is None or source_data is False:
            source_data = []
        # check if we have an array or record, if not, we throw an exception.
        if not isinstance(source_data, list) and not isinstance(source_data, dict):
            raise Exception(f"From expected array or record, got {type(source_data)}")
        if not isinstance(destination_data, List) and not isinstance(destination_data, dict):
            raise Exception(f"Expected array, record or string, got {type(destination_data)}")

        # convert the source data to an array if it is a record.
        if isinstance(source_data, dict):
            source_data = [source_data]

        # if we have a where expression, we filter the source data.
        result_data = []

        if len(where_expr) > 0:
            for item in source_data:
                if self._execute_expression_for_value(where_expr, scope, iswhere=True, where_item_data=item) is False:
                    continue
                if distinct and item not in result_data:
                    result_data.append(item)
                elif not distinct:
                    result_data.append(item)
        else:
            result_data = source_data.copy()
        
        # source data is filtered into the result data.
        # we will now apply the field filters to the result data if we do not have a select all (*).
        if not (len(fields) == 1 and list(fields.keys())[0] == "*"):
            result_data = self._apply_field_filters(fields, result_data)

        # distinct always results in a single record no matter what.
        # also if there is only 1 record in the result data, we also return it as a single record.
        if isinstance(result_data, list) and distinct is True and len(result_data) > 0:
            result_data = result_data[0]

        # if we have a merge, we merge the result data into the destination data.
        if merge is True:
            destination_data = self._merge_data(destination_data, result_data).copy()
        else:
            destination_data = result_data.copy()

        # distinct always results in a single record no matter what.
        # also if there is only 1 record in the result data, we also return it as a single record.
        if isinstance(destination_data, list) and distinct is True and len(destination_data) > 0:
            destination_data = destination_data[0]

        if distinct is True and len(destination_data) == 1:
            destination_data = destination_data[list(destination_data.keys())[0]]

        # we now have the final result data, we store it into the destination variable.
        # we need to take into account if the destination variable has an index or not.
        if into_expr_result.is_indexed:
            self._execute_walk_index_for_store(into_var, into_expr_result.index, destination_data)
        else:
            into_var.value = destination_data

    def _apply_field_filters(self, fields: Dict, source_data: List[Dict]) -> List[Dict]:
        if len(source_data) == 0:
            return [{fields[field]: AstNodetype.NIL for field in fields.keys()}]
        return [{fields[field]: item.get(field, AstNodetype.NIL) for field in fields.keys()} for item in source_data]

    def _merge_data(self, source_data: List[Dict], destination_data: List[Dict]) -> Union[List[Dict], Dict]:
        if isinstance(source_data, dict):
            source_data = [source_data]
        if isinstance(destination_data, dict):
            destination_data = [destination_data]
        if not (isinstance(source_data, list) and isinstance(destination_data, list)):
            raise Exception("MERGE: Type error, both parameters must be arrays.")
        if len(source_data)== 0 and len(destination_data) == 0:
            return []
        if len(source_data) == 0 and len(destination_data) > 0:
            final_data = destination_data
        elif len(source_data) > 0 and len(destination_data) == 0:
            final_data = source_data
        elif len(source_data) > 1 and len(destination_data) > 1 and set(source_data[0].keys()) == set(destination_data[0].keys()):
            final_data = [source_data[0], destination_data[0]]
        elif len(source_data) == 1 and len(destination_data) == 1 and set(source_data[0].keys()) != set(destination_data[0].keys()):
            keys = set().union(source_data[0].keys(), destination_data[0].keys())
            final_data = [{k: source_data[0].get(k, destination_data[0].get(k, AstNodetype.NIL)) for k in keys}]
        # multiple records in each, with the same set of fields, then just append them both.
        elif set(source_data[0].keys()) == set(destination_data[0].keys()):
            final_data = source_data.copy()
            final_data.extend(destination_data)
        # multiple records in each, but with the or different fields, then merge the records and fields.
        elif set(source_data[0].keys()) != set(destination_data[0].keys()):
            keys = set().union(*(d.keys() for d in source_data + destination_data))
            final_data = [{k: d.get(k, AstNodetype.NIL) for k in keys} for d in source_data + destination_data]
        if len(final_data) == 1:
            return final_data[0]
        return final_data

    def _import_module(self, module_name: str) -> Optional[Any]:
        try:
            return importlib.import_module(module_name)
        except ImportError:
            return None

    def _import_module_from_path(self, module_name: str) -> Optional[Any]:
        try:
            for path in SearchPath:
                path = os.path.join(path, f"{module_name}.py")
                if not os.path.exists(path): continue
                spec = importlib.util.spec_from_file_location(module_name, path)
                if spec is None: continue
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return module
        except ImportError as ex:
            self._Error(f"Import error: {ex}")
        return None

    def _run_external_function(self, module_name: str, function_name: str, args ) -> Any:
        module = self.LoadedModules.get(module_name, None)
        if module is None:
            imported_module = self._import_module(module_name)
            if imported_module is None:
                imported_module = self._import_module_from_path(module_name)
                if imported_module is None:
                    raise Exception(f"Module {module_name} not found.")
            module = ModuleInfo(module_name, imported_module)
            self.LoadedModules[module_name] = module
        function = module.functions.get(function_name, None)
        if function is None:
            raise Exception(f"Function {function_name} not found in module {module_name}.")
        result = function(*args)
        if result is None:
            result = AstNodetype.NIL
        return result
        
