import re

DEBUG = True  # Set to False to disable debug prints


class Node:
    def evaluate(self, context):
        raise NotImplementedError()

    def debug_print(self, indent=0):
        print("  " * indent + str(self))


class BinaryOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self, context):
        left_val = self.left.evaluate(context)
        right_val = self.right.evaluate(context)
        result = None

        # Ensure right_val is converted to match left_val type, but never modify left_val
        if isinstance(left_val, bool):
            if isinstance(right_val, (int,float)):
                right_val = right_val!=0
            elif isinstance(right_val, str):
                right_val = right_val.lower()=="true" or right_val=="1"
            elif not isinstance(right_val, bool):
                raise TypeError(f"Type mismatch: Cannot compare bool '{left_val}' with non-bool '{right_val}'")
        elif isinstance(left_val, str):
            if isinstance(right_val, bool):
                right_val = "true" if right_val else "false"
            elif isinstance(right_val, (int, float)):
                right_val = str(right_val)  # Convert number to string
            elif not isinstance(right_val, str):
                raise TypeError(f"Type mismatch: Cannot compare string '{left_val}' with non-string '{right_val}'")
        elif isinstance(left_val, (int, float)):
            if isinstance(right_val, bool):
                right_val = 1 if right_val else 0
            elif isinstance(right_val, str):
                try:
                    right_val = float(right_val)
                except ValueError:
                    raise TypeError(f"Type mismatch: Cannot compare numeric '{left_val}' with non-numeric string '{right_val}'")
            if isinstance(left_val, int):
                if int(right_val)==right_val:
                    right_val = int(right_val)

        if isinstance(left_val, str):
            if self.op == "==":
                result = left_val == right_val
            elif self.op == "!=":
                result = left_val != right_val
            else:
                raise RuntimeError(f"Unsupported operator '{self.op}' for string.")
        elif isinstance(left_val, bool):
            if self.op == "and":
                result = left_val and right_val
            elif self.op == "or":
                result = left_val or right_val
            elif self.op == "==":
                result = left_val == right_val
            elif self.op == "!=":
                result = left_val != right_val
            else:
                raise RuntimeError(f"Unsupported operator '{self.op}' for bool.")
        else:
            if self.op == "+":
                result = left_val + right_val
            elif self.op == "-":
                result = left_val - right_val
            elif self.op == "*":
                result = left_val * right_val
            elif self.op == "/":
                if right_val == 0:
                    raise ZeroDivisionError("Division by zero.")
                result = left_val / right_val
            elif self.op == "and":
                result = left_val and right_val
            elif self.op == "or":
                result = left_val or right_val
            elif self.op == "==":
                result = left_val == right_val
            elif self.op == "!=":
                result = left_val != right_val
            elif self.op == ">":
                result = left_val > right_val
            elif self.op == "<":
                result = left_val < right_val
            elif self.op == ">=":
                result = left_val >= right_val
            elif self.op == "<=":
                result = left_val <= right_val
        
        if DEBUG:
            print(f"Evaluating: {left_val} {self.op} {right_val} -> {result}")
        return result

    def debug_print(self, indent=0):
        print("  " * indent + f"BinaryOp({self.op})")
        self.left.debug_print(indent + 1)
        self.right.debug_print(indent + 1)


class UnaryOp(Node):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def evaluate(self, context):
        val = self.operand.evaluate(context)
        result = not val if self.op == "not" else val
        if DEBUG:
            print(f"Evaluating: {self.op} {val} -> {result}")
        return result

    def debug_print(self, indent=0):
        print("  " * indent + f"UnaryOp({self.op})")
        self.operand.debug_print(indent + 1)


