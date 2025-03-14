import re
from typing import Any, Dict, List, Optional, Union

class Node:
    def evaluate(self, context: Dict[str, Any], dump_eval: Optional[List[str]] = None) -> Any:
        raise NotImplementedError()

    def dump_structure(self, indent: int = 0) -> str:
        return ("  " * indent + str(self)) + "\n"


class BinaryOp(Node):
    def __init__(self, left: Node, op: str, right: Node) -> None:
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
            raise RuntimeError(f"Unsupported types for operator '{self._op}'.")
        
        if dump_eval is not None:
            dump_eval.append(f"Evaluated: {left_val} {self._op} {right_val} = {result}")
        return result

    def dump_structure(self, indent: int = 0) -> str:
        out = ("  " * indent + f"BinaryOp({self._op})") + "\n"
        out += self._left.dump_structure(indent + 1)
        out += self._right.dump_structure(indent + 1)
        return out


class UnaryOp(Node):
    def __init__(self, op: str, operand: Node) -> None:
        self._op = op
        self._operand = operand

    def evaluate(self, context: Dict[str, Any], dump_eval: Optional[List[str]] = None) -> Any:
        val = self._operand.evaluate(context, dump_eval)
        if self._op == "not":
            if isinstance(val, bool):
                result = not val
            else:
                raise TypeError("Type mismatch: Can't call operator 'not' on a non-bool.")
        elif self._op == "-":
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                result = -val
            else:
                raise TypeError("Type mismatch: Can't call operator '-' on a non-numeric.")
        else:
            raise RuntimeError(f"Unsupported unary operator '{self._op}'")
        if dump_eval is not None:
            dump_eval.append(f"Evaluated: {self._op} {val} = {result}")
        return result

    def dump_structure(self, indent: int = 0) -> str:
        out = ("  " * indent + f"UnaryOp({self._op})") + "\n"
        out += self._operand.dump_structure(indent + 1)
        return out


class BooleanLiteral(Node):
    def __init__(self, value: bool) -> None:
        self._value = value

    def evaluate(self, context: Dict[str, Any], dump_eval: Optional[List[str]] = None) -> bool:
        if dump_eval is not None:
            dump_eval.append(f"Boolean literal: {self._value}")
        return self._value

    def dump_structure(self, indent: int = 0) -> str:
        return ("  " * indent + f"BooleanLiteral({self._value})") + "\n"


class NumericLiteral(Node):
    def __init__(self, value: str) -> None:
        self._value = float(value) if '.' in value else int(value)

    def evaluate(self, context: Dict[str, Any], dump_eval: Optional[List[str]] = None) -> Union[int, float]:
        if dump_eval is not None:
            dump_eval.append(f"Numeric literal: {self._value}")
        return self._value

    def dump_structure(self, indent: int = 0) -> str:
        return ("  " * indent + f"NumericLiteral({self._value})") + "\n"


class Variable(Node):
    def __init__(self, name: str) -> None:
        self._name = name

    def evaluate(self, context: Dict[str, Any], dump_eval: Optional[List[str]] = None) -> Any:
        value = context.get(self._name)
        if value is None:
            raise RuntimeError(f"Variable '{self._name}' not found in context.")
        
        if dump_eval is not None:
            dump_eval.append(f"Fetching variable: {self._name} -> {value}")
        return value

    def dump_structure(self, indent: int = 0) -> str:
        return ("  " * indent + f"Variable({self._name})") + "\n"


class StringLiteral(Node):
    def __init__(self, value: str) -> None:
        self._value = value

    def evaluate(self, context: Dict[str, Any], dump_eval: Optional[List[str]] = None) -> str:
        if dump_eval is not None:
            dump_eval.append(f"String literal: {self._value}")
        return self._value

    def dump_structure(self, indent: int = 0) -> str:
        return ("  " * indent + f"StringLiteral({self._value})") + "\n"


class FunctionCall(Node):
    def __init__(self, func_name: str, args: Optional[List[Node]] = None) -> None:
        if args is None:
            args = []
        self._func_name = func_name
        self._args = args

    def evaluate(self, context: Dict[str, Any], dump_eval: Optional[List[str]] = None) -> Any:
        func = context.get(self._func_name)
        if func is None:
            raise RuntimeError(f"Function '{self._func_name}' not found in context.")
        
        arg_values: List[Any] = [arg.evaluate(context, dump_eval) for arg in self._args]
        result = func(*arg_values)
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
        | true|false|True|False                         # Boolean literals
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
            node = BinaryOp(node, "or", self._parse_and())
        return node

    def _parse_and(self) -> Node:
        node: Node = self._parse_binary_op()
        while self._match("and") or self._match("&&"):
            node = BinaryOp(node, "and", self._parse_binary_op())
        return node

    def _parse_math_add_sub(self) -> Node:
        node: Node = self._parse_math_mul_div()
        while self._match("+", "-"):
            op: str = self._previous() or ""
            node = BinaryOp(node, op, self._parse_math_mul_div())
        return node

    def _parse_math_mul_div(self) -> Node:
        node: Node = self._parse_unary_op()
        while self._match("*", "/"):
            op: str = self._previous() or ""
            node = BinaryOp(node, op, self._parse_unary_op())
        return node

    def _parse_binary_op(self) -> Node:
        node: Node = self._parse_math_add_sub()
        while self._match("==", "!=", ">", "<", ">=", "<=", "="):
            op: str = self._previous() or ""
            if op == "=":
                op = "=="
            node = BinaryOp(node, op, self._parse_math_add_sub())
        return node

    def _parse_unary_op(self) -> Node:
        if self._match("not") or self._match("!"):
            return UnaryOp("not", self._parse_unary_op())
        elif self._match("-"):
            return UnaryOp("-", self._parse_unary_op())
        return self._parse_term()
    
    def _parse_term(self) -> Node:
        if self._match("("):
            node: Node = self._parse_or()
            self._consume(")")
            return node
        elif self._match("true") or self._match("True"):
            return BooleanLiteral(True)
        elif self._match("false") or self._match("False"):
            return BooleanLiteral(False)
        elif re.match(r'^-?\d+(\.\d+)?$', self._peek() or ""):
            return NumericLiteral(self._advance() or "")
        elif self._peek() and self._peek().startswith("\"") and self._peek().endswith("\""):
            token = self._advance() or ""
            return StringLiteral(token[1:-1])
        elif self._peek() and self._peek().startswith("'") and self._peek().endswith("'"):
            token = self._advance() or ""
            return StringLiteral(token[1:-1])
        identifier: Optional[str] = self._match_identifier()
        if identifier:
            if self._match("("):
                args: List[Node] = []
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