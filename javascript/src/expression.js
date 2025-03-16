/*
 * This file is part of an MIT-licensed project: see LICENSE file or README.md for details.
 * Copyright (c) 2025 Ian Thomas
 */

export const StringFormat = Object.freeze({
  SINGLEQUOTE: 0,
  ESCAPED_SINGLEQUOTE: 1,
  DOUBLEQUOTE: 2,
  ESCAPED_DOUBLEQUOTE: 3,
});

let _STRING_FORMAT = StringFormat.SINGLEQUOTE;

export function setStringFormat(newFormat) {
  _STRING_FORMAT = newFormat;
}

export class ExpressionNode {
  constructor(name, precedence) {
    if (new.target === ExpressionNode) {
      throw new TypeError("Cannot instantiate abstract class ExpressionNode directly");
    }
    this._name = name;
    this._precedence = precedence;
  }

  evaluate(context, dump_eval) {
    throw new Error("Abstract method 'evaluate' not implemented");
  }

  dump_structure(indent = 0) {
    throw new Error("Abstract method 'dump_structure' not implemented");
  }

  write() {
    throw new Error("Abstract method 'write' not implemented");
  }
}

export class BinaryOp extends ExpressionNode {
  constructor(name, left, op, right, precedence) {
    super(name, precedence);
    this._left = left;
    this._op = op;
    this._right = right;
  }

  evaluate(context, dump_eval) {
    const left_val = this._left.evaluate(context, dump_eval);
    const right_val = this._right.evaluate(context, dump_eval);
    const result = this._do_eval(left_val, right_val);

    if (dump_eval) {
      dump_eval.push(`Evaluated: ${_format_value(left_val)} ${this._op} ${_format_value(right_val)} = ${_format_value(result)}`);
    }
    return result;
  }

  _do_eval(left_val, right_val) {
    throw new Error("Abstract method '_do_eval' not implemented");
  }

  dump_structure(indent = 0) {
    let out = "  ".repeat(indent) + `${this._name}\n`;
    out += this._left.dump_structure(indent + 1);
    out += this._right.dump_structure(indent + 1);
    return out;
  }

  write() {
    let left_str = this._left.write();
    let right_str = this._right.write();

    if (this._left._precedence < this._precedence) {
      left_str = `(${left_str})`;
    }
    if (this._right._precedence < this._precedence) {
      right_str = `(${right_str})`;
    }
    return `${left_str} ${this._op} ${right_str}`;
  }
}

export class OpOr extends BinaryOp {
  constructor(left, right) {
    super("Or", left, "or", right, 40);
  }
  _do_eval(left_val, right_val) {
    return _make_bool(left_val) || _make_bool(right_val);
  }
}

export class OpAnd extends BinaryOp {
  constructor(left, right) {
    super("And", left, "and", right, 50);
  }
  _do_eval(left_val, right_val) {
    return _make_bool(left_val) && _make_bool(right_val);
  }
}

export class OpEquals extends BinaryOp {
  constructor(left, right) {
    super("Equals", left, "==", right, 60);
  }
  _do_eval(left_val, right_val) {
    right_val = _make_type_match(left_val, right_val);
    return left_val === right_val;
  }
}

export class OpNotEquals extends BinaryOp {
  constructor(left, right) {
    super("NotEquals", left, "!=", right, 60);
  }
  _do_eval(left_val, right_val) {
    right_val = _make_type_match(left_val, right_val);
    return left_val !== right_val;
  }
}

export class OpPlus extends BinaryOp {
  constructor(left, right) {
    super("Plus", left, "+", right, 70);
  }
  _do_eval(left_val, right_val) {
    return _make_numeric(left_val) + _make_numeric(right_val);
  }
}

export class OpMinus extends BinaryOp {
  constructor(left, right) {
    super("Minus", left, "-", right, 70);
  }
  _do_eval(left_val, right_val) {
    return _make_numeric(left_val) - _make_numeric(right_val);
  }
}

export class OpDivide extends BinaryOp {
  constructor(left, right) {
    super("Divide", left, "/", right, 85);
  }
  _do_eval(left_val, right_val) {
    right_val = _make_numeric(right_val);
    if (right_val === 0) {
      throw new Error("Division by zero.");
    }
    return _make_numeric(left_val) / right_val;
  }
}

