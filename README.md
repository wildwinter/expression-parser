# expression-parser
**expression-parser** is a set of libraries to parse and execute simple comparison expressions from text, including variable references and function calls.

It is used to have a simple expression language for conditionals that is identical across different plaforms, so that data that includes conditionals can be agnostic. These libraries are written in **C++**, **Javascript**, **Python**, and **C#**.

```
(location=="spain" and is_day_time) or spell_power("jamie")>12
```

### Contents
* [The Basics](#the-basics)
* [Source Code](#source-code)
* [Releases](#releases)
* [Usage](#usage)
    * [Overview](#overview)
    * [Javascript as an ES6 module](#javascript-as-an-es6-module)
    * [Javascript in a browser](#javascript-in-a-browser)
    * [Python](#python)
    * [C#](#c)
    * [C++](#c-1)
* [API](#api)
* [Contributors](#contributors)
* [License](#license)

## The Basics
TO DO

## Source Code
The source can be found on [Github](https://github.com/wildwinter/expresison-parser), and is available under the MIT license.

## Releases
Releases are available in the releases area in [Github](https://github.com/wildwinter/expression-parser/releases) and are available for multiple platforms:
* Javascript - a JS file for use in ESM modules, and a minified JS file for use in a browser.
* Python - a Python package for import into other Python files.
* C# - a DotNET DLL for use in any C# project
* C++ - a set of source files for you to compile yourself

## Usage

### Overview
TBD

### Javascript as an ES6 module
```javascript
TBD
```

### Javascript in a browser
Either you can use the same module / ESM format (`expressionParser.js`):
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fountain Tools</title>
</head>
<body>
    <script type="module">
        import { ExpressionParser } from './expressionParser.js';

        const parser = new ExpressionParser();
        TBD
    </script>
</body>
</html>
```
Or you can use a minified IIFE version (`expressionParser.min.js`):
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Expression Parser</title>
    <script src="expressionParser.min.js"></script>
</head>
<body>
    <script>
        // Access the global ExpressionParser object
        const parser = new ExpressionParser.Parser();
        TBD
    </script>
</body>
</html>
```

### Python
```Python
from expression_parser.parser import Parser

TBD
```

### C#
Install the DLL in your project, and use it like so:
```CSharp
using System; 
using ExpressionParser;

class Program
{
    static void Main(string[] args)
    {
        Parser parser = new Parser();
        TBD
    }
}
```

### C++
I haven't supplied any built libs (because building multiplatform libs is outside my scope right now). Instead I have supplied source code in the zip - you should be able to build and use it with your project.

```cpp
#include "expression_parser/parser.h"
#include <iostream>
#include <string>

int main() {
    // Create an instance of ExpressionParser::Parser
    ExpressionParser::Parser parser;

   TBD

    return 0;
}
```

## API
### Parser
TBD

## Contributors
* [wildwinter](https://github.com/wildwinter) - original author

## License
```
MIT License

Copyright (c) 2024 Ian Thomas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```