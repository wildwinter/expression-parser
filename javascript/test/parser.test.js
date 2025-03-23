// This file is part of an MIT-licensed project: see LICENSE file or README.md for details.
// Copyright (c) 2025 Ian Thomas

import {loadTestFile} from '../test/testUtils.js';
import {strict as assert} from 'assert';
import {ExpressionParser} from "../src/parser.js";

describe('ExpressionParser', () => {

  describe('Simple', () => {
    it('should match', () => {

      let parser = new ExpressionParser();
      let expression = parser.parse("get_name()=='fred' and counter>0 and 5/5.0!=0");

      let context = {
        "get_name": () => "fred",
        "counter": 1
      };

      let result = expression.evaluate(context);

      assert.equal(result, true);
    });
  });

  describe('Specificity', () => {
    it('should match', () => {

      let parser = new ExpressionParser();
      let expression = parser.parse("get_name()=='fred' and counter>0 and 5/5.0!=0");
      assert.equal(expression.specificity, 2);
      expression = parser.parse("get_name()=='fred' and counter>0 and (5/5.0!=0 or true)");
      assert.equal(expression.specificity, 3);
      expression = parser.parse("true");
      assert.equal(expression.specificity, 0);
    });
  });

  describe('MatchingOutput', () => {
    it('should match', () => {

      const source = loadTestFile('Parse.txt');

      const lines = source.split(/\r?\n/);

      const context = {
        C: 15,
        D: false,
        get_name: () => "fred",
        end_func: () => true,
        whisky: (id, n) => String(n) + "whisky_" + id,
        counter: 1,
      };
    
      const parser = new ExpressionParser();
    
      let processed_lines = [];
      for (const line of lines) {

        if (line.startsWith("//")) {
          processed_lines.push(line);
          continue;
        }
    
        processed_lines.push(`"${line}"`);
        try {

          const node = parser.parse(line);
          processed_lines.push(node.dump_structure());

          let dump_eval = [];
          node.evaluate(context, dump_eval);
          processed_lines.push(dump_eval.join("\n"));

        } catch (e) {
          processed_lines.push(`${e.message}`);
        }
        processed_lines.push("");
      }
    
      const output = processed_lines.join("\n");

      const match = loadTestFile('Parse-Output.txt');
      assert.equal(match, output);
    });
  });

});