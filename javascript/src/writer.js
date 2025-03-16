// This file is part of an MIT-licensed project: see LICENSE file or README.md for details.
// Copyright (c) 2025 Ian Thomas

export const STRING_FORMAT = Object.freeze({
    SINGLEQUOTE: 0,
    ESCAPED_SINGLEQUOTE: 1,
    DOUBLEQUOTE: 2,
    ESCAPED_DOUBLEQUOTE: 3,
  });
  
let _stringFormat = STRING_FORMAT.SINGLEQUOTE;

export const Writer = {
    get StringFormat() {
        return _stringFormat;
    },
    set StringFormat(value) {
        _stringFormat = value;
    }
};