// This file is part of an MIT-licensed project: see LICENSE file or README.md for details.
// Copyright (c) 2025 Ian Thomas

import {
    ExpressionNode,
    LiteralBoolean,
    LiteralNumber,
    LiteralString,
    OpAnd,
    OpDivide,
    OpEquals,
    OpGreaterThan,
    OpGreaterThanEquals,
    OpLessThan,
    OpLessThanEquals,
    OpMinus,
    OpMultiply,
    OpNegative,
    OpNot,
    OpNotEquals,
    OpOr,
    OpPlus,
    Variable,
    FunctionCall,
  } from "./expression.js";
  
  // A JavaScript regular expression for tokenizing the expression.
  // The pattern below mirrors the Python TOKEN_REGEX from your parser.
  // Note: The "g" flag (global) is used for repeated matching.
  const TOKEN_REGEX = /\s*(>=|<=|==|=|!=|>|<|\(|\)|,|and|&&|or|\|\||not|!|\+|\-|\/|\*|[A-Za-z_][A-Za-z0-9_]*|-?\d+\.\d+|-?\d+|"[^"]*"|'[^']*'|true|false|True|False)\s*/g;
  
  export class ExpressionParser {
    constructor() {
      this._tokens = [];
      this._pos = 0;
    }
  
    /**
     * Parses the given expression string into an AST (ExpressionNode).
     * @param {string} expression 
     * @returns {ExpressionNode}
     */
    parse(expression) {
      this._tokens = this.tokenize(expression);
      this._pos = 0;
      const node = this._parse_or();
  
      if (this._pos < this._tokens.length) {
        throw new SyntaxError(
          `Unexpected token '${this._tokens[this._pos]}' at position ${this._pos}`
        );
      }
      return node;
    }
  
    /**
     * Tokenizes the input expression string.
     * @param {string} expression 
     * @returns {string[]}
     */
    tokenize(expression) {
        const matches = expression.matchAll(TOKEN_REGEX);
        const tokens = [];
        for (const match of matches) {
          // match[1] contains the captured token (without surrounding whitespace)
          if (match[1]) {
            tokens.push(match[1]);
          }
        }

        if (tokens.length === 0) {
          throw new SyntaxError(`No tokens were recognized in expression: '${expression}'`);
        }
        return tokens;
      }

    _parse_or() {
      let node = this._parse_and();
      while (this._match("or") || this._match("||")) {
        node = new OpOr(node, this._parse_and());
      }
      return node;
    }
  
    _parse_and() {
      let node = this._parse_binary_op();
      while (this._match("and") || this._match("&&")) {
        node = new OpAnd(node, this._parse_binary_op());
      }
      return node;
    }
  
    _parse_math_add_sub() {
      let node = this._parse_math_mul_div();
      while (this._match("+", "-")) {
        const op = this._previous() || "";
        if (op === "+") {
          node = new OpPlus(node, this._parse_math_mul_div());
        } else {
          node = new OpMinus(node, this._parse_math_mul_div());
        }
      }
      return node;
    }
  
    _parse_math_mul_div() {
      let node = this._parse_unary_op();
      while (this._match("*", "/")) {
        const op = this._previous() || "";
        if (op === "*") {
          node = new OpMultiply(node, this._parse_unary_op());
        } else {
          node = new OpDivide(node, this._parse_unary_op());
        }
      }
      return node;
    }
  
    _parse_binary_op() {
      let node = this._parse_math_add_sub();
      while (this._match("==", "!=", ">", "<", ">=", "<=", "=")) {
        const op = this._previous() || "";
        if (op === "=" || op === "==") {
          node = new OpEquals(node, this._parse_math_add_sub());
        } else if (op === "!=") {
          node = new OpNotEquals(node, this._parse_math_add_sub());
        } else if (op === ">") {
          node = new OpGreaterThan(node, this._parse_math_add_sub());
        } else if (op === "<") {
          node = new OpLessThan(node, this._parse_math_add_sub());
        } else if (op === ">=") {
          node = new OpGreaterThanEquals(node, this._parse_math_add_sub());
        } else if (op === "<=") {
          node = new OpLessThanEquals(node, this._parse_math_add_sub());
        }
      }
      return node;
    }
  
    _parse_unary_op() {
      if (this._match("not") || this._match("!")) {
        return new OpNot(this._parse_unary_op());
      } else if (this._match("-")) {
        return new OpNegative(this._parse_unary_op());
      }
      return this._parse_term();
    }
  
    _parse_string_literal() {
      const stringVal = this._peek();
      if (
        stringVal &&
        ((stringVal.startsWith('"') && stringVal.endsWith('"')) ||
          (stringVal.startsWith("'") && stringVal.endsWith("'")))
      ) {
        this._advance();
        return new LiteralString(stringVal.slice(1, -1));
      }
      return null;
    }
  
    _parse_term() {
      if (this._match("(")) {
        const node = this._parse_or();
        this._consume(")");
        return node;
      } else if (this._match("true") || this._match("True")) {
        return new LiteralBoolean(true);
      } else if (this._match("false") || this._match("False")) {
        return new LiteralBoolean(false);
      } else if (/^-?\d+(\.\d+)?$/.test(this._peek() || "")) {
        return new LiteralNumber(this._advance() || "");
      }
  
      const stringLiteral = this._parse_string_literal();
      if (stringLiteral !== null) {
        return stringLiteral;
      }
  
      const identifier = this._match_identifier();
      if (identifier) {
        if (this._match("(")) {
          const args = [];
          if (!this._match(")")) {
            args.push(this._parse_or());
            while (this._match(",")) {
              args.push(this._parse_or());
            }
            this._consume(")");
          }
          return new FunctionCall(identifier, args);
        }
        return new Variable(identifier);
      }
      throw new SyntaxError(`Unexpected token: ${this._peek()}`);
    }
  
    _match(...expectedTokens) {
      if (this._pos < this._tokens.length && expectedTokens.includes(this._tokens[this._pos])) {
        this._pos++;
        return true;
      }
      return false;
    }
  
    _consume(expectedToken) {
      if (this._match(expectedToken)) {
        return;
      }
      if (this._pos >= this._tokens.length) {
        throw new SyntaxError(`Expected '${expectedToken}' but expression ended.`);
      }
      throw new SyntaxError(`Expected '${expectedToken}' but found '${this._peek()}'`);
    }
  
    _peek() {
      return this._pos < this._tokens.length ? this._tokens[this._pos] : null;
    }
  
    _previous() {
      return this._pos > 0 ? this._tokens[this._pos - 1] : null;
    }
  
    _advance() {
      if (this._pos < this._tokens.length) {
        this._pos++;
        return this._tokens[this._pos - 1];
      }
      return null;
    }
  
    _expect(expectedToken) {
      const token = this._advance();
      if (token !== expectedToken) {
        throw new SyntaxError(`Expected '${expectedToken}', but found '${token}'`);
      }
      return token;
    }
  
    _match_identifier() {
      if (this._pos < this._tokens.length && /^[A-Za-z_][A-Za-z0-9_]*$/.test(this._tokens[this._pos])) {
        const token = this._tokens[this._pos];
        this._pos++;
        return token;
      }
      return null;
    }
  }