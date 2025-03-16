// This file is part of an MIT-licensed project: see LICENSE file or README.md for details.
// Copyright (c) 2025 Ian Thomas

#include "expression_parser/parser.h"
#include <catch_amalgamated.hpp>
#include "test_utils.h"

using namespace ExpressionParser;

TEST_CASE( "Simple") {

    Parser parser;

    auto expression = parser.Parse("get_name()=='fred' and counter>0 and 5/5.0!=0");

    Context context;
    context["get_name"] = make_function_wrapper([]() -> std::string {
        return "fred";
    });
    context["counter"] = 1;

    std::any result = expression->Evaluate(context);

    REQUIRE(std::any_cast<bool>(result) == true);
}
/*
TEST_CASE( "SceneHeading") {
    
    const std::string source = loadTestFile("Parse.txt");

    Fountain::Parser fp;

    fp.addText(source);

    const std::string output = fp.getScript()->dump();

    const std::string match = loadTestFile("Parse-Output.txt");
    REQUIRE(match == output);
}
*/