import re
import inspect
from abc import abstractmethod
from typing import Any, Dict, List, Optional, Union

class Node:
    @abstractmethod
    def __init__(self, name: str) -> None:
        self._name = name

    def evaluate(self, context: Dict[str, Any], dump_eval: Optional[List[str]] = None) -> Any:
        raise NotImplementedError()

    def dump_structure(self, indent: int = 0) -> str:
        return ("  " * indent + self._name) + "\n"
    

class BinaryOp(Node):
    @abstractmethod
    def __init__(self, name: str, left: Node, op: str, right: Node) -> None:
        super().__init__(name)
        self._left = left
        self._op = op
        self._right = right

    def _eval_bool(self, left_val: bool, right_val: Any) -> bool:
        if isinstance(right_val, (int, float)):
            right_val = right_val != 0
        elif isinstance(right_val, str):
            right_val = right_val.lower() == "true" or right_val == "1"
        elif not isinstance(right_val, bool):
            raise TypeError(f"Type mismatch: Cannot compare bool '{left_val}' with non-bool '{right_val}'")
        
        if self._op == "and":
            return left_val and right_val
        elif self._op == "or":
            return left_val or right_val
        elif self._op == "==":
            return left_val == right_val
        elif self._op == "!=":
            return left_val != right_val
        
        raise RuntimeError(f"Unsupported operator '{self._op}' for bool.")
    
    def _eval_str(self, left_val: str, right_val: Any) -> bool:
        if isinstance(right_val, bool):
            right_val = "true" if right_val else "false"
        elif isinstance(right_val, (int, float)):
            right_val = str(right_val)
        elif not isinstance(right_val, str):
            raise TypeError(f"Type mismatch: Cannot compare string '{left_val}' with non-string '{right_val}'")

        if self._op == "==":
            return left_val == right_val
        elif self._op == "!=":
            return left_val != right_val
        
        raise RuntimeError(f"Unsupported operator '{self._op}' for string.")
    
    def _eval_num(self, left_val: Union[int, float], right_val: Any) -> Union[int, float, bool]:
        if isinstance(right_val, bool):
            right_val = 1 if right_val else 0
        elif isinstance(right_val, str):
            try:
                right_val = float(right_val)
            except ValueError:
                raise TypeError(f"Type mismatch: Cannot compare numeric '{left_val}' with non-numeric string '{right_val}'")
        
        if isinstance(left_val, int):
            if int(right_val) == right_val:
                right_val = int(right_val)
        
        if self._op == "+":
            return left_val + right_val
        elif self._op == "-":
            return left_val - right_val
        elif self._op == "*":
            return left_val * right_val
        elif self._op == "/":
            if right_val == 0:
                raise ZeroDivisionError("Division by zero.")
            return left_val / right_val
        elif self._op == "and":
            return bool(left_val and right_val)
        elif self._op == "or":
            return bool(left_val or right_val)
        elif self._op == "==":
            return bool(left_val == right_val)
        elif self._op == "!=":
            return bool(left_val != right_val)
        elif self._op == ">":
            return left_val > right_val
        elif self._op == "<":
            return left_val < right_val
        elif self._op == ">=":
            return left_val >= right_val
        elif self._op == "<=":
            return left_val <= right_val
        
        raise RuntimeError(f"Unsupported operator '{self._op}' for number.")

    def evaluate(self, context: Dict[str, Any], dump_eval: Optional[List[str]] = None) -> Any:
        left_val = self._left.evaluate(context, dump_eval)
        right_val = self._right.evaluate(context, dump_eval)
        result: Any = None

        if isinstance(left_val, bool):
            result = self._eval_bool(left_val, right_val)
        elif isinstance(left_val, str):
            result = self._eval_str(left_val, right_val)
        elif isinstance(left_val, (int, float)):
            result = self._eval_num(left_val, right_val)
        else:
            raise RuntimeError(f"Unsupported types for operator '{self._op}' - '{left_val}', '{right_val}'.")
        
        if dump_eval is not None:
            dump_eval.append(f"Evaluated: {left_val} {self._op} {right_val} = {result}")
        return result

    def dump_structure(self, indent: int = 0) -> str:
        out = ("  " * indent + f"{self._name}") + "\n"
        out += self._left.dump_structure(indent + 1)
        out += self._right.dump_structure(indent + 1)
        return out
    