export class OpMultiply extends BinaryOp {
  constructor(left, right) {
    super("Multiply", left, "*", right, 80);
  }
  _do_eval(left_val, right_val) {
    return _make_numeric(left_val) * _make_numeric(right_val);
  }
}

export class OpGreaterThan extends BinaryOp {
  constructor(left, right) {
    super("GreaterThan", left, ">", right, 60);
  }
  _do_eval(left_val, right_val) {
    return _make_numeric(left_val) > _make_numeric(right_val);
  }
}

export class OpLessThan extends BinaryOp {
  constructor(left, right) {
    super("LessThan", left, "<", right, 60);
  }
  _do_eval(left_val, right_val) {
    return _make_numeric(left_val) < _make_numeric(right_val);
  }
}

export class OpGreaterThanEquals extends BinaryOp {
  constructor(left, right) {
    super("GreaterThanEquals", left, ">=", right, 60);
  }
  _do_eval(left_val, right_val) {
    return _make_numeric(left_val) >= _make_numeric(right_val);
  }
}

export class OpLessThanEquals extends BinaryOp {
  constructor(left, right) {
    super("LessThanEquals", left, "<=", right, 60);
  }
  _do_eval(left_val, right_val) {
    return _make_numeric(left_val) <= _make_numeric(right_val);
  }
}

export class UnaryOp extends ExpressionNode {
  constructor(name, op, operand, precedence) {
    super(name, precedence);
    this._operand = operand;
    this._op = op;
  }

  evaluate(context, dump_eval) {
    const val = this._operand.evaluate(context, dump_eval);
    const result = this._do_eval(val);
    if (dump_eval) {
      dump_eval.push(`Evaluated: ${this._op} ${_format_value(val)} = ${_format_value(result)}`);
    }
    return result;
  }

  _do_eval(val) {
    throw new Error("Abstract method '_do_eval' not implemented");
  }

  dump_structure(indent = 0) {
    let out = "  ".repeat(indent) + `${this._name}\n`;
    out += this._operand.dump_structure(indent + 1);
    return out;
  }

  write() {
    let operand_str = this._operand.write();
    if (this._operand._precedence < this._precedence) {
      operand_str = `(${operand_str})`;
    }
    return `${this._op} ${operand_str}`;
  }
}

export class OpNegative extends UnaryOp {
  constructor(operand) {
    super("Negative", "-", operand, 90);
  }
  _do_eval(val) {
    return -_make_numeric(val);
  }
}

export class OpNot extends UnaryOp {
  constructor(operand) {
    super("Not", "not", operand, 90);
  }
  _do_eval(val) {
    return !_make_bool(val);
  }
}

export class LiteralBoolean extends ExpressionNode {
  constructor(value) {
    super("Boolean", 100);
    this._value = value;
  }
  evaluate(context, dump_eval) {
    if (dump_eval) {
      dump_eval.push(`Boolean: ${_format_value(this._value)}`);
    }
    return this._value;
  }
  dump_structure(indent = 0) {
    return "  ".repeat(indent) + `Boolean(${_format_value(this._value)})\n`;
  }
  write() {
    return _format_value(this._value);
  }
}

export class LiteralNumber extends ExpressionNode {
  constructor(value) {
    super("Number", 100);
    // Assuming value is provided as a string
    this._value = parseFloat(value);
  }
  evaluate(context, dump_eval) {
    if (dump_eval) {
      dump_eval.push(`Number: ${this._value}`);
    }
    return this._value;
  }
  dump_structure(indent = 0) {
    return "  ".repeat(indent) + `Number(${this._value})\n`;
  }
  write() {
    return `${this._value}`;
  }
}

export class LiteralString extends ExpressionNode {
  constructor(value) {
    super("String", 100);
    this._value = value;
  }
  evaluate(context, dump_eval) {
    if (dump_eval) {
      dump_eval.push(`String: ${_format_string(this._value)}`);
    }
    return this._value;
  }
  dump_structure(indent = 0) {
    return "  ".repeat(indent) + `String(${_format_string(this._value)})\n`;
  }
  write() {
    return _format_string(this._value);
  }
}

