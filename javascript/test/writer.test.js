// This file is part of an MIT-licensed project: see LICENSE file or README.md for details.
// Copyright (c) 2024 Ian Thomas

import {loadTestFile} from '../test/testUtils.js';
import {strict as assert} from 'assert';
import {ExpressionParser} from "../src/parser.js";
import {STRING_FORMAT, Writer} from "../src/writer.js";

describe('Writer', () => {

  describe('Simple', () => {
    it('should match', () => {

      let parser = new ExpressionParser();
      let expression = parser.parse("get_name()=='fred' and counter>0 and 5/5.0!=0");
      
      let result = expression.write();
      assert.equal(result, "get_name() == 'fred' and counter > 0 and 5 / 5 != 0", "Expression doesn't match.");
      Writer.StringFormat = STRING_FORMAT.DOUBLEQUOTE;
      result = expression.write();
      assert.equal(result, "get_name() == \"fred\" and counter > 0 and 5 / 5 != 0", "Expression doesn't match.");
      Writer.StringFormat = STRING_FORMAT.ESCAPED_DOUBLEQUOTE;
      result = expression.write();
      assert.equal(result, "get_name() == \\\"fred\\\" and counter > 0 and 5 / 5 != 0", "Expression doesn't match.");
      Writer.StringFormat = STRING_FORMAT.ESCAPED_SINGLEQUOTE;
      result = expression.write();
      assert.equal(result, "get_name() == \\'fred\\' and counter > 0 and 5 / 5 != 0", "Expression doesn't match.");
      Writer.StringFormat = STRING_FORMAT.SINGLEQUOTE;
    });
  });

  describe('MatchingOutput', () => {
    it('should match', () => {

      const source = loadTestFile('Writer.txt');
      const lines = source.split(/\r?\n/);

      const parser = new ExpressionParser();
    
      let processed_lines = [];
      for (const line of lines) {

        if (line.startsWith("//")) {
          processed_lines.push(line);
          continue;
        }
    
        processed_lines.push(`"${line}"`);
        const node = parser.parse(line);
        processed_lines.push(node.write());
        processed_lines.push("");
      }
    
      const output = processed_lines.join("\n");

      const match = loadTestFile('Writer-Output.txt');
      assert.equal(match, output);
    });
  });

});