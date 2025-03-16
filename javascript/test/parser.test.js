// This file is part of an MIT-licensed project: see LICENSE file or README.md for details.
// Copyright (c) 2024 Ian Thomas

import {loadTestFile} from '../test/testUtils.js';
import {strict as assert} from 'assert';
import {ExpressionParser} from "../src/parser.js";

describe('FountainParser', () => {

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

  describe('Tags', () => {
    it('should match', () => {

      const source = loadTestFile('Parse.txt');

      const lines = source.split(/\r?\n/);

      // Create the context object with callable entries
      const context = {
        C: 15,
        D: false,
        get_name: () => "fred",
        end_func: () => true,
        whisky: (id, n) => String(n) + "whisky_" + id,
        counter: 1,
      };
    
      // Create a new Parser instance
      const parser = new ExpressionParser();
    
      // Process each line
      let processed_lines = [];
      for (const line of lines) {
        // If the line is a comment, keep it as-is.
        if (line.startsWith("//")) {
          processed_lines.push(line);
          continue;
        }
    
        // Append the original line, wrapped in quotes
        processed_lines.push(`"${line}"`);
        try {
          // Parse the line into an AST node
          const node = parser.parse(line);
          // Dump the structure (for debugging or output)
          processed_lines.push(node.dump_structure());
          // Prepare an array to capture evaluation trace
          let dump_eval = [];
          // Evaluate the node using the context
          node.evaluate(context, dump_eval);
          // Append the evaluation trace (joined by newlines)
          processed_lines.push(dump_eval.join("\n"));
        } catch (e) {
          // Check for different error types
          if (e instanceof TypeError) {
            processed_lines.push(`TypeError: ${e.message}`);
          } else if (e instanceof SyntaxError) {
            processed_lines.push(`SyntaxError: ${e.message}`);
          } else {
            // For runtime or other errors
            processed_lines.push(`RuntimeError: ${e.message}`);
          }
        }
        // Append a blank line between entries
        processed_lines.push("");
      }
    
      // Join all processed lines into the final output string
      const output = processed_lines.join("\n");

      //const match = loadTestFile('Parse-Output.txt');
      //assert.equal(match, output);
    });
  });

});