class OpAnd(BinaryOp):
    def __init__(self, left: Node, right: Node) -> None:
        super().__init__("And", left, "and", right)

class OpOr(BinaryOp):
    def __init__(self, left: Node, right: Node) -> None:
        super().__init__("Or", left, "or", right)

class OpEquals(BinaryOp):
    def __init__(self, left: Node, right: Node) -> None:
        super().__init__("Equals", left, "==", right)

class OpNotEquals(BinaryOp):
    def __init__(self, left: Node, right: Node) -> None:
        super().__init__("NotEquals", left, "!=", right)

class OpPlus(BinaryOp):
    def __init__(self, left: Node, right: Node) -> None:
        super().__init__("Plus", left, "+", right)

class OpMinus(BinaryOp):
    def __init__(self, left: Node, right: Node) -> None:
        super().__init__("Minus", left, "-", right)

class OpMultiply(BinaryOp):
    def __init__(self, left: Node, right: Node) -> None:
        super().__init__("Multiply", left, "*", right)

class OpDivide(BinaryOp):
    def __init__(self, left: Node, right: Node) -> None:
        super().__init__("Divide", left, "/", right)

class OpGreaterThan(BinaryOp):
    def __init__(self, left: Node, right: Node) -> None:
        super().__init__("GreaterThan", left, ">", right)

class OpLessThan(BinaryOp):
    def __init__(self, left: Node, right: Node) -> None:
        super().__init__("LessThan", left, "<", right)

class OpGreaterThanEquals(BinaryOp):
    def __init__(self, left: Node, right: Node) -> None:
        super().__init__("GreaterThanEquals", left, ">=", right)

class OpLessThanEquals(BinaryOp):
    def __init__(self, left: Node, right: Node) -> None:
        super().__init__("LessThanEquals", left, "<=", right)


class UnaryOp(Node):
    @abstractmethod
    def __init__(self, name:str, operand: Node) -> None:
        super().__init__(name)
        self._operand = operand

    def dump_structure(self, indent: int = 0) -> str:
        out = ("  " * indent + f"{self._name}") + "\n"
        out += self._operand.dump_structure(indent + 1)
        return out
    
    
class OpNegative(UnaryOp):
    def __init__(self, operand: Node) -> None:
        super().__init__("Negative", operand)

    def evaluate(self, context: Dict[str, Any], dump_eval: Optional[List[str]] = None) -> Any:
        val = self._operand.evaluate(context, dump_eval)
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            result = -val
        else:
            raise TypeError("Type mismatch: Can't call operator '-' on a non-numeric.")
        
        if dump_eval is not None:
            dump_eval.append(f"Evaluated: - {val} = {result}")
        
        return result


class OpNot(UnaryOp):
    def __init__(self, operand: Node) -> None:
        super().__init__("Not", operand)

    def evaluate(self, context: Dict[str, Any], dump_eval: Optional[List[str]] = None) -> Any:
        val = self._operand.evaluate(context, dump_eval)
        if isinstance(val, bool):
            result = not val
        else:
            raise TypeError("Type mismatch: Can't call operator 'not' on a non-bool.")
        
        if dump_eval is not None:
            dump_eval.append(f"Evaluated: not {val} = {result}")

        return result


class LiteralBoolean(Node):
    def __init__(self, value: bool) -> None:
        super().__init__("Boolean")
        self._value = value

    def evaluate(self, context: Dict[str, Any], dump_eval: Optional[List[str]] = None) -> bool:
        if dump_eval is not None:
            dump_eval.append(f"Boolean: {self._value}")
        return self._value

    def dump_structure(self, indent: int = 0) -> str:
        return ("  " * indent + f"Boolean({self._value})") + "\n"


class LiteralNumber(Node):
    def __init__(self, value: str) -> None:
        super().__init__("Number")
        self._value = float(value) if '.' in value else int(value)

    def evaluate(self, context: Dict[str, Any], dump_eval: Optional[List[str]] = None) -> Union[int, float]:
        if dump_eval is not None:
            dump_eval.append(f"Number: {self._value}")
        return self._value

    def dump_structure(self, indent: int = 0) -> str:
        return ("  " * indent + f"Number({self._value})") + "\n"