class BooleanLiteral(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        if DEBUG:
            print(f"Boolean literal: {self.value}")
        return self.value

    def debug_print(self, indent=0):
        print("  " * indent + f"BooleanLiteral({self.value})")


class NumericLiteral(Node):
    def __init__(self, value):
        self.value = float(value) if '.' in value else int(value)

    def evaluate(self, context):
        if DEBUG:
            print(f"Numeric literal: {self.value}")
        return self.value

    def debug_print(self, indent=0):
        print("  " * indent + f"NumericLiteral({self.value})")


class Variable(Node):
    def __init__(self, name):
        self.name = name

    def evaluate(self, context):
        value = context.get(self.name)
        if value is None:
            raise RuntimeError(f"Variable '{self.name}' not found in context.")
        
        if DEBUG:
            print(f"Fetching variable: {self.name} -> {value}")
        return value

    def debug_print(self, indent=0):
        print("  " * indent + f"Variable({self.name})")


class StringLiteral(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        if DEBUG:
            print(f"String literal: {self.value}")
        return self.value

    def debug_print(self, indent=0):
        print("  " * indent + f"StringLiteral({self.value})")


class FunctionCall(Node):
    def __init__(self, func_name, args=[]):
        self.func_name = func_name
        self.args = args

    def evaluate(self, context):
        func = context.get(self.func_name) #, lambda *args: False)
        if func is None:
            raise RuntimeError(f"Function '{self.func_name}' not found in context.")
        
        arg_values = [arg.evaluate(context) for arg in self.args]
        result = func(*arg_values)
        if DEBUG:
            print(f"Calling function: {self.func_name}({arg_values}) -> {result}")
        return result

    def debug_print(self, indent=0):
        print("  " * indent + f"FunctionCall({self.func_name})")
        for arg in self.args:
            arg.debug_print(indent + 1)


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
    def __init__(self):
        self.tokens = []
        self.pos = 0

    def parse(self, expression):
        self.tokens = self.tokenize(expression)
        self.pos = 0
        node = self.parse_or()

        if self.pos < len(self.tokens):
            raise SyntaxError(f"Unexpected token '{self.tokens[self.pos]}' at position {self.pos}")
    
        if DEBUG:
            print("Parsed Expression Tree:")
            node.debug_print()
        return node

    def tokenize(self, expression):
        tokens = []
        pos = 0

        while pos < len(expression):
            match = TOKEN_REGEX.match(expression, pos)
            if not match:
                raise SyntaxError(f"Unrecognized token at position {pos}: '{expression[pos:]}'")
            
            token = match.group(0).strip()
            if token:
                tokens.append(token)

            pos = match.end()

        if DEBUG:
            print(f"Tokens: {tokens}")

        return tokens

    def parse_or(self):
        node = self.parse_and()
        while self.match("or") or self.match("||"):
            node = BinaryOp(node, "or", self.parse_and())
        return node

    def parse_and(self):
        node = self.parse_unary_op()
        while self.match("and") or self.match("&&"):
            node = BinaryOp(node, "and", self.parse_unary_op())
        return node

    def parse_unary_op(self):
        if self.match("not") or self.match("!"):
            return UnaryOp("not", self.parse_unary_op())
        return self.parse_binary_op()

    def parse_math_add_sub(self):
        node = self.parse_math_mul_div()
        while self.match("+", "-"):
            op = self.previous()
            node = BinaryOp(node, op, self.parse_math_mul_div())
        return node

    def parse_math_mul_div(self):
        node = self.parse_term()
        while self.match("*", "/"):
            op = self.previous()
            node = BinaryOp(node, op, self.parse_term())
        return node

    def parse_binary_op(self):
        node = self.parse_math_add_sub()
        while self.match("==", "!=", ">", "<", ">=", "<=", "="):
            op = self.previous()
            if op == "=":
                op = "=="
            node = BinaryOp(node, op, self.parse_math_add_sub())
        return node

    def parse_term(self):
        if self.match("("):
            node = self.parse_or()
            self.consume(")")
            return node
        elif self.match("true") or self.match("True"):
            return BooleanLiteral(True)
        elif self.match("false") or self.match("False"):
            return BooleanLiteral(False)
        elif re.match(r'^-?\d+(\.\d+)?$', self.peek()):
            return NumericLiteral(self.advance())
        elif self.peek().startswith("\"") and self.peek().endswith("\""):
            return StringLiteral(self.advance()[1:-1])
        elif self.peek().startswith("\'") and self.peek().endswith("\'"):
            return StringLiteral(self.advance()[1:-1])
        elif self.match_identifier():
            name = self.previous()
            if self.match("("):
                args = []
                if not self.match(")"):
                    args.append(self.parse_or())
                    while self.match(","):
                        args.append(self.parse_or())
                    self.consume(")")
                return FunctionCall(name, args)
            return Variable(name)
        raise SyntaxError(f"Unexpected token: {self.peek()}")
    
    def match(self, *expected_tokens):
        if self.pos < len(self.tokens) and self.tokens[self.pos] in expected_tokens:
            self.pos += 1
            return True
        return False

    def consume(self, expected_token):
        if self.match(expected_token):
            return
        raise SyntaxError(f"Expected '{expected_token}' but found '{self.peek()}'")

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def previous(self):
        return self.tokens[self.pos - 1] if self.pos > 0 else None

    def advance(self):
        if self.pos < len(self.tokens):
            self.pos += 1
            return self.tokens[self.pos - 1]
        return None

    def expect(self, expected_token):
        token = self.advance()
        if token != expected_token:
            raise SyntaxError(f"Expected '{expected_token}', but found '{token}'")
        return token

    def match_identifier(self):
        if self.pos < len(self.tokens) and re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', self.tokens[self.pos]):
            self.pos += 1
            return True
        return False
