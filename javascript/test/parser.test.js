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

 /* describe('Tags', () => {
    it('should match', () => {

      const source = loadTestFile('Tags.fountain');
      const match = loadTestFile('Tags.txt');

      let fp = new FountainParser();
      fp.useTags = true;
      fp.addText(source);

      let output = fp.script.dump();
      //console.log(output);
      assert.equal(output, match);
    });
  });*/

});