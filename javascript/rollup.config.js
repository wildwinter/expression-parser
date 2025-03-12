import terser from '@rollup/plugin-terser';

console.log(terser);

export default {
  input: "src/expressionParser.js", // Aggregation file as the entry point
  output: [
    {
      file: "dist/expressionParser.js",
      format: "esm", // ES Module format
      sourcemap: true,
    },
    {
      file: "dist/expressionParser.min.js",
      format: "iife", 
      name: "ExpressionParser", 
      plugins: [terser()],
      sourcemap: true,
    },
  ],
};