class LiteralString(Node):
    def __init__(self, value: str) -> None:
        super().__init__("String")
        self._value = value

    def evaluate(self, context: Dict[str, Any], dump_eval: Optional[List[str]] = None) -> str:
        if dump_eval is not None:
            dump_eval.append(f"String: {self._value}")
        return self._value

    def dump_structure(self, indent: int = 0) -> str:
        return ("  " * indent + f"String({self._value})") + "\n"


class Variable(Node):
    def __init__(self, name: str) -> None:
        super().__init__("Variable")
        self._name = name

    def evaluate(self, context: Dict[str, Any], dump_eval: Optional[List[str]] = None) -> Any:
        value = context.get(self._name)
        if value is None:
            raise RuntimeError(f"Variable '{self._name}' not found in context.")
        if not isinstance(value, (int, float, bool, str)):
            raise TypeError(f"Variable '{self._name}' must return bool, string, or numeric.")
        
        if dump_eval is not None:
            dump_eval.append(f"Fetching variable: {self._name} -> {value}")
        return value

    def dump_structure(self, indent: int = 0) -> str:
        return ("  " * indent + f"Variable({self._name})") + "\n"
    

class FunctionCall(Node):
    def __init__(self, func_name: str, args: Optional[List[Node]] = None) -> None:
        super().__init__("FunctionCall")
        if args is None:
            args = []
        self._func_name = func_name
        self._args = args

    def evaluate(self, context: Dict[str, Any], dump_eval: Optional[List[str]] = None) -> Any:
        func = context.get(self._func_name)
        if func is None:
            raise RuntimeError(f"Function '{self._func_name}' not found in context.")
        
        arg_values: List[Any] = [arg.evaluate(context, dump_eval) for arg in self._args]

        # Get the function signature and check if it accepts the provided arguments.
        sig = inspect.signature(func)
        try:
            sig.bind(*arg_values)
        except TypeError as e:
            raise RuntimeError(f"Function '{self._func_name}' does not support the provided arguments {arg_values}.")

        result = func(*arg_values)

        if not isinstance(result, (int, float, bool, str)):
            raise TypeError(f"Function '{self._func_name}' must return bool, string, or numeric.")
        
        if dump_eval is not None:
            dump_eval.append(f"Calling function: {self._func_name}({arg_values}) = {result}")

        return result

    def dump_structure(self, indent: int = 0) -> str:
        out = ("  " * indent + f"FunctionCall({self._func_name})") + "\n"
        for arg in self._args:
            out += arg.dump_structure(indent + 1)
        return out


TOKEN_REGEX = re.compile(r'''
    \s*(
        >=|<=|==|=|!=|>|<|\(|\)|,|and|&&|or|\|\||not|!  # Operators & keywords
        | \+|\-|\/|\*                                   # Maths operators
        | [A-Za-z_][A-Za-z0-9_]*                        # Identifiers (Variables & Functions)
        | -?\d+\.\d+(?![A-Za-z_])                       # Floating-point numbers (supports negative)
        | -?\d+(?![A-Za-z_])                            # Integers (supports negative)
        | "[^"]*"                                       # Strings in double quotes
        | '[^']*'                                       # Strings in single quotes
        | true|false|True|False                         # Booleans
    )\s*
''', re.VERBOSE)

class Parser:
    def __init__(self) -> None:
        self._tokens: List[str] = []
        self._pos: int = 0

    def parse(self, expression: str) -> Node:
        self._tokens = self.tokenize(expression)
        self._pos = 0
        node: Node = self._parse_or()

        if self._pos < len(self._tokens):
            raise SyntaxError(f"Unexpected token '{self._tokens[self._pos]}' at position {self._pos}")
    
        return node

    def tokenize(self, expression: str) -> List[str]:
        tokens: List[str] = []
        pos: int = 0

        while pos < len(expression):
            match = TOKEN_REGEX.match(expression, pos)
            if not match:
                raise SyntaxError(f"Unrecognized token at position {pos}: '{expression[pos:]}'")
            
            token: str = match.group(0).strip()
            if token:
                tokens.append(token)

            pos = match.end()

        return tokens

    def _parse_or(self) -> Node:
        node: Node = self._parse_and()
        while self._match("or") or self._match("||"):
            node = OpOr(node, self._parse_and())
        return node

    def _parse_and(self) -> Node:
        node: Node = self._parse_binary_op()
        while self._match("and") or self._match("&&"):
            node = OpAnd(node, self._parse_binary_op())
        return node

    def _parse_math_add_sub(self) -> Node:
        node: Node = self._parse_math_mul_div()
        while self._match("+", "-"):
            op: str = self._previous() or ""
            if op=="+":
                node = OpPlus(node, self._parse_math_mul_div())
            else:
                node = OpMinus(node, self._parse_math_mul_div())
        return node

    def _parse_math_mul_div(self) -> Node:
        node: Node = self._parse_unary_op()
        while self._match("*", "/"):
            op: str = self._previous() or ""
            if op=="*":
                node = OpMultiply(node, self._parse_unary_op())
            else:
                node = OpDivide(node, self._parse_unary_op())          
        return node

    def _parse_binary_op(self) -> Node:
        node: Node = self._parse_math_add_sub()
        while self._match("==", "!=", ">", "<", ">=", "<=", "="):
            op: str = self._previous() or ""
            if op == "=" or op == "==":
                node = OpEquals(node, self._parse_math_add_sub())
            elif op == "!=":
                node = OpNotEquals(node, self._parse_math_add_sub())
            elif op == ">":
                node = OpGreaterThan(node, self._parse_math_add_sub())
            elif op == "<":
                node = OpLessThan(node, self._parse_math_add_sub())
            elif op == ">=":
                node = OpGreaterThanEquals(node, self._parse_math_add_sub())
            elif op == "<=":
                node = OpLessThanEquals(node, self._parse_math_add_sub())          
        return node

    def _parse_unary_op(self) -> Node:
        if self._match("not") or self._match("!"):
            return OpNot(self._parse_unary_op())
        elif self._match("-"):
            return OpNegative(self._parse_unary_op())
        return self._parse_term()
    
    def _parse_string_literal(self) -> Optional[LiteralString]:
        string_val = self._peek()
        if string_val and ((string_val.startswith('"') and string_val.endswith('"')) or (string_val.startswith("'") and string_val.endswith("'"))):
            self._advance()
            return LiteralString(string_val[1:-1])
        return None
    
    def _parse_term(self) -> Node:
        if self._match("("):
            node: Node = self._parse_or()
            self._consume(")")
            return node
        elif self._match("true") or self._match("True"):
            return LiteralBoolean(True)
        elif self._match("false") or self._match("False"):
            return LiteralBoolean(False)
        elif re.match(r'^-?\d+(\.\d+)?$', self._peek() or ""):
            return LiteralNumber(self._advance() or "")
        
        string_val = self._parse_string_literal()
        if string_val is not None:
            return string_val
        
        identifier = self._match_identifier()
        if identifier:
            if self._match("("):
                args = []
                if not self._match(")"):
                    args.append(self._parse_or())
                    while self._match(","):
                        args.append(self._parse_or())
                    self._consume(")")
                return FunctionCall(identifier, args)
            return Variable(identifier)
        raise SyntaxError(f"Unexpected token: {self._peek()}")

    def _match(self, *expected_tokens: str) -> bool:
        if self._pos < len(self._tokens) and self._tokens[self._pos] in expected_tokens:
            self._pos += 1
            return True
        return False

    def _consume(self, expected_token: str) -> None:
        if self._match(expected_token):
            return
        raise SyntaxError(f"Expected '{expected_token}' but found '{self._peek()}'")

    def _peek(self) -> Optional[str]:
        return self._tokens[self._pos] if self._pos < len(self._tokens) else None

    def _previous(self) -> Optional[str]:
        return self._tokens[self._pos - 1] if self._pos > 0 else None

    def _advance(self) -> Optional[str]:
        if self._pos < len(self._tokens):
            self._pos += 1
            return self._tokens[self._pos - 1]
        return None

    def _expect(self, expected_token: str) -> str:
        token: Optional[str] = self._advance()
        if token != expected_token:
            raise SyntaxError(f"Expected '{expected_token}', but found '{token}'")
        return token

    def _match_identifier(self) -> Optional[str]:
        if self._pos < len(self._tokens) and re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', self._tokens[self._pos]):
            token: str = self._tokens[self._pos]
            self._pos += 1
            return token
        return None