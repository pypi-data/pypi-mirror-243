/* A Bison parser, made by GNU Bison 2.3.  */

/* Skeleton interface for Bison's Yacc-like parsers in C

   Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor,
   Boston, MA 02110-1301, USA.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     NUMBER = 258,
     SIDED_DIE = 259,
     FATE_DIE = 260,
     REPEAT = 261,
     SIDED_DIE_ZERO = 262,
     EXPLOSION = 263,
     IMPLOSION = 264,
     PENETRATE = 265,
     ONCE = 266,
     MACRO_ACCESSOR = 267,
     MACRO_STORAGE = 268,
     SYMBOL_SEPERATOR = 269,
     ASSIGNMENT = 270,
     KEEP_LOWEST = 271,
     KEEP_HIGHEST = 272,
     DROP_LOWEST = 273,
     DROP_HIGHEST = 274,
     FILTER = 275,
     LBRACE = 276,
     RBRACE = 277,
     PLUS = 278,
     MINUS = 279,
     MULT = 280,
     MODULO = 281,
     DIVIDE_ROUND_UP = 282,
     DIVIDE_ROUND_DOWN = 283,
     REROLL = 284,
     SYMBOL_LBRACE = 285,
     SYMBOL_RBRACE = 286,
     STATEMENT_SEPERATOR = 287,
     CAPITAL_STRING = 288,
     DO_COUNT = 289,
     UNIQUE = 290,
     IS_EVEN = 291,
     IS_ODD = 292,
     RANGE = 293,
     FN_MAX = 294,
     FN_MIN = 295,
     FN_ABS = 296,
     FN_POOL = 297,
     UMINUS = 298,
     GE = 299,
     LE = 300,
     LT = 301,
     GT = 302,
     EQ = 303,
     NE = 304
   };
#endif
/* Tokens.  */
#define NUMBER 258
#define SIDED_DIE 259
#define FATE_DIE 260
#define REPEAT 261
#define SIDED_DIE_ZERO 262
#define EXPLOSION 263
#define IMPLOSION 264
#define PENETRATE 265
#define ONCE 266
#define MACRO_ACCESSOR 267
#define MACRO_STORAGE 268
#define SYMBOL_SEPERATOR 269
#define ASSIGNMENT 270
#define KEEP_LOWEST 271
#define KEEP_HIGHEST 272
#define DROP_LOWEST 273
#define DROP_HIGHEST 274
#define FILTER 275
#define LBRACE 276
#define RBRACE 277
#define PLUS 278
#define MINUS 279
#define MULT 280
#define MODULO 281
#define DIVIDE_ROUND_UP 282
#define DIVIDE_ROUND_DOWN 283
#define REROLL 284
#define SYMBOL_LBRACE 285
#define SYMBOL_RBRACE 286
#define STATEMENT_SEPERATOR 287
#define CAPITAL_STRING 288
#define DO_COUNT 289
#define UNIQUE 290
#define IS_EVEN 291
#define IS_ODD 292
#define RANGE 293
#define FN_MAX 294
#define FN_MIN 295
#define FN_ABS 296
#define FN_POOL 297
#define UMINUS 298
#define GE 299
#define LE 300
#define LT 301
#define GT 302
#define EQ 303
#define NE 304




#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
#line 97 "src/grammar/dice.yacc"
{
    vec values;
}
/* Line 1529 of yacc.c.  */
#line 151 "y.tab.h"
	YYSTYPE;
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
# define YYSTYPE_IS_TRIVIAL 1
#endif

extern YYSTYPE yylval;