export class Variable extends ExpressionNode {
  constructor(name) {
    super("Variable", 100);
    this._name = name;
  }
  evaluate(context, dump_eval) {
    const value = context[this._name];
    if (value === undefined) {
      throw new Error(`Variable '${this._name}' not found in context.`);
    }
    if (typeof value !== "number" && typeof value !== "boolean" && typeof value !== "string") {
      throw new TypeError(`Variable '${this._name}' must return bool, string, or numeric.`);
    }
    if (dump_eval) {
      dump_eval.push(`Fetching variable: ${this._name} -> ${_format_value(value)}`);
    }
    return value;
  }
  dump_structure(indent = 0) {
    return "  ".repeat(indent) + `Variable(${this._name})\n`;
  }
  write() {
    return this._name;
  }
}

export class FunctionCall extends ExpressionNode {
  constructor(func_name, args = []) {
    super("FunctionCall", 100);
    this._func_name = func_name;
    this._args = args;
  }
  evaluate(context, dump_eval) {
    const func = context[this._func_name];
    if (func === undefined) {
      throw new Error(`Function '${this._func_name}' not found in context.`);
    }
    const arg_values = this._args.map(arg => arg.evaluate(context, dump_eval));

    // Check function arity using func.length
    if (arg_values.length !== func.length) {
      const formattedArgs = arg_values.map(val => _format_value(val)).join(", ");
      throw new Error(`Function '${this._func_name}' does not support the provided arguments (${formattedArgs}).`);
    }

    const result = func(...arg_values);

    if (typeof result !== "number" && typeof result !== "boolean" && typeof result !== "string") {
      throw new TypeError(`Function '${this._func_name}' must return bool, string, or numeric.`);
    }
    if (dump_eval) {
      const formattedArgs = arg_values.map(val => _format_value(val)).join(", ");
      dump_eval.push(`Called function: ${this._func_name}(${formattedArgs}) = ${_format_value(result)}`);
    }
    return result;
  }
  dump_structure(indent = 0) {
    let out = "  ".repeat(indent) + `FunctionCall(${this._func_name})\n`;
    for (const arg of this._args) {
      out += arg.dump_structure(indent + 1);
    }
    return out;
  }
  write() {
    const written_args = this._args.map(arg => arg.write());
    return `${this._func_name}(${written_args.join(", ")})`;
  }
}

function _make_bool(val) {
  if (typeof val === "boolean") {
    return val;
  }
  if (typeof val === "number") {
    return val !== 0;
  }
  if (typeof val === "string") {
    return val.toLowerCase() === "true" || val === "1";
  }
  throw new TypeError(`Type mismatch: Expecting bool, but got '${val}'`);
}

function _make_str(val) {
  if (typeof val === "string") {
    return val;
  }
  if (typeof val === "boolean") {
    return val ? "true" : "false";
  }
  if (typeof val === "number") {
    return val.toString();
  }
  throw new TypeError(`Type mismatch: Expecting string but got '${val}'`);
}

function _make_numeric(val) {
  if (typeof val === "boolean") {
    return val ? 1 : 0;
  }
  if (typeof val === "number") {
    return val;
  }
  if (typeof val === "string") {
    const numericRegex = /^-?\d+(\.\d+)?$/;
    if (numericRegex.test(val)) {
      return parseFloat(val);
    }
  }
  throw new TypeError(`Type mismatch: Expecting number but got '${val}'`);
}

function _make_type_match(left_val, right_val) {
  if (typeof left_val === "boolean") {
    return _make_bool(right_val);
  }
  if (typeof left_val === "number") {
    return _make_numeric(right_val);
  }
  if (typeof left_val === "string") {
    return _make_str(right_val);
  }
  throw new TypeError(`Type mismatch: unrecognised type for '${left_val}'`);
}

function _format_string(val) {
  switch (_STRING_FORMAT) {
    case StringFormat.SINGLEQUOTE:
      return `'${val}'`;
    case StringFormat.ESCAPED_SINGLEQUOTE:
      return `\\'${val}\\'`;
    case StringFormat.ESCAPED_DOUBLEQUOTE:
      return `\\"${val}\\"`;
    case StringFormat.DOUBLEQUOTE:
    default:
      return `"${val}"`;
  }
}

function _format_value(val) {
  if (typeof val === "string") {
    return _format_string(val);
  }
  return val.toString();
}