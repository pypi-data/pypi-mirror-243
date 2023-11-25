/* A Bison parser, made by GNU Bison 2.3.  */

/* Skeleton implementation for Bison's Yacc-like parsers in C

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

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output.  */
#define YYBISON 1

/* Bison version.  */
#define YYBISON_VERSION "2.3"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Using locations.  */
#define YYLSP_NEEDED 0



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




/* Copy the first part of user declarations.  */
#line 4 "src/grammar/dice.yacc"


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <limits.h>
#include <assert.h>
#include <errno.h>
#include "shared_header.h"
#include "external/pcg_basic.h"
#include "external/tinydir.h"
#include "operations/macros.h"
#include "operations/conditionals.h"
#include "rolls/dice_core.h"
#include "rolls/dice_frontend.h"
#include "util/mocking.h"
#include "util/safe_functions.h"
#include "util/array_functions.h"
#include "util/vector_functions.h"
#include "util/string_functions.h"

#define UNUSED(x) (void)(x)
// Avoid conflicts with MacOs predefined macros
#define MAXV(x, y) (((x) > (y)) ? (x) : (y))
#define MINV(x, y) (((x) < (y)) ? (x) : (y))
#define ABSV(x) (((x) < 0) ? (-x) : (x))

int yylex(void);
int yyerror(const char* s);
int yywrap();

//TODO: move to external file 

#ifdef JUST_YACC
int yydebug=1;
#endif

int verbose = 0;
int dice_breakdown = 0;
int seeded = 0;
int write_to_file = 0;
char * output_file;

extern int gnoll_errno;
extern struct macro_struct *macros;
pcg32_random_t rng;

// Function Signatures for this file
int initialize();

// Functions
int initialize(){
    if (!seeded){
        unsigned long int tick = (unsigned long)time(0)+(unsigned long)clock();
        pcg32_srandom_r(
            &rng,
            tick ^ (unsigned long int)&printf,
            54u
        );
        seeded = 1;
    }
    return 0;
}



/* Enabling traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif

/* Enabling verbose error messages.  */
#ifdef YYERROR_VERBOSE
# undef YYERROR_VERBOSE
# define YYERROR_VERBOSE 1
#else
# define YYERROR_VERBOSE 0
#endif

/* Enabling the token table.  */
#ifndef YYTOKEN_TABLE
# define YYTOKEN_TABLE 0
#endif

#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
#line 97 "src/grammar/dice.yacc"
{
    vec values;
}
/* Line 193 of yacc.c.  */
#line 265 "y.tab.c"
	YYSTYPE;
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
# define YYSTYPE_IS_TRIVIAL 1
#endif



/* Copy the second part of user declarations.  */


/* Line 216 of yacc.c.  */
#line 278 "y.tab.c"

#ifdef short
# undef short
#endif

#ifdef YYTYPE_UINT8
typedef YYTYPE_UINT8 yytype_uint8;
#else
typedef unsigned char yytype_uint8;
#endif

#ifdef YYTYPE_INT8
typedef YYTYPE_INT8 yytype_int8;
#elif (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
typedef signed char yytype_int8;
#else
typedef short int yytype_int8;
#endif

#ifdef YYTYPE_UINT16
typedef YYTYPE_UINT16 yytype_uint16;
#else
typedef unsigned short int yytype_uint16;
#endif

#ifdef YYTYPE_INT16
typedef YYTYPE_INT16 yytype_int16;
#else
typedef short int yytype_int16;
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif ! defined YYSIZE_T && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned int
# endif
#endif

#define YYSIZE_MAXIMUM ((YYSIZE_T) -1)

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(msgid) dgettext ("bison-runtime", msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(msgid) msgid
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YYUSE(e) ((void) (e))
#else
# define YYUSE(e) /* empty */
#endif

/* Identity function, used to suppress warnings about constant conditions.  */
#ifndef lint
# define YYID(n) (n)
#else
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static int
YYID (int i)
#else
static int
YYID (i)
    int i;
#endif
{
  return i;
}
#endif

#if ! defined yyoverflow || YYERROR_VERBOSE

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined _STDLIB_H && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#     ifndef _STDLIB_H
#      define _STDLIB_H 1
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's `empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (YYID (0))
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined _STDLIB_H \
       && ! ((defined YYMALLOC || defined malloc) \
	     && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef _STDLIB_H
#    define _STDLIB_H 1
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined _STDLIB_H && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined _STDLIB_H && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* ! defined yyoverflow || YYERROR_VERBOSE */


#if (! defined yyoverflow \
     && (! defined __cplusplus \
	 || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yytype_int16 yyss;
  YYSTYPE yyvs;
  };

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (sizeof (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (sizeof (yytype_int16) + sizeof (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

/* Copy COUNT objects from FROM to TO.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(To, From, Count) \
      __builtin_memcpy (To, From, (Count) * sizeof (*(From)))
#  else
#   define YYCOPY(To, From, Count)		\
      do					\
	{					\
	  YYSIZE_T yyi;				\
	  for (yyi = 0; yyi < (Count); yyi++)	\
	    (To)[yyi] = (From)[yyi];		\
	}					\
      while (YYID (0))
#  endif
# endif

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack)					\
    do									\
      {									\
	YYSIZE_T yynewbytes;						\
	YYCOPY (&yyptr->Stack, Stack, yysize);				\
	Stack = &yyptr->Stack;						\
	yynewbytes = yystacksize * sizeof (*Stack) + YYSTACK_GAP_MAXIMUM; \
	yyptr += yynewbytes / sizeof (*yyptr);				\
      }									\
    while (YYID (0))

#endif

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  33
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   177

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  50
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  15
/* YYNRULES -- Number of rules.  */
#define YYNRULES  72
/* YYNRULES -- Number of states.  */
#define YYNSTATES  114

/* YYTRANSLATE(YYLEX) -- Bison symbol number corresponding to YYLEX.  */
#define YYUNDEFTOK  2
#define YYMAXUTOK   304

#define YYTRANSLATE(YYX)						\
  ((unsigned int) (YYX) <= YYMAXUTOK ? yytranslate[YYX] : YYUNDEFTOK)

/* YYTRANSLATE[YYLEX] -- Bison symbol number corresponding to YYLEX.  */
static const yytype_uint8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    48,    49
};

#if YYDEBUG
/* YYPRHS[YYN] -- Index of the first RHS symbol of rule number YYN in
   YYRHS.  */
static const yytype_uint8 yyprhs[] =
{
       0,     0,     3,     5,     9,    12,    14,    16,    18,    20,
      25,    27,    34,    41,    46,    50,    54,    58,    62,    66,
      70,    74,    77,    79,    82,    84,    90,    95,   100,   104,
     107,   111,   115,   119,   123,   126,   129,   132,   135,   137,
     143,   148,   154,   159,   164,   168,   172,   175,   179,   182,
     186,   189,   192,   194,   196,   198,   204,   209,   212,   216,
     220,   222,   224,   226,   228,   230,   232,   234,   236,   238,
     240,   242,   244
};

/* YYRHS -- A `-1'-separated list of the rules' RHS.  */
static const yytype_int8 yyrhs[] =
{
      51,     0,    -1,    52,    -1,    52,    32,    52,    -1,    52,
      32,    -1,    53,    -1,     1,    -1,    54,    -1,    55,    -1,
      13,    33,    15,    56,    -1,    56,    -1,    39,    21,    56,
      14,    56,    22,    -1,    40,    21,    56,    14,    56,    22,
      -1,    41,    21,    56,    22,    -1,    21,    56,    22,    -1,
      56,    25,    56,    -1,    56,    27,    56,    -1,    56,    28,
      56,    -1,    56,    26,    56,    -1,    56,    23,    56,    -1,
      56,    24,    56,    -1,    24,    56,    -1,    57,    -1,    58,
      34,    -1,    58,    -1,    59,    29,    29,    63,     3,    -1,
      59,    29,    63,     3,    -1,    58,    20,    63,     3,    -1,
      58,    20,    62,    -1,    58,    35,    -1,    58,    17,     3,
      -1,    58,    19,     3,    -1,    58,    16,     3,    -1,    58,
      18,     3,    -1,    58,    17,    -1,    58,    19,    -1,    58,
      16,    -1,    58,    18,    -1,    59,    -1,     3,    64,     3,
       8,    11,    -1,    64,     3,     8,    11,    -1,     3,    64,
       3,     8,    10,    -1,    64,     3,     8,    10,    -1,     3,
      64,     3,     8,    -1,    64,     3,     8,    -1,     3,    64,
       3,    -1,    64,     3,    -1,     3,    64,    26,    -1,    64,
      26,    -1,     3,    64,    34,    -1,    64,    34,    -1,     3,
       5,    -1,     5,    -1,    60,    -1,     3,    -1,     3,    64,
      30,    61,    31,    -1,    64,    30,    61,    31,    -1,    12,
      33,    -1,    61,    14,    61,    -1,     3,    38,     3,    -1,
      33,    -1,     3,    -1,    35,    -1,    37,    -1,    36,    -1,
      48,    -1,    46,    -1,    47,    -1,    45,    -1,    44,    -1,
      49,    -1,     4,    -1,     7,    -1
};

/* YYRLINE[YYN] -- source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,   107,   107,   113,   119,   121,   123,   132,   134,   139,
     167,   232,   254,   275,   292,   296,   327,   366,   407,   444,
     507,   547,   580,   584,   599,   628,   685,   732,   762,   787,
     809,   827,   846,   865,   883,   897,   912,   927,   942,   946,
     976,  1005,  1031,  1059,  1084,  1111,  1134,  1162,  1187,  1211,
    1236,  1263,  1283,  1305,  1307,  1312,  1343,  1415,  1488,  1511,
    1547,  1549,  1565,  1565,  1565,  1566,  1566,  1566,  1566,  1566,
    1566,  1569,  1580
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || YYTOKEN_TABLE
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "NUMBER", "SIDED_DIE", "FATE_DIE",
  "REPEAT", "SIDED_DIE_ZERO", "EXPLOSION", "IMPLOSION", "PENETRATE",
  "ONCE", "MACRO_ACCESSOR", "MACRO_STORAGE", "SYMBOL_SEPERATOR",
  "ASSIGNMENT", "KEEP_LOWEST", "KEEP_HIGHEST", "DROP_LOWEST",
  "DROP_HIGHEST", "FILTER", "LBRACE", "RBRACE", "PLUS", "MINUS", "MULT",
  "MODULO", "DIVIDE_ROUND_UP", "DIVIDE_ROUND_DOWN", "REROLL",
  "SYMBOL_LBRACE", "SYMBOL_RBRACE", "STATEMENT_SEPERATOR",
  "CAPITAL_STRING", "DO_COUNT", "UNIQUE", "IS_EVEN", "IS_ODD", "RANGE",
  "FN_MAX", "FN_MIN", "FN_ABS", "FN_POOL", "UMINUS", "GE", "LE", "LT",
  "GT", "EQ", "NE", "$accept", "gnoll_entry", "gnoll_statement",
  "sub_statement", "macro_statement", "dice_statement", "math",
  "collapsing_dice_operations", "dice_operations", "die_roll",
  "custom_symbol_dice", "csd", "singular_condition", "condition",
  "die_symbol", 0
};
#endif

# ifdef YYPRINT
/* YYTOKNUM[YYLEX-NUM] -- Internal token number corresponding to
   token YYLEX-NUM.  */
static const yytype_uint16 yytoknum[] =
{
       0,   256,   257,   258,   259,   260,   261,   262,   263,   264,
     265,   266,   267,   268,   269,   270,   271,   272,   273,   274,
     275,   276,   277,   278,   279,   280,   281,   282,   283,   284,
     285,   286,   287,   288,   289,   290,   291,   292,   293,   294,
     295,   296,   297,   298,   299,   300,   301,   302,   303,   304
};
# endif

/* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint8 yyr1[] =
{
       0,    50,    51,    52,    52,    52,    52,    53,    53,    54,
      55,    56,    56,    56,    56,    56,    56,    56,    56,    56,
      56,    56,    56,    57,    57,    58,    58,    58,    58,    58,
      58,    58,    58,    58,    58,    58,    58,    58,    58,    59,
      59,    59,    59,    59,    59,    59,    59,    59,    59,    59,
      59,    59,    59,    59,    59,    60,    60,    60,    61,    61,
      61,    61,    62,    62,    62,    63,    63,    63,    63,    63,
      63,    64,    64
};

/* YYR2[YYN] -- Number of symbols composing right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     1,     3,     2,     1,     1,     1,     1,     4,
       1,     6,     6,     4,     3,     3,     3,     3,     3,     3,
       3,     2,     1,     2,     1,     5,     4,     4,     3,     2,
       3,     3,     3,     3,     2,     2,     2,     2,     1,     5,
       4,     5,     4,     4,     3,     3,     2,     3,     2,     3,
       2,     2,     1,     1,     1,     5,     4,     2,     3,     3,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1
};

/* YYDEFACT[STATE-NAME] -- Default rule to reduce with in state
   STATE-NUM when YYTABLE doesn't specify something else to do.  Zero
   means the default is an error.  */
static const yytype_uint8 yydefact[] =
{
       0,     6,    54,    71,    52,    72,     0,     0,     0,     0,
       0,     0,     0,     0,     2,     5,     7,     8,    10,    22,
      24,    38,    53,     0,    51,     0,    57,     0,     0,    21,
       0,     0,     0,     1,     0,     0,     0,     0,     0,     0,
       0,    36,    34,    37,    35,     0,    23,    29,     0,    46,
      48,     0,    50,    45,    47,     0,    49,     0,    14,     0,
       0,     0,     3,    19,    20,    15,    18,    16,    17,    32,
      30,    33,    31,    62,    64,    63,    69,    68,    66,    67,
      65,    70,    28,     0,     0,     0,    44,    61,    60,     0,
      43,     0,     9,     0,     0,    13,    27,     0,    26,    42,
      40,     0,     0,    56,    41,    39,    55,     0,     0,    25,
      59,    58,    11,    12
};

/* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int8 yydefgoto[] =
{
      -1,    13,    14,    15,    16,    17,    18,    19,    20,    21,
      22,    89,    82,    83,    23
};

/* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
   STATE-NUM.  */
#define YYPACT_NINF -53
static const yytype_int16 yypact[] =
{
      35,   -53,    85,   -53,   -53,   -53,   -29,   -18,    57,    57,
      12,    14,    34,    67,    26,   -53,   -53,   -53,    90,   -53,
      92,    48,   -53,    54,   -53,    65,   -53,    64,   -16,   -53,
      57,    57,    57,   -53,    13,    57,    57,    57,    57,    57,
      57,    79,    80,    91,    97,    84,   -53,   -53,    58,    93,
     -53,    18,   -53,   114,   -53,    18,   -53,    57,   -53,   111,
     126,   119,   -53,    45,    45,   -53,   -53,   -53,   -53,   -53,
     -53,   -53,   -53,   -53,   -53,   -53,   -53,   -53,   -53,   -53,
     -53,   -53,   -53,   120,   125,   121,    33,   110,   -53,   -12,
      55,    32,    90,    57,    57,   -53,   -53,   172,   -53,   -53,
     -53,   173,    18,   -53,   -53,   -53,   -53,   133,   140,   -53,
     -53,   -53,   -53,   -53
};

/* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
     -53,   -53,    59,   -53,   -53,   -53,    -8,   -53,   -53,   -53,
     -53,   -52,   -53,   -43,   175
};

/* YYTABLE[YYPACT[STATE-NUM]].  What to do in state STATE-NUM.  If
   positive, shift that token.  If negative, reduce the rule which
   number is the opposite.  If zero, do what YYDEFACT says.
   If YYTABLE_NINF, syntax error.  */
#define YYTABLE_NINF -5
static const yytype_int8 yytable[] =
{
      28,    29,   102,    91,    26,    85,    58,    35,    36,    37,
      38,    39,    40,    -4,     1,    27,     2,     3,     4,   103,
       5,    87,    59,    60,    61,     6,     7,    63,    64,    65,
      66,    67,    68,    30,     8,    31,     1,     9,     2,     3,
       4,    97,     5,    99,   100,    -4,   102,     6,     7,    92,
     111,    88,    10,    11,    12,    32,     8,    49,    34,     9,
       2,     3,     4,   106,     5,   104,   105,    33,    53,     6,
      37,    38,    39,    40,    10,    11,    12,    48,     8,    57,
      50,     9,    69,    70,    51,   107,   108,    84,    52,     3,
      24,    54,     5,    62,    71,    55,    10,    11,    12,    56,
      72,    86,    76,    77,    78,    79,    80,    81,    41,    42,
      43,    44,    45,    35,    36,    37,    38,    39,    40,    73,
      74,    75,    90,    96,    98,    93,    46,    47,    76,    77,
      78,    79,    80,    81,    35,    36,    37,    38,    39,    40,
      94,    95,    35,    36,    37,    38,    39,    40,   101,    35,
      36,    37,    38,    39,    40,   112,    35,    36,    37,    38,
      39,    40,   113,    35,    36,    37,    38,    39,    40,    76,
      77,    78,    79,    80,    81,   109,   110,    25
};

static const yytype_uint8 yycheck[] =
{
       8,     9,    14,    55,    33,    48,    22,    23,    24,    25,
      26,    27,    28,     0,     1,    33,     3,     4,     5,    31,
       7,     3,    30,    31,    32,    12,    13,    35,    36,    37,
      38,    39,    40,    21,    21,    21,     1,    24,     3,     4,
       5,    84,     7,    10,    11,    32,    14,    12,    13,    57,
     102,    33,    39,    40,    41,    21,    21,     3,    32,    24,
       3,     4,     5,    31,     7,    10,    11,     0,     3,    12,
      25,    26,    27,    28,    39,    40,    41,    29,    21,    15,
      26,    24,     3,     3,    30,    93,    94,    29,    34,     4,
       5,    26,     7,    34,     3,    30,    39,    40,    41,    34,
       3,     8,    44,    45,    46,    47,    48,    49,    16,    17,
      18,    19,    20,    23,    24,    25,    26,    27,    28,    35,
      36,    37,     8,     3,     3,    14,    34,    35,    44,    45,
      46,    47,    48,    49,    23,    24,    25,    26,    27,    28,
      14,    22,    23,    24,    25,    26,    27,    28,    38,    23,
      24,    25,    26,    27,    28,    22,    23,    24,    25,    26,
      27,    28,    22,    23,    24,    25,    26,    27,    28,    44,
      45,    46,    47,    48,    49,     3,     3,     2
};

/* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
   symbol of state STATE-NUM.  */
static const yytype_uint8 yystos[] =
{
       0,     1,     3,     4,     5,     7,    12,    13,    21,    24,
      39,    40,    41,    51,    52,    53,    54,    55,    56,    57,
      58,    59,    60,    64,     5,    64,    33,    33,    56,    56,
      21,    21,    21,     0,    32,    23,    24,    25,    26,    27,
      28,    16,    17,    18,    19,    20,    34,    35,    29,     3,
      26,    30,    34,     3,    26,    30,    34,    15,    22,    56,
      56,    56,    52,    56,    56,    56,    56,    56,    56,     3,
       3,     3,     3,    35,    36,    37,    44,    45,    46,    47,
      48,    49,    62,    63,    29,    63,     8,     3,    33,    61,
       8,    61,    56,    14,    14,    22,     3,    63,     3,    10,
      11,    38,    14,    31,    10,    11,    31,    56,    56,     3,
       3,    61,    22,    22
};

#define yyerrok		(yyerrstatus = 0)
#define yyclearin	(yychar = YYEMPTY)
#define YYEMPTY		(-2)
#define YYEOF		0

#define YYACCEPT	goto yyacceptlab
#define YYABORT		goto yyabortlab
#define YYERROR		goto yyerrorlab


/* Like YYERROR except do call yyerror.  This remains here temporarily
   to ease the transition to the new meaning of YYERROR, for GCC.
   Once GCC version 2 has supplanted version 1, this can go.  */

#define YYFAIL		goto yyerrlab

#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)					\
do								\
  if (yychar == YYEMPTY && yylen == 1)				\
    {								\
      yychar = (Token);						\
      yylval = (Value);						\
      yytoken = YYTRANSLATE (yychar);				\
      YYPOPSTACK (1);						\
      goto yybackup;						\
    }								\
  else								\
    {								\
      yyerror (YY_("syntax error: cannot back up")); \
      YYERROR;							\
    }								\
while (YYID (0))


#define YYTERROR	1
#define YYERRCODE	256


/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

#define YYRHSLOC(Rhs, K) ((Rhs)[K])
#ifndef YYLLOC_DEFAULT
# define YYLLOC_DEFAULT(Current, Rhs, N)				\
    do									\
      if (YYID (N))                                                    \
	{								\
	  (Current).first_line   = YYRHSLOC (Rhs, 1).first_line;	\
	  (Current).first_column = YYRHSLOC (Rhs, 1).first_column;	\
	  (Current).last_line    = YYRHSLOC (Rhs, N).last_line;		\
	  (Current).last_column  = YYRHSLOC (Rhs, N).last_column;	\
	}								\
      else								\
	{								\
	  (Current).first_line   = (Current).last_line   =		\
	    YYRHSLOC (Rhs, 0).last_line;				\
	  (Current).first_column = (Current).last_column =		\
	    YYRHSLOC (Rhs, 0).last_column;				\
	}								\
    while (YYID (0))
#endif


/* YY_LOCATION_PRINT -- Print the location on the stream.
   This macro was not mandated originally: define only if we know
   we won't break user code: when these are the locations we know.  */

#ifndef YY_LOCATION_PRINT
# if defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL
#  define YY_LOCATION_PRINT(File, Loc)			\
     fprintf (File, "%d.%d-%d.%d",			\
	      (Loc).first_line, (Loc).first_column,	\
	      (Loc).last_line,  (Loc).last_column)
# else
#  define YY_LOCATION_PRINT(File, Loc) ((void) 0)
# endif
#endif


/* YYLEX -- calling `yylex' with the right arguments.  */

#ifdef YYLEX_PARAM
# define YYLEX yylex (YYLEX_PARAM)
#else
# define YYLEX yylex ()
#endif

/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)			\
do {						\
  if (yydebug)					\
    YYFPRINTF Args;				\
} while (YYID (0))

# define YY_SYMBOL_PRINT(Title, Type, Value, Location)			  \
do {									  \
  if (yydebug)								  \
    {									  \
      YYFPRINTF (stderr, "%s ", Title);					  \
      yy_symbol_print (stderr,						  \
		  Type, Value); \
      YYFPRINTF (stderr, "\n");						  \
    }									  \
} while (YYID (0))


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

/*ARGSUSED*/
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_symbol_value_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
#else
static void
yy_symbol_value_print (yyoutput, yytype, yyvaluep)
    FILE *yyoutput;
    int yytype;
    YYSTYPE const * const yyvaluep;
#endif
{
  if (!yyvaluep)
    return;
# ifdef YYPRINT
  if (yytype < YYNTOKENS)
    YYPRINT (yyoutput, yytoknum[yytype], *yyvaluep);
# else
  YYUSE (yyoutput);
# endif
  switch (yytype)
    {
      default:
	break;
    }
}


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_symbol_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
#else
static void
yy_symbol_print (yyoutput, yytype, yyvaluep)
    FILE *yyoutput;
    int yytype;
    YYSTYPE const * const yyvaluep;
#endif
{
  if (yytype < YYNTOKENS)
    YYFPRINTF (yyoutput, "token %s (", yytname[yytype]);
  else
    YYFPRINTF (yyoutput, "nterm %s (", yytname[yytype]);

  yy_symbol_value_print (yyoutput, yytype, yyvaluep);
  YYFPRINTF (yyoutput, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_stack_print (yytype_int16 *bottom, yytype_int16 *top)
#else
static void
yy_stack_print (bottom, top)
    yytype_int16 *bottom;
    yytype_int16 *top;
#endif
{
  YYFPRINTF (stderr, "Stack now");
  for (; bottom <= top; ++bottom)
    YYFPRINTF (stderr, " %d", *bottom);
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)				\
do {								\
  if (yydebug)							\
    yy_stack_print ((Bottom), (Top));				\
} while (YYID (0))


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_reduce_print (YYSTYPE *yyvsp, int yyrule)
#else
static void
yy_reduce_print (yyvsp, yyrule)
    YYSTYPE *yyvsp;
    int yyrule;
#endif
{
  int yynrhs = yyr2[yyrule];
  int yyi;
  unsigned long int yylno = yyrline[yyrule];
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %lu):\n",
	     yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      fprintf (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr, yyrhs[yyprhs[yyrule] + yyi],
		       &(yyvsp[(yyi + 1) - (yynrhs)])
		       		       );
      fprintf (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)		\
do {					\
  if (yydebug)				\
    yy_reduce_print (yyvsp, Rule); \
} while (YYID (0))

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args)
# define YY_SYMBOL_PRINT(Title, Type, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef	YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif



#if YYERROR_VERBOSE

# ifndef yystrlen
#  if defined __GLIBC__ && defined _STRING_H
#   define yystrlen strlen
#  else
/* Return the length of YYSTR.  */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static YYSIZE_T
yystrlen (const char *yystr)
#else
static YYSIZE_T
yystrlen (yystr)
    const char *yystr;
#endif
{
  YYSIZE_T yylen;
  for (yylen = 0; yystr[yylen]; yylen++)
    continue;
  return yylen;
}
#  endif
# endif

# ifndef yystpcpy
#  if defined __GLIBC__ && defined _STRING_H && defined _GNU_SOURCE
#   define yystpcpy stpcpy
#  else
/* Copy YYSRC to YYDEST, returning the address of the terminating '\0' in
   YYDEST.  */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static char *
yystpcpy (char *yydest, const char *yysrc)
#else
static char *
yystpcpy (yydest, yysrc)
    char *yydest;
    const char *yysrc;
#endif
{
  char *yyd = yydest;
  const char *yys = yysrc;

  while ((*yyd++ = *yys++) != '\0')
    continue;

  return yyd - 1;
}
#  endif
# endif

# ifndef yytnamerr
/* Copy to YYRES the contents of YYSTR after stripping away unnecessary
   quotes and backslashes, so that it's suitable for yyerror.  The
   heuristic is that double-quoting is unnecessary unless the string
   contains an apostrophe, a comma, or backslash (other than
   backslash-backslash).  YYSTR is taken from yytname.  If YYRES is
   null, do not copy; instead, return the length of what the result
   would have been.  */
static YYSIZE_T
yytnamerr (char *yyres, const char *yystr)
{
  if (*yystr == '"')
    {
      YYSIZE_T yyn = 0;
      char const *yyp = yystr;

      for (;;)
	switch (*++yyp)
	  {
	  case '\'':
	  case ',':
	    goto do_not_strip_quotes;

	  case '\\':
	    if (*++yyp != '\\')
	      goto do_not_strip_quotes;
	    /* Fall through.  */
	  default:
	    if (yyres)
	      yyres[yyn] = *yyp;
	    yyn++;
	    break;

	  case '"':
	    if (yyres)
	      yyres[yyn] = '\0';
	    return yyn;
	  }
    do_not_strip_quotes: ;
    }

  if (! yyres)
    return yystrlen (yystr);

  return yystpcpy (yyres, yystr) - yyres;
}
# endif

/* Copy into YYRESULT an error message about the unexpected token
   YYCHAR while in state YYSTATE.  Return the number of bytes copied,
   including the terminating null byte.  If YYRESULT is null, do not
   copy anything; just return the number of bytes that would be
   copied.  As a special case, return 0 if an ordinary "syntax error"
   message will do.  Return YYSIZE_MAXIMUM if overflow occurs during
   size calculation.  */
static YYSIZE_T
yysyntax_error (char *yyresult, int yystate, int yychar)
{
  int yyn = yypact[yystate];

  if (! (YYPACT_NINF < yyn && yyn <= YYLAST))
    return 0;
  else
    {
      int yytype = YYTRANSLATE (yychar);
      YYSIZE_T yysize0 = yytnamerr (0, yytname[yytype]);
      YYSIZE_T yysize = yysize0;
      YYSIZE_T yysize1;
      int yysize_overflow = 0;
      enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
      char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];
      int yyx;

# if 0
      /* This is so xgettext sees the translatable formats that are
	 constructed on the fly.  */
      YY_("syntax error, unexpected %s");
      YY_("syntax error, unexpected %s, expecting %s");
      YY_("syntax error, unexpected %s, expecting %s or %s");
      YY_("syntax error, unexpected %s, expecting %s or %s or %s");
      YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s");
# endif
      char *yyfmt;
      char const *yyf;
      static char const yyunexpected[] = "syntax error, unexpected %s";
      static char const yyexpecting[] = ", expecting %s";
      static char const yyor[] = " or %s";
      char yyformat[sizeof yyunexpected
		    + sizeof yyexpecting - 1
		    + ((YYERROR_VERBOSE_ARGS_MAXIMUM - 2)
		       * (sizeof yyor - 1))];
      char const *yyprefix = yyexpecting;

      /* Start YYX at -YYN if negative to avoid negative indexes in
	 YYCHECK.  */
      int yyxbegin = yyn < 0 ? -yyn : 0;

      /* Stay within bounds of both yycheck and yytname.  */
      int yychecklim = YYLAST - yyn + 1;
      int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
      int yycount = 1;

      yyarg[0] = yytname[yytype];
      yyfmt = yystpcpy (yyformat, yyunexpected);

      for (yyx = yyxbegin; yyx < yyxend; ++yyx)
	if (yycheck[yyx + yyn] == yyx && yyx != YYTERROR)
	  {
	    if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
	      {
		yycount = 1;
		yysize = yysize0;
		yyformat[sizeof yyunexpected - 1] = '\0';
		break;
	      }
	    yyarg[yycount++] = yytname[yyx];
	    yysize1 = yysize + yytnamerr (0, yytname[yyx]);
	    yysize_overflow |= (yysize1 < yysize);
	    yysize = yysize1;
	    yyfmt = yystpcpy (yyfmt, yyprefix);
	    yyprefix = yyor;
	  }

      yyf = YY_(yyformat);
      yysize1 = yysize + yystrlen (yyf);
      yysize_overflow |= (yysize1 < yysize);
      yysize = yysize1;

      if (yysize_overflow)
	return YYSIZE_MAXIMUM;

      if (yyresult)
	{
	  /* Avoid sprintf, as that infringes on the user's name space.
	     Don't have undefined behavior even if the translation
	     produced a string with the wrong number of "%s"s.  */
	  char *yyp = yyresult;
	  int yyi = 0;
	  while ((*yyp = *yyf) != '\0')
	    {
	      if (*yyp == '%' && yyf[1] == 's' && yyi < yycount)
		{
		  yyp += yytnamerr (yyp, yyarg[yyi++]);
		  yyf += 2;
		}
	      else
		{
		  yyp++;
		  yyf++;
		}
	    }
	}
      return yysize;
    }
}
#endif /* YYERROR_VERBOSE */


/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

/*ARGSUSED*/
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep)
#else
static void
yydestruct (yymsg, yytype, yyvaluep)
    const char *yymsg;
    int yytype;
    YYSTYPE *yyvaluep;
#endif
{
  YYUSE (yyvaluep);

  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yytype, yyvaluep, yylocationp);

  switch (yytype)
    {

      default:
	break;
    }
}


/* Prevent warnings from -Wmissing-prototypes.  */

#ifdef YYPARSE_PARAM
#if defined __STDC__ || defined __cplusplus
int yyparse (void *YYPARSE_PARAM);
#else
int yyparse ();
#endif
#else /* ! YYPARSE_PARAM */
#if defined __STDC__ || defined __cplusplus
int yyparse (void);
#else
int yyparse ();
#endif
#endif /* ! YYPARSE_PARAM */



/* The look-ahead symbol.  */
int yychar;

/* The semantic value of the look-ahead symbol.  */
YYSTYPE yylval;

/* Number of syntax errors so far.  */
int yynerrs;



/*----------.
| yyparse.  |
`----------*/

#ifdef YYPARSE_PARAM
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
int
yyparse (void *YYPARSE_PARAM)
#else
int
yyparse (YYPARSE_PARAM)
    void *YYPARSE_PARAM;
#endif
#else /* ! YYPARSE_PARAM */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
int
yyparse (void)
#else
int
yyparse ()

#endif
#endif
{
  
  int yystate;
  int yyn;
  int yyresult;
  /* Number of tokens to shift before error messages enabled.  */
  int yyerrstatus;
  /* Look-ahead token as an internal (translated) token number.  */
  int yytoken = 0;
#if YYERROR_VERBOSE
  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYSIZE_T yymsg_alloc = sizeof yymsgbuf;
#endif

  /* Three stacks and their tools:
     `yyss': related to states,
     `yyvs': related to semantic values,
     `yyls': related to locations.

     Refer to the stacks thru separate pointers, to allow yyoverflow
     to reallocate them elsewhere.  */

  /* The state stack.  */
  yytype_int16 yyssa[YYINITDEPTH];
  yytype_int16 *yyss = yyssa;
  yytype_int16 *yyssp;

  /* The semantic value stack.  */
  YYSTYPE yyvsa[YYINITDEPTH];
  YYSTYPE *yyvs = yyvsa;
  YYSTYPE *yyvsp;



#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  YYSIZE_T yystacksize = YYINITDEPTH;

  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;


  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yystate = 0;
  yyerrstatus = 0;
  yynerrs = 0;
  yychar = YYEMPTY;		/* Cause a token to be read.  */

  /* Initialize stack pointers.
     Waste one element of value and location stack
     so that they stay on the same level as the state stack.
     The wasted elements are never initialized.  */

  yyssp = yyss;
  yyvsp = yyvs;

  goto yysetstate;

/*------------------------------------------------------------.
| yynewstate -- Push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
 yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;

 yysetstate:
  *yyssp = yystate;

  if (yyss + yystacksize - 1 <= yyssp)
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYSIZE_T yysize = yyssp - yyss + 1;

#ifdef yyoverflow
      {
	/* Give user a chance to reallocate the stack.  Use copies of
	   these so that the &'s don't force the real ones into
	   memory.  */
	YYSTYPE *yyvs1 = yyvs;
	yytype_int16 *yyss1 = yyss;


	/* Each stack pointer address is followed by the size of the
	   data in use in that stack, in bytes.  This used to be a
	   conditional around just the two extra args, but that might
	   be undefined if yyoverflow is a macro.  */
	yyoverflow (YY_("memory exhausted"),
		    &yyss1, yysize * sizeof (*yyssp),
		    &yyvs1, yysize * sizeof (*yyvsp),

		    &yystacksize);

	yyss = yyss1;
	yyvs = yyvs1;
      }
#else /* no yyoverflow */
# ifndef YYSTACK_RELOCATE
      goto yyexhaustedlab;
# else
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
	goto yyexhaustedlab;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
	yystacksize = YYMAXDEPTH;

      {
	yytype_int16 *yyss1 = yyss;
	union yyalloc *yyptr =
	  (union yyalloc *) YYSTACK_ALLOC (YYSTACK_BYTES (yystacksize));
	if (! yyptr)
	  goto yyexhaustedlab;
	YYSTACK_RELOCATE (yyss);
	YYSTACK_RELOCATE (yyvs);

#  undef YYSTACK_RELOCATE
	if (yyss1 != yyssa)
	  YYSTACK_FREE (yyss1);
      }
# endif
#endif /* no yyoverflow */

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;


      YYDPRINTF ((stderr, "Stack size increased to %lu\n",
		  (unsigned long int) yystacksize));

      if (yyss + yystacksize - 1 <= yyssp)
	YYABORT;
    }

  YYDPRINTF ((stderr, "Entering state %d\n", yystate));

  goto yybackup;

/*-----------.
| yybackup.  |
`-----------*/
yybackup:

  /* Do appropriate processing given the current state.  Read a
     look-ahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to look-ahead token.  */
  yyn = yypact[yystate];
  if (yyn == YYPACT_NINF)
    goto yydefault;

  /* Not known => get a look-ahead token if don't already have one.  */

  /* YYCHAR is either YYEMPTY or YYEOF or a valid look-ahead symbol.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token: "));
      yychar = YYLEX;
    }

  if (yychar <= YYEOF)
    {
      yychar = yytoken = YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yyn == 0 || yyn == YYTABLE_NINF)
	goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  if (yyn == YYFINAL)
    YYACCEPT;

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the look-ahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);

  /* Discard the shifted token unless it is eof.  */
  if (yychar != YYEOF)
    yychar = YYEMPTY;

  yystate = yyn;
  *++yyvsp = yylval;

  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- Do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     `$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
        case 2:
#line 107 "src/grammar/dice.yacc"
    {
        free_vector((yyvsp[(1) - (1)].values));
    }
    break;

  case 3:
#line 113 "src/grammar/dice.yacc"
    {
        free_vector((yyvsp[(3) - (3)].values));
        // vec1 freed at root.
    }
    break;

  case 6:
#line 123 "src/grammar/dice.yacc"
    {
        printf("Invalid Notation\n");
        gnoll_errno = SYNTAX_ERROR;
        YYABORT;
        yyclearin;
    }
    break;

  case 9:
#line 139 "src/grammar/dice.yacc"
    {
        /**
        * MACRO_STORAGE - the symbol '#''
        * CAPITAL_STRING - vector 
        * ASSIGNMENT - the symbol '='
        * math - vector dice roll assignment
        * returns - nothing.
        */
                
        vec key = (yyvsp[(2) - (4)].values);
        vec value = (yyvsp[(4) - (4)].values);

        register_macro(&key, &value.source);

        // Cleanup
        free_vector(key);
        free_vector(value);
        
        if(gnoll_errno){
            YYABORT;
            yyclearin;
        }
        vec null_vec;
        light_initialize_vector(&null_vec, NUMERIC, 0);
        (yyval.values) = null_vec;
    }
    break;

  case 10:
#line 167 "src/grammar/dice.yacc"
    {
    /**
    * functions a vector
    * return NULL
    */

    vec vector = (yyvsp[(1) - (1)].values);
    vec new_vec;

    //  Step 1: Collapse pool to a single value if nessicary
    collapse_vector(&vector, &new_vec);
    if(gnoll_errno){
        YYABORT;
        yyclearin;
    }

    // Step 2: Output to file
    FILE *fp = NULL;

    if(write_to_file){
        fp = safe_fopen(output_file, "a+");
        if(gnoll_errno){
            YYABORT;
            yyclearin;
        }
    }

    // TODO: To Function
    for(unsigned int i = 0; i!= new_vec.length;i++){
        if (new_vec.dtype == SYMBOLIC){
            // TODO: Strings >1 character
            if (verbose){
                printf("%s;", new_vec.symbols[i]);
            }
            if(write_to_file){
                fprintf(fp, "%s;", new_vec.symbols[i]);
            }
        }else{
            if(verbose){
                printf("%d;", new_vec.content[i]);
            }
            if(write_to_file){
                fprintf(fp, "%d;", new_vec.content[i]);
            }
        }
    }
    if(verbose){
       printf("\n");
    }
    
    if (dice_breakdown){
        fprintf(fp, "\n");
    }

    if(write_to_file){
        fclose(fp);
    }

    free_vector(vector);
    
    (yyval.values) = new_vec;
}
    break;

  case 11:
#line 232 "src/grammar/dice.yacc"
    {
        /** @brief performs the min(__, __) function
        * @FN_MAX the symbol "max"
        * @LBRACE the symbol "("
        * function The target vector
        * SYMBOL_SEPERATOR the symbol ","
        * function The target vector
        * @RBRACE the symbol ")"
        * return vector
        */
        vec new_vec;
        initialize_vector(&new_vec, NUMERIC, 1);
        int vmax = MAXV(
            (yyvsp[(3) - (6)].values).content[0],
            (yyvsp[(5) - (6)].values).content[0]
        );
        new_vec.content[0] = vmax;
        (yyval.values) = new_vec;
        free_vector((yyvsp[(3) - (6)].values));
        free_vector((yyvsp[(5) - (6)].values));
    }
    break;

  case 12:
#line 254 "src/grammar/dice.yacc"
    {
        /** @brief performs the min(__, __) function
        * @FN_MIN the symbol "min"
        * @LBRACE the symbol "("
        * function The target vector
        * SYMBOL_SEPERATOR the symbol ","
        * function The target vector
        * @RBRACE the symbol ")"
        * return vector
        */
        vec new_vec;
        initialize_vector(&new_vec, NUMERIC, 1);
        new_vec.content[0] = MINV(
            (yyvsp[(3) - (6)].values).content[0],
            (yyvsp[(5) - (6)].values).content[0]
        );
        (yyval.values) = new_vec;
        free_vector((yyvsp[(3) - (6)].values));
        free_vector((yyvsp[(5) - (6)].values));
    }
    break;

  case 13:
#line 275 "src/grammar/dice.yacc"
    {
        /** @brief performs the abs(__) function
        * @FN_ABS the symbol "abs"
        * @LBRACE the symbol "("
        * function The target vector
        * @RBRACE the symbol ")"
        * return vector
        */
        vec new_vec;
        initialize_vector(&new_vec, NUMERIC, 1);
        new_vec.content[0] = ABSV(
            (yyvsp[(3) - (4)].values).content[0]
        );
        (yyval.values) = new_vec;
        free_vector((yyvsp[(3) - (4)].values));
    }
    break;

  case 14:
#line 292 "src/grammar/dice.yacc"
    {
        (yyval.values) = (yyvsp[(2) - (3)].values);
    }
    break;

  case 15:
#line 296 "src/grammar/dice.yacc"
    {
        /** @brief Collapse both sides and multiply
        * Math vector
        * MULT symbol '*'
        * Math vector
        */
        vec vector1 = (yyvsp[(1) - (3)].values);
        vec vector2 = (yyvsp[(3) - (3)].values);

        if (vector1.dtype == SYMBOLIC || vector2.dtype == SYMBOLIC){
            printf("Multiplication not implemented for symbolic dice.\n");
            gnoll_errno = NOT_IMPLEMENTED;
            YYABORT;
            yyclearin;
        }else{
            int v1 = collapse(vector1.content, vector1.length);
            int v2 = collapse(vector2.content, vector2.length);

            vec new_vec;
            new_vec.content = safe_calloc(sizeof(int), 1);
            new_vec.length = 1;
            new_vec.content[0] = v1 * v2;
            new_vec.dtype = vector1.dtype;

            (yyval.values) = new_vec;
        }
        
        free_vector(vector1);
        free_vector(vector2);
    }
    break;

  case 16:
#line 327 "src/grammar/dice.yacc"
    {
        /** @brief Collapse both sides and divide
        * Math vector
        * Divide symbol '/'
        * Math vector
        */
        // Collapse both sides and subtract
        vec vector1 = (yyvsp[(1) - (3)].values);
        vec vector2 = (yyvsp[(3) - (3)].values);

        if (vector1.dtype == SYMBOLIC || vector2.dtype == SYMBOLIC){
            printf("Division unsupported for symbolic dice.\n");
            gnoll_errno = UNDEFINED_BEHAVIOUR;
            YYABORT;
            yyclearin;

        }else{
            int v1 = collapse(vector1.content, vector1.length);
            int v2 = collapse(vector2.content, vector2.length);

            vec new_vec;
            new_vec.content = safe_calloc(sizeof(int), 1);
            if(gnoll_errno){ YYABORT; yyclearin;}
            new_vec.length = 1;
            if(v2==0){
                gnoll_errno=DIVIDE_BY_ZERO;
                new_vec.content[0] = 0;
            }else{
                new_vec.content[0] = (v1+(v2-1))/ v2;
            }
            new_vec.dtype = vector1.dtype;

            (yyval.values) = new_vec;
        }
        
        free_vector(vector1);
        free_vector(vector2);
    }
    break;

  case 17:
#line 366 "src/grammar/dice.yacc"
    {
        /** @brief Collapse both sides and divide
        * Math vector
        * Divide symbol '\'
        * Math vector
        */
        // Collapse both sides and subtract
        vec vector1 = (yyvsp[(1) - (3)].values);
        vec vector2 = (yyvsp[(3) - (3)].values);

        if (vector1.dtype == SYMBOLIC || vector2.dtype == SYMBOLIC){
            printf("Division unsupported for symbolic dice.\n");
            gnoll_errno = UNDEFINED_BEHAVIOUR;
            YYABORT;
            yyclearin;
        }else{
            int v1 = collapse(vector1.content, vector1.length);
            int v2 = collapse(vector2.content, vector2.length);

            vec new_vec;
            new_vec.content = safe_calloc(sizeof(int), 1);
            if(gnoll_errno){
               YYABORT;
               yyclearin;
            }
            new_vec.length = 1;
            if(v2==0){
                gnoll_errno=DIVIDE_BY_ZERO;
                new_vec.content[0] = 0;
            }else{
                new_vec.content[0] = v1 / v2;
            }
            new_vec.dtype = vector1.dtype;

            (yyval.values) = new_vec;
        }
        
        free_vector(vector1);
        free_vector(vector2);
    }
    break;

  case 18:
#line 407 "src/grammar/dice.yacc"
    {
        /** @brief Collapse both sides and modulo
        * Math vector
        * MULT symbol '%'
        * Math vector
        */
        // Collapse both sides and subtract
        vec vector1 = (yyvsp[(1) - (3)].values);
        vec vector2 = (yyvsp[(3) - (3)].values);

        if (vector1.dtype == SYMBOLIC || vector2.dtype == SYMBOLIC){
            printf("Modulo unsupported for symbolic dice.\n");
            gnoll_errno = UNDEFINED_BEHAVIOUR;
            YYABORT;
            yyclearin;

        }else{
            int v1 = collapse(vector1.content, vector1.length);
            int v2 = collapse(vector2.content, vector2.length);

            vec new_vec;
            new_vec.content = safe_calloc(sizeof(int), 1);
            if(gnoll_errno){
                YYABORT;
                yyclearin;
            }
            new_vec.length = 1;
            new_vec.content[0] = v1 % v2;
            new_vec.dtype = vector1.dtype;

            (yyval.values) = new_vec;
        }
        
        free_vector(vector1);
        free_vector(vector2);
    }
    break;

  case 19:
#line 444 "src/grammar/dice.yacc"
    {
        /** @brief
        * math vector
        * PLUS symbol "+"
        * math vector
        */
        // Collapse both sides and subtract
        vec vector1 = (yyvsp[(1) - (3)].values);
        vec vector2 = (yyvsp[(3) - (3)].values);

        if (
            (vector1.dtype == SYMBOLIC && vector2.dtype == NUMERIC) ||
            (vector2.dtype == SYMBOLIC && vector1.dtype == NUMERIC)
        ){
            printf("Addition not supported with mixed dice types.\n");
            gnoll_errno = UNDEFINED_BEHAVIOUR;
            YYABORT;
            yyclearin;
        } else if (vector1.dtype == SYMBOLIC){
            vec new_vec;
            unsigned int concat_length = vector1.length + vector2.length;
            new_vec.symbols = safe_calloc(sizeof(char *), concat_length);
            if(gnoll_errno){
                YYABORT;
                yyclearin;
            }
            for (unsigned int i = 0; i != concat_length; i++){
                new_vec.symbols[i] = safe_calloc(sizeof(char), MAX_SYMBOL_LENGTH);
                if(gnoll_errno){
                    YYABORT;
                    yyclearin;
                }
            }
            new_vec.length = concat_length;
            new_vec.dtype = vector1.dtype;

            concat_symbols(
                vector1.symbols, vector1.length,
                vector2.symbols, vector2.length,
                new_vec.symbols
            );
            (yyval.values) = new_vec;
        }else{
            int v1 = collapse(vector1.content, vector1.length);
            int v2 = collapse(vector2.content, vector2.length);

            vec new_vec;
            new_vec.content = safe_calloc(sizeof(int), 1);
            if(gnoll_errno){
                YYABORT;
                yyclearin;
            }
            new_vec.length = 1;
            new_vec.dtype = vector1.dtype;
            new_vec.content[0] = v1 + v2;

            (yyval.values) = new_vec;
        }
        free_vector(vector1);
        free_vector(vector2);

    }
    break;

  case 20:
#line 507 "src/grammar/dice.yacc"
    {
        /** @brief Collapse both sides and subtract
        * Math vector
        * MINUS symbol '-'
        * Math vector
        */
        vec vector1 = (yyvsp[(1) - (3)].values);
        vec vector2 = (yyvsp[(3) - (3)].values);
        if (
            (vector1.dtype == SYMBOLIC || vector2.dtype == SYMBOLIC)
        ){
            // It's not clear whether {+,-} - {-, 0} should be {+} or {+, 0}!
            // Therfore, we'll exclude it.
            printf("Subtract not supported with symbolic dice.\n");
            gnoll_errno = UNDEFINED_BEHAVIOUR;
            YYABORT;
            yyclearin;;
        }else{
            // Collapse both sides and subtract

            int v1 = collapse(vector1.content, vector1.length);
            int v2 = collapse(vector2.content, vector2.length);

            vec new_vec;
            new_vec.content = safe_calloc(sizeof(int), 1);
            if(gnoll_errno){
                YYABORT;
                yyclearin;
            }
            new_vec.length = 1;
            new_vec.content[0] = v1 - v2;
            new_vec.dtype = vector1.dtype;

            (yyval.values) = new_vec;
        }
        free_vector(vector1);
        free_vector(vector2);

    }
    break;

  case 21:
#line 547 "src/grammar/dice.yacc"
    {
        /**
        * MINUS a symbol '-'
        * math a vector
        */
        // Eltwise Negation
        vec vector = (yyvsp[(2) - (2)].values);

        if (vector.dtype == SYMBOLIC){
            printf("Symbolic Dice, Cannot negate. Consider using Numeric dice or post-processing.\n");
            gnoll_errno = UNDEFINED_BEHAVIOUR;
            YYABORT;
            yyclearin;;
        } else {
            vec new_vec;

            new_vec.content = safe_calloc(sizeof(int), vector.length);
            if(gnoll_errno){
                YYABORT;
                yyclearin;
            }
            new_vec.length = vector.length;
            new_vec.dtype = vector.dtype;

            for(unsigned int i = 0; i != vector.length; i++){
                new_vec.content[i] = - vector.content[i];
            }
            (yyval.values) = new_vec;

        }
        free_vector(vector);
    }
    break;

  case 23:
#line 584 "src/grammar/dice.yacc"
    {
        /**
        * dice_operations - a vector
        * DO_COUNT - a symbol 'c'
        */

        vec new_vec;
        vec dice = (yyvsp[(1) - (2)].values);
        initialize_vector(&new_vec, NUMERIC, 1);

        new_vec.content[0] = (int)dice.length;
        free_vector(dice);
        (yyval.values) = new_vec;
    }
    break;

  case 24:
#line 599 "src/grammar/dice.yacc"
    {
        /** 
        * dice_operations a vector
        * returns a vector
        */

        vec vector = (yyvsp[(1) - (1)].values);

        if (vector.dtype == SYMBOLIC){
            // Symbolic, Impossible to collapse
            (yyval.values) = vector;
        }
        else{
            // Collapse if Necessary
            if(vector.length > 1){
                vec new_vector;
                initialize_vector(&new_vector, NUMERIC, 1);
                new_vector.content[0] = sum(vector.content, vector.length);
                (yyval.values) = new_vector;
                free_vector(vector);
            }else{
                (yyval.values) = vector;
            }
        }
    }
    break;

  case 25:
#line 628 "src/grammar/dice.yacc"
    {
        /** 
        * dice_roll a vector
        * REROLL symbol 'r'
        * REROLL symbol 'r'
        * condition vector
        * Number vector
        * returns a vector
        */

        vec dice = (yyvsp[(1) - (5)].values);
        vec cv = (yyvsp[(4) - (5)].values);
        vec cvno = (yyvsp[(5) - (5)].values);

        int check = cv.content[0];

        if(dice.dtype == NUMERIC){
            int count = 0;
            while (! check_condition(&dice, &cvno, (COMPARATOR)check)){
                if (count > MAX_ITERATION){
                    printf("MAX ITERATION LIMIT EXCEEDED: REROLL\n");
                    gnoll_errno = MAX_LOOP_LIMIT_HIT;
                    YYABORT; 
                    yyclearin;
                    break;
                }
                vec number_of_dice;
                initialize_vector(&number_of_dice, NUMERIC, 1);
                number_of_dice.content[0] = (int)dice.source.number_of_dice;

                vec die_sides;
                initialize_vector(&die_sides, NUMERIC, 1);
                die_sides.content[0] = (int)dice.source.die_sides;

                roll_plain_sided_dice(
                    &number_of_dice,
                    &die_sides,
                    &dice,
                    dice.source.explode,
                    1
                );
                count ++;
                free_vector(die_sides);
                free_vector(number_of_dice);
            }
            (yyval.values) = dice;

        }else{
            printf("No support for Symbolic die rerolling yet!\n");
            gnoll_errno = NOT_IMPLEMENTED;
            YYABORT;
            yyclearin;
        }
        free_vector(cv);
        free_vector(cvno);
    }
    break;

  case 26:
#line 685 "src/grammar/dice.yacc"
    {
        /*
        * die_roll vector
        * Reroll symbol
        * condition vector
        * Number vector
        */

        vec dice = (yyvsp[(1) - (4)].values);
        vec comp = (yyvsp[(3) - (4)].values);
        int check = comp.content[0];
        vec numv = (yyvsp[(4) - (4)].values);

        if(dice.dtype == NUMERIC){
            if (check_condition(&dice, &numv, (COMPARATOR)check)){

                vec number_of_dice;
                initialize_vector(&number_of_dice, NUMERIC, 1);
                number_of_dice.content[0] = (int)dice.source.number_of_dice;

                vec die_sides;
                initialize_vector(&die_sides, NUMERIC, 1);
                die_sides.content[0] = (int)dice.source.die_sides;

                roll_plain_sided_dice(
                    &number_of_dice,
                    &die_sides,
                    &(yyval.values),
                    dice.source.explode,
                    1
                );
                free_vector(dice);
                free_vector(number_of_dice);
            }else{
                // No need to reroll
                (yyval.values) = dice;
            }
        }else{
            printf("No support for Symbolic die rerolling yet!");
            gnoll_errno = NOT_IMPLEMENTED;
            YYABORT;
            yyclearin;;
        }
        free_vector(numv);
        free_vector(comp);
    }
    break;

  case 27:
#line 732 "src/grammar/dice.yacc"
    {
        /*
        * dice_operations vector
        * Filter symbol 'f'
        * condition vector
        * Number vector
        */
        vec new_vec;
        vec dice = (yyvsp[(1) - (4)].values);
        vec condition = (yyvsp[(4) - (4)].values);
        vec cv = (yyvsp[(3) - (4)].values);

        int check = cv.content[0];

        if(dice.dtype == NUMERIC){
            initialize_vector(&new_vec, NUMERIC, dice.length);
            filter(&dice, &condition, check, &new_vec);

            (yyval.values) = new_vec;
        }else{
            printf("No support for Symbolic die rerolling yet!\n");
            gnoll_errno = NOT_IMPLEMENTED;
            YYABORT;
            yyclearin;
        }
        free_vector(dice);
        free_vector(condition);
        free_vector(cv);
    }
    break;

  case 28:
#line 762 "src/grammar/dice.yacc"
    {
        /**
        * dice_operations vector
        * FILTER symbol 'f'
        * singular_condition symbol
        */
        vec dice = (yyvsp[(1) - (3)].values);
        int check = (yyvsp[(3) - (3)].values).content[0];
        vec new_vec;

        if(dice.dtype == NUMERIC){
            initialize_vector(&new_vec, NUMERIC, dice.length);
            filter(&dice, NULL, check, &new_vec);

            (yyval.values) = new_vec;
        }else{
            printf("No support for Symbolic die rerolling yet!\n");
            gnoll_errno = NOT_IMPLEMENTED;
            YYABORT;
            yyclearin;;
        }
        free_vector(dice);

    }
    break;

  case 29:
#line 787 "src/grammar/dice.yacc"
    {
        /**
        * dice_operations vector
        * UNIQUE symbol 'u'
        */
        vec new_vec;
        vec dice = (yyvsp[(1) - (2)].values);

        if(dice.dtype == NUMERIC){
            initialize_vector(&new_vec, NUMERIC, dice.length);
            filter_unique(&dice, &new_vec);

            (yyval.values) = new_vec;
        }else{
            printf("No support for Symbolic die rerolling yet!\n");
            gnoll_errno = NOT_IMPLEMENTED;
            YYABORT;
            yyclearin;;
        }
        free_vector(dice);
    }
    break;

  case 30:
#line 809 "src/grammar/dice.yacc"
    {
        /**
        * dice_operations vector
        * KEEP_HIGHEST symbol 'kh'
        * NUMBER vector
        */
        vec do_vec = (yyvsp[(1) - (3)].values);
        vec keep_vector = (yyvsp[(3) - (3)].values);
        vec new_vec;
        unsigned int num_to_hold = (unsigned int)keep_vector.content[0];

        keep_highest_values(&do_vec, &new_vec, num_to_hold);

        (yyval.values) = new_vec;
        // free_vector(do_vec);
        free_vector(keep_vector);
    }
    break;

  case 31:
#line 827 "src/grammar/dice.yacc"
    {
        /**
        * dice_operations vector
        * KEEP_HIGHEST symbol 'kh'
        * NUMBER vector
        */
        vec do_vec = (yyvsp[(1) - (3)].values);
        vec keep_vector = (yyvsp[(3) - (3)].values);
        vec new_vec;
        unsigned int num_to_hold = (unsigned int)keep_vector.content[0];

        drop_highest_values(&do_vec, &new_vec, num_to_hold);

        (yyval.values) = new_vec;
        // free_vector(do_vec);
        free_vector(keep_vector);

    }
    break;

  case 32:
#line 846 "src/grammar/dice.yacc"
    {
        /**
        * dice_operations vector
        * KEEP_HIGHEST symbol 'kh'
        * NUMBER vector
        */

        vec do_vec = (yyvsp[(1) - (3)].values);
        vec keep_vector = (yyvsp[(3) - (3)].values);
        unsigned int num_to_hold = (unsigned int)keep_vector.content[0];

        vec new_vec;
        keep_lowest_values(&do_vec, &new_vec, num_to_hold);

        (yyval.values) = new_vec;
        // free_vector(do_vec);
        free_vector(keep_vector);
    }
    break;

  case 33:
#line 865 "src/grammar/dice.yacc"
    {
        /**
        * dice_operations vector
        * KEEP_HIGHEST symbol 'kh'
        * NUMBER vector
        */
        vec do_vec = (yyvsp[(1) - (3)].values);
        vec keep_vector = (yyvsp[(3) - (3)].values);
        unsigned int num_to_hold = (unsigned int)keep_vector.content[0];

        vec new_vec;
        drop_lowest_values(&do_vec, &new_vec, num_to_hold);

        (yyval.values) = new_vec;
        // free_vector(do_vec);
        free_vector(keep_vector);
    }
    break;

  case 34:
#line 883 "src/grammar/dice.yacc"
    {
        /**
        * dice_operations vector
        * KEEP_HIGHEST symbol 'kh'
        */
        vec do_vec = (yyvsp[(1) - (2)].values);
        unsigned int num_to_hold = 1;
        vec new_vec;
        keep_highest_values(&do_vec, &new_vec, num_to_hold);

        (yyval.values) = new_vec;
        // free_vector(do_vec);
    }
    break;

  case 35:
#line 897 "src/grammar/dice.yacc"
    {
        /**
        * dice_operations vector
        * KEEP_HIGHEST symbol 'kh'
        */
        vec roll_vec = (yyvsp[(1) - (2)].values);
        unsigned int num_to_hold = 1;

        vec new_vec;
        drop_highest_values(&roll_vec, &new_vec, num_to_hold);

        (yyval.values) = new_vec;
        // free_vector(roll_vec);
    }
    break;

  case 36:
#line 912 "src/grammar/dice.yacc"
    {
        /**
        * dice_operations vector
        * KEEP_LOWEST symbol 'kh'
        */
        vec roll_vec = (yyvsp[(1) - (2)].values);
        unsigned int num_to_hold = 1;

        vec new_vec;
        keep_lowest_values(&roll_vec, &new_vec, num_to_hold);

        (yyval.values) = new_vec;
        // free_vector(roll_vec);
    }
    break;

  case 37:
#line 927 "src/grammar/dice.yacc"
    {
        /**
        * dice_operations vector
        * DROP_LOWEST symbol 'dl'
        */
        vec roll_vec = (yyvsp[(1) - (2)].values);
        unsigned int num_to_hold = 1;

        vec new_vec;
        drop_lowest_values(&roll_vec, &new_vec, num_to_hold);

        (yyval.values) = new_vec;
        // free_vector(roll_vec);
    }
    break;

  case 39:
#line 946 "src/grammar/dice.yacc"
    {
        /**
        * NUMBER vector
        * die_symbol vector 
        * NUMBER vector
        * EXPLOSION symbol 'e' or similar
        * ONCE symbol 'o'
        */
        vec numA = (yyvsp[(1) - (5)].values);
        vec ds = (yyvsp[(2) - (5)].values);
        vec numB = (yyvsp[(3) - (5)].values);

        int start_from = ds.content[0];

        vec number_of_dice;
        initialize_vector(&number_of_dice, NUMERIC, 1);
        number_of_dice.content[0] = 1;

        roll_plain_sided_dice(
            &numA,
            &numB,
            &(yyval.values),
            ONLY_ONCE_EXPLOSION,
            start_from
        );
        free_vector(numA);
        free_vector(ds);
        free_vector(numB);
    }
    break;

  case 40:
#line 976 "src/grammar/dice.yacc"
    {
        /**
        * die_symbol vector 
        * NUMBER vector
        * EXPLOSION symbol 'e' or similar
        * ONCE symbol 'o'
        */
        
        vec ds = (yyvsp[(1) - (4)].values);
        vec numB = (yyvsp[(2) - (4)].values);

        int start_from = ds.content[0];

        vec number_of_dice;
        initialize_vector(&number_of_dice, NUMERIC, 1);
        number_of_dice.content[0] = 1;

        roll_plain_sided_dice(
            &number_of_dice,
            &numB,
            &(yyval.values),
            ONLY_ONCE_EXPLOSION,
            start_from
        );
        free_vector(number_of_dice);
        free_vector(ds);
        free_vector(numB);
    }
    break;

  case 41:
#line 1005 "src/grammar/dice.yacc"
    {
        /**
        * NUMBER vector
        * die_symbol vector 
        * NUMBER vector
        * EXPLOSION symbol 'e' or similar
        * PENETRATE symbol 'p'
        */
        vec numA = (yyvsp[(1) - (5)].values);
        vec ds = (yyvsp[(2) - (5)].values);
        vec numB = (yyvsp[(3) - (5)].values);
        int start_from = ds.content[0];

        roll_plain_sided_dice(
            &numA,
            &numB,
            &(yyval.values),
            PENETRATING_EXPLOSION,
            start_from
        );
        
        free_vector(numA);
        free_vector(ds);
        free_vector(numB);
    }
    break;

  case 42:
#line 1031 "src/grammar/dice.yacc"
    {
        /**
        * die_symbol vector 
        * NUMBER vector
        * EXPLOSION symbol 'e' or similar
        * PENETRATE symbol 'p'
        */
        vec ds = (yyvsp[(1) - (4)].values);
        vec numB = (yyvsp[(2) - (4)].values);
        
        int start_from = ds.content[0];

        vec number_of_dice;
        initialize_vector(&number_of_dice, NUMERIC, 1);
        number_of_dice.content[0] = 1;

        roll_plain_sided_dice(
            &number_of_dice,
            &numB,
            &(yyval.values),
            PENETRATING_EXPLOSION,
            start_from
        );
        free_vector(number_of_dice);
        free_vector(ds);
        free_vector(numB);
    }
    break;

  case 43:
#line 1059 "src/grammar/dice.yacc"
    {
        /**
        * NUMBER vector
        * die_symbol vector 
        * NUMBER vector
        * EXPLOSION symbol 'e' or similar
        */

        vec numA = (yyvsp[(1) - (4)].values);
        vec ds = (yyvsp[(2) - (4)].values);
        vec numB = (yyvsp[(3) - (4)].values);
        int start_from = ds.content[0];

        roll_plain_sided_dice(
            &numA,
            &numB,
            &(yyval.values),
            PENETRATING_EXPLOSION,
            start_from
        );
        free_vector(numA);
        free_vector(ds);
        free_vector(numB);
    }
    break;

  case 44:
#line 1084 "src/grammar/dice.yacc"
    {
        /**
        * die_symbol vector 
        * NUMBER vector
        * EXPLOSION symbol 'e' or similar
        */

        vec ds = (yyvsp[(1) - (3)].values);
        vec numB = (yyvsp[(2) - (3)].values);
        int start_from = ds.content[0];

        vec number_of_dice;
        initialize_vector(&number_of_dice, NUMERIC, 1);
        number_of_dice.content[0] = 1;
        
        roll_plain_sided_dice(
            &number_of_dice,
            &numB,
            &(yyval.values),
            STANDARD_EXPLOSION,
            start_from
        );
        free_vector(numB);
        free_vector(ds);
        free_vector(number_of_dice);
    }
    break;

  case 45:
#line 1111 "src/grammar/dice.yacc"
    {
        /**
        * NUMBER vector
        * die_symbol vector 
        * NUMBER vector
        */
        vec numA = (yyvsp[(1) - (3)].values);
        vec ds = (yyvsp[(2) - (3)].values);
        vec numB = (yyvsp[(3) - (3)].values);
        int start_from = ds.content[0];

        roll_plain_sided_dice(
            &numA,
            &numB,
            &(yyval.values),
            NO_EXPLOSION,
            start_from
        );
        free_vector(numB);
        free_vector(ds);
        free_vector(numA);
    }
    break;

  case 46:
#line 1134 "src/grammar/dice.yacc"
    {
        /**
        * die_symbol vector 
        * NUMBER vector
        */
        vec ds = (yyvsp[(1) - (2)].values);
        vec numB = (yyvsp[(2) - (2)].values);
        vec new_vec;

        int start_from = ds.content[0];

        vec number_of_dice;
        initialize_vector(&number_of_dice, NUMERIC, 1);
        number_of_dice.content[0] = 1;

        roll_plain_sided_dice(
            &number_of_dice,
            &numB,
            &new_vec,
            NO_EXPLOSION,
            start_from
        );
        free_vector(number_of_dice);
        free_vector(ds);
        free_vector(numB);
        (yyval.values) = new_vec;
    }
    break;

  case 47:
#line 1162 "src/grammar/dice.yacc"
    {   
        /**
        * NUMBER vector
        * die_symbol vector - d or z 
        * MODULE symbol %
        */

        // TODO: z% is not functional!

        vec num_dice = (yyvsp[(1) - (3)].values);
        vec dice_sides;
        initialize_vector(&dice_sides, NUMERIC, 1);
        dice_sides.content[0] = 100;

        roll_plain_sided_dice(
            &num_dice,
            &dice_sides,
            &(yyval.values),
            NO_EXPLOSION,
            1
        );
        free_vector(num_dice);
        free_vector(dice_sides);
    }
    break;

  case 48:
#line 1187 "src/grammar/dice.yacc"
    {
        /**
        * die_symbol vector 
        * NUMBER vector
        */
        // TODO: z% is not possible yet.
        vec num_dice;
        initialize_vector(&num_dice, NUMERIC, 1);
        num_dice.content[0] = 1;
        vec dice_sides;
        initialize_vector(&dice_sides, NUMERIC, 1);
        dice_sides.content[0] = 100;

        roll_plain_sided_dice(
            &num_dice,
            &dice_sides,
            &(yyval.values),
            NO_EXPLOSION,
            1
        );
        free_vector(num_dice);
        free_vector(dice_sides);
    }
    break;

  case 49:
#line 1211 "src/grammar/dice.yacc"
    {
        /**
        * NUMBER vector
        * die_symbol vector 
        * DO_COUNT symbol 'c'
        */
        vec num = (yyvsp[(1) - (3)].values);
        vec die_sym = (yyvsp[(2) - (3)].values);
        int start_from = die_sym.content[0];

        vec dice_sides;
        initialize_vector(&dice_sides, NUMERIC, 1);
        dice_sides.content[0] = 2;

        roll_plain_sided_dice(
            &num,
            &dice_sides,
            &(yyval.values),
            NO_EXPLOSION,
            start_from
        );
        free_vector(num);
        free_vector(die_sym);
    }
    break;

  case 50:
#line 1236 "src/grammar/dice.yacc"
    {
        /**
        * die_symbol vector
        * DO_COUNT symbol 'c'
        */
        vec ds= (yyvsp[(1) - (2)].values);
        int start_from = ds.content[0];

        vec num_dice;
        initialize_vector(&num_dice, NUMERIC, 1);
        num_dice.content[0] = 1;
        vec dice_sides;
        initialize_vector(&dice_sides, NUMERIC, 1);
        dice_sides.content[0] = 2;

        roll_plain_sided_dice(
            &num_dice,
            &dice_sides,
            &(yyval.values),
            NO_EXPLOSION,
            start_from
        );
        free_vector(ds);
        free_vector(num_dice);
        free_vector(dice_sides);
    }
    break;

  case 51:
#line 1263 "src/grammar/dice.yacc"
    {
        /**
        * NUMBER - 
        */
        vec number_of_dice = (yyvsp[(1) - (2)].values);
        vec symb = (yyvsp[(2) - (2)].values);
        vec result_vec;
        initialize_vector(&result_vec, SYMBOLIC, (unsigned int)number_of_dice.content[0]);

        roll_symbolic_dice(
            &number_of_dice,
            &symb,
            &result_vec
        );
        (yyval.values) = result_vec;
        free_vector(symb);
        free_vector(number_of_dice);

    }
    break;

  case 52:
#line 1283 "src/grammar/dice.yacc"
    {
        /** 
        * FATE_DIE - Vector
        */
        vec symb = (yyvsp[(1) - (1)].values);
        vec result_vec;
        vec number_of_dice;
        initialize_vector(&result_vec, SYMBOLIC, 1);
        initialize_vector(&number_of_dice, NUMERIC, 1);
        number_of_dice.content[0] = 1;

        roll_symbolic_dice(
            &number_of_dice,
            &symb,
            &result_vec
        );
        (yyval.values) = result_vec;
        free_vector(symb);
        free_vector(number_of_dice);

    }
    break;

  case 55:
#line 1313 "src/grammar/dice.yacc"
    {
        /**
        * NUMBER - vector
        * die_symbol - vector
        * SYMBOL_LBRACE - the symbol {
        * csd - vector
        * SYMBOL_RBRACE - the symbol }
        */
        // Nd{SYMB}
        vec left = (yyvsp[(1) - (5)].values);
        vec dsymb = (yyvsp[(2) - (5)].values);
        vec right = (yyvsp[(4) - (5)].values);

        // TODO: Multiple ranges

        vec result_vec;
        initialize_vector(&result_vec, SYMBOLIC, (unsigned int)left.content[0]);

        roll_symbolic_dice(
            &left,
            &right,
            &result_vec
        );
        
        free_vector(left);
        free_vector(right);
        free_vector(dsymb);
        (yyval.values) = result_vec;
    }
    break;

  case 56:
#line 1344 "src/grammar/dice.yacc"
    {
        /** @brief 
        * @param die_symbol a vector
        * @param SYMBOL_LBRACE the symbol "{"
        * @param csd a vector
        * @param SYMBOL_LBRACE the symbol "}"
        * returns a vector
        */
        vec csd_vec = (yyvsp[(3) - (4)].values);
        vec number_of_dice;
        vec result_vec;
        initialize_vector(&number_of_dice, NUMERIC, 1);
        number_of_dice.content[0] = 1;
        
        if (csd_vec.dtype == NUMERIC){
            vec dice_sides;
            vec num_dice;
            initialize_vector(&dice_sides, NUMERIC, 1);
            initialize_vector(&num_dice, NUMERIC, 1);
            initialize_vector(&result_vec, NUMERIC, 1);
            num_dice.content[0] = 1;

            int start_value = csd_vec.content[0];
            int end_value = csd_vec.content[csd_vec.length-1];
            dice_sides.content[0] = end_value - start_value + 1;

            // Range
            roll_plain_sided_dice(
                &num_dice,
                &dice_sides,
                &result_vec,
                NO_EXPLOSION,
                start_value
            );
            free_vector(dice_sides);
            free_vector(num_dice);
        }else{
            initialize_vector(&result_vec, SYMBOLIC, 1);

            roll_params rp = {
                .number_of_dice=(unsigned int)number_of_dice.content[0],
                .die_sides=csd_vec.length,
                .dtype=SYMBOLIC,
                .start_value=0,
                .symbol_pool=(char **)safe_calloc(csd_vec.length , sizeof(char *))
            };
            result_vec.source = rp;
            result_vec.has_source = true;
            for(unsigned int i = 0; i != csd_vec.length; i++){
                result_vec.source.symbol_pool[i] = (char*)safe_calloc(sizeof(char),MAX_SYMBOL_LENGTH);
                memcpy(
                    result_vec.source.symbol_pool[i], 
                    csd_vec.symbols[i], 
                    MAX_SYMBOL_LENGTH*sizeof(char)
                );
            }

            // Custom Symbol
            roll_symbolic_dice(
                &number_of_dice,
                &csd_vec,
                &result_vec
            );
        }

        free_vector(number_of_dice);
        free_vector(csd_vec);
        free_vector((yyvsp[(1) - (4)].values));
        (yyval.values) = result_vec;
    }
    break;

  case 57:
#line 1415 "src/grammar/dice.yacc"
    {
        /**
        * MACRO_ACCESSOR the symbol '@'
        * CAPITAL_STRING A vector containing a macro identifier
        * return A vector containing rollparams for the selected  macro
        */
        vec vector = (yyvsp[(2) - (2)].values);
        char * name = vector.symbols[0];

        vec new_vector;
        search_macros(name, &new_vector.source);

        if(gnoll_errno){YYABORT;yyclearin;}
        // Resolve Roll

        vec number_of_dice;
        vec die_sides;

        // Set Num Dice
        initialize_vector(&number_of_dice, NUMERIC, 1);
        number_of_dice.content[0] = (int)new_vector.source.number_of_dice;
        
        // Set Die Sides
        // die_sides.content[0] = (int)new_vector.source.die_sides;
        // die_sides.symbols = NULL;

        // Roll according to the stored values
        // Careful: Newvector used already
        if (new_vector.source.dtype == NUMERIC){
            light_initialize_vector(&die_sides, NUMERIC, 1);
            die_sides.length = new_vector.source.die_sides;
            die_sides.content[0] = (int)new_vector.source.die_sides;
            initialize_vector(&new_vector, new_vector.source.dtype, 1);
            roll_plain_sided_dice(
                &number_of_dice,
                &die_sides,
                &new_vector,
                new_vector.source.explode,
                1
            );
            free_vector(die_sides);

        }else if (new_vector.source.dtype == SYMBOLIC){
            light_initialize_vector(&die_sides, SYMBOLIC, 1);
            die_sides.length = new_vector.source.die_sides;
            free(die_sides.symbols);  
            safe_copy_2d_chararray_with_allocation(
                &die_sides.symbols,
                new_vector.source.symbol_pool,
                die_sides.length,
                MAX_SYMBOL_LENGTH
            );

            free_2d_array(&new_vector.source.symbol_pool, new_vector.source.die_sides);

            initialize_vector(&new_vector, new_vector.source.dtype, 1);
            roll_symbolic_dice(
                &number_of_dice,
                &die_sides,
                &new_vector
            );
            free_vector(die_sides);

        }else{
            printf("Complex Dice Equation. Only dice definitions supported. No operations\n");
            gnoll_errno = NOT_IMPLEMENTED;
        }
        free_vector(vector);
        free_vector(number_of_dice);
        (yyval.values) = new_vector;
    }
    break;

  case 58:
#line 1488 "src/grammar/dice.yacc"
    {
        /**
        * csd a vector containing custom symbols
        * SYMBOL_SEPERATOR the symbol ','
        * csd a vector containing custom symbols
        * return A vector with all the symbols
        */
        vec l = (yyvsp[(1) - (3)].values);
        vec r = (yyvsp[(3) - (3)].values);

        vec new_vector;
        initialize_vector(&new_vector, SYMBOLIC, l.length + r.length);

        concat_symbols(
            l.symbols, l.length,
            r.symbols, r.length,
            new_vector.symbols
        );
        free_vector(l);
        free_vector(r);
        (yyval.values) = new_vector;
    }
    break;

  case 59:
#line 1511 "src/grammar/dice.yacc"
    {
        /**
        * NUMBER The symbol 0-9+
        * RANGE The symbol '..'
        * NUMBER The symbol 0-9+
        * return A vector containing the numeric values as symbols 
        */
        vec start = (yyvsp[(1) - (3)].values);
        vec end = (yyvsp[(3) - (3)].values);

        int s = start.content[0];
        int e = end.content[0];


        if (s > e){
            printf("Range: %i -> %i\n", s, e);
            printf("Reversed Ranged not supported yet.\n");
            gnoll_errno = NOT_IMPLEMENTED;
            YYABORT;
            yyclearin;
        }

        // How many values in this range:
        // 2..2 = 1 
        // 2..3 = 2
        // etc.
        unsigned int spread = (unsigned int)e - (unsigned int)s + 1; 

        vec new_vector;
        initialize_vector(&new_vector, SYMBOLIC, spread);
        for (int i = 0; i <= (e-s); i++){
            sprintf(new_vector.symbols[i], "%d", s+i);
        }
        (yyval.values) = new_vector;
    }
    break;

  case 61:
#line 1549 "src/grammar/dice.yacc"
    {
        /**
        * NUMBER The symbol 0-9+
        * return A vector containing the numeric values as symbols 
        */
        vec in = (yyvsp[(1) - (1)].values);
        // INT_MAX/INT_MIN has 10 characters
        in.symbols = safe_calloc(1, sizeof(char *));  
        in.symbols[0] = safe_calloc(10, sizeof(char));  
        sprintf(in.symbols[0], "%d", in.content[0]);
        free(in.content);
        in.dtype = SYMBOLIC;
        (yyval.values) = in;
    }
    break;

  case 71:
#line 1569 "src/grammar/dice.yacc"
    {
        /**
        * @brief SIDED_DIE The symbol 'd'
        * @param return A vector containing '1', the start index
        */
        vec new_vec;
        initialize_vector(&new_vec, NUMERIC, 1);
        new_vec.content[0] = 1;
        (yyval.values) = new_vec;
    }
    break;

  case 72:
#line 1580 "src/grammar/dice.yacc"
    {
        /**
        * SIDED_DIE The symbol 'z'
        * return A vector containing '0', the start index
        */
        vec new_vec;
        initialize_vector(&new_vec, NUMERIC, 1);
        new_vec.content[0] = 0;
        (yyval.values) = new_vec;
    }
    break;


/* Line 1267 of yacc.c.  */
#line 3195 "y.tab.c"
      default: break;
    }
  YY_SYMBOL_PRINT ("-> $$ =", yyr1[yyn], &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);

  *++yyvsp = yyval;


  /* Now `shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */

  yyn = yyr1[yyn];

  yystate = yypgoto[yyn - YYNTOKENS] + *yyssp;
  if (0 <= yystate && yystate <= YYLAST && yycheck[yystate] == *yyssp)
    yystate = yytable[yystate];
  else
    yystate = yydefgoto[yyn - YYNTOKENS];

  goto yynewstate;


/*------------------------------------.
| yyerrlab -- here on detecting error |
`------------------------------------*/
yyerrlab:
  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
#if ! YYERROR_VERBOSE
      yyerror (YY_("syntax error"));
#else
      {
	YYSIZE_T yysize = yysyntax_error (0, yystate, yychar);
	if (yymsg_alloc < yysize && yymsg_alloc < YYSTACK_ALLOC_MAXIMUM)
	  {
	    YYSIZE_T yyalloc = 2 * yysize;
	    if (! (yysize <= yyalloc && yyalloc <= YYSTACK_ALLOC_MAXIMUM))
	      yyalloc = YYSTACK_ALLOC_MAXIMUM;
	    if (yymsg != yymsgbuf)
	      YYSTACK_FREE (yymsg);
	    yymsg = (char *) YYSTACK_ALLOC (yyalloc);
	    if (yymsg)
	      yymsg_alloc = yyalloc;
	    else
	      {
		yymsg = yymsgbuf;
		yymsg_alloc = sizeof yymsgbuf;
	      }
	  }

	if (0 < yysize && yysize <= yymsg_alloc)
	  {
	    (void) yysyntax_error (yymsg, yystate, yychar);
	    yyerror (yymsg);
	  }
	else
	  {
	    yyerror (YY_("syntax error"));
	    if (yysize != 0)
	      goto yyexhaustedlab;
	  }
      }
#endif
    }



  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse look-ahead token after an
	 error, discard it.  */

      if (yychar <= YYEOF)
	{
	  /* Return failure if at end of input.  */
	  if (yychar == YYEOF)
	    YYABORT;
	}
      else
	{
	  yydestruct ("Error: discarding",
		      yytoken, &yylval);
	  yychar = YYEMPTY;
	}
    }

  /* Else will try to reuse look-ahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:

  /* Pacify compilers like GCC when the user code never invokes
     YYERROR and the label yyerrorlab therefore never appears in user
     code.  */
  if (/*CONSTCOND*/ 0)
     goto yyerrorlab;

  /* Do not reclaim the symbols of the rule which action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;	/* Each real token shifted decrements this.  */

  for (;;)
    {
      yyn = yypact[yystate];
      if (yyn != YYPACT_NINF)
	{
	  yyn += YYTERROR;
	  if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYTERROR)
	    {
	      yyn = yytable[yyn];
	      if (0 < yyn)
		break;
	    }
	}

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
	YYABORT;


      yydestruct ("Error: popping",
		  yystos[yystate], yyvsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  if (yyn == YYFINAL)
    YYACCEPT;

  *++yyvsp = yylval;


  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", yystos[yyn], yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturn;

/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturn;

#ifndef yyoverflow
/*-------------------------------------------------.
| yyexhaustedlab -- memory exhaustion comes here.  |
`-------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  /* Fall through.  */
#endif

yyreturn:
  if (yychar != YYEOF && yychar != YYEMPTY)
     yydestruct ("Cleanup: discarding lookahead",
		 yytoken, &yylval);
  /* Do not reclaim the symbols of the rule which action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
		  yystos[*yyssp], yyvsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif
#if YYERROR_VERBOSE
  if (yymsg != yymsgbuf)
    YYSTACK_FREE (yymsg);
#endif
  /* Make sure YYID is used.  */
  return YYID (yyresult);
}


#line 1594 "src/grammar/dice.yacc"

/* Subroutines */

typedef struct yy_buffer_state * YY_BUFFER_STATE;
extern YY_BUFFER_STATE yy_scan_string(char * str);
extern void yy_delete_buffer(YY_BUFFER_STATE buffer);

int roll_full_options(
    char* roll_request, 
    char* log_file, 
    int enable_verbosity, 
    int enable_introspection,
    int enable_mocking,
    int enable_builtins,
    int mocking_type,
    int mocking_seed
){
    /**
    * @brief the main GNOLL roll function
    * @param roll_request the dice notation to parse
    * @param log_file the file location to write results to
    * @param enable_verbosity Adds extra prints to the program
    * @param enable_introspection Adds per-dice breakdown in the output file
    * @param enable_mocking Replaces random rolls with predictables values for testing
    * @param enable_builtins Load in predefined macros for usage
    * @param mocking_type Type of mock values to generate
    * @param mocking_seed The first value of the mock generation to produce
    * @return GNOLL error code
    */
    gnoll_errno = 0;

    if (enable_verbosity){
        verbose = 1;
        printf("Trying to roll '%s'\n", roll_request);
    }
    if (enable_mocking){
        init_mocking((MOCK_METHOD)mocking_type, mocking_seed);
    }
    if (log_file != NULL){
        write_to_file = 1;
        output_file = log_file;
        if (enable_introspection){
            dice_breakdown = 1;
        }
    }else{
        if (enable_introspection){
            // Introspection is only implemented on a file-basis
            gnoll_errno = NOT_IMPLEMENTED;
            return gnoll_errno;
        }
    }

    initialize();
    
    if(enable_builtins){
        load_builtins("builtins/");
    }
    
    YY_BUFFER_STATE buffer = yy_scan_string(roll_request);
    yyparse();
    yy_delete_buffer(buffer);
    delete_all_macros();

    return gnoll_errno;
}

void load_builtins(char* root){

    int db_setting = dice_breakdown;
    dice_breakdown = 0; // Dont want dice breakdown for all the macro loading

    tinydir_dir dir = (tinydir_dir){0};
    tinydir_open(&dir, root);
    
    int count = 0;
    while (dir.has_next)
    {
        tinydir_file file;
        tinydir_readfile(&dir, &file);
        if(verbose){
            printf("%s", file.name);
        }
        if (file.is_dir)
        {
            if(verbose){
                printf("/\n");
            }
        }else{
            char *ext = strrchr(file.name, '.');

            if(strcmp(".dice", ext) != 0){
                if(verbose){
                    printf("Skip %s\n", file.name);
                }        
                tinydir_next(&dir);
                continue;
            }

            count++;
            if(verbose){
               printf("\n");
            }
            
            unsigned long max_file_path_length = 1000;
            int max_macro_length = 1000;

            char* path = safe_calloc(sizeof(char), max_file_path_length);
            char* stored_str = safe_calloc(sizeof(char), (unsigned long)max_macro_length);
            if(gnoll_errno){return;}

            // Get full path
            strcat(path, "builtins/");
            strcat(path, file.name);
            
            // TODO: Check filename for length
            FILE* fp = fopen(path, "r");
            while (fgets(stored_str, max_macro_length, fp)!=NULL){
                if(verbose){
                    printf("Contents: %s\n",stored_str); 
                }
                YY_BUFFER_STATE buffer = yy_scan_string(stored_str);
                yyparse();
                yy_delete_buffer(buffer);
                if(gnoll_errno){return;}
            }
            fclose(fp);
            free(path);
            free(stored_str);
        }
        tinydir_next(&dir);
    }

    tinydir_close(&dir);
    dice_breakdown = db_setting;
    return;
}

// The following are legacy functions to be deprecated in the future
// in favor of the general roll_full_options() fn.

int roll(char * s){
    return roll_full_options(s, NULL, 1, 0, 0, 0, 0, 0);
}

int roll_with_breakdown(char * s, char* f){
    return roll_full_options(s, f, 0, 1, 0, 0, 0, 0);
}

int roll_and_write(char* s, char* f){
    return roll_full_options(s, f, 0, 0, 0, 0, 0, 0);
}

void roll_and_write_R(int* return_code, char** s, char** f){    
    (*return_code) = roll_full_options(s[0], f[0], 0, 0, 0, 0, 0, 0);
}

int mock_roll(char * s, char * f, int mock_value, int mock_const){
    return roll_full_options(s, f, 0, 0, 1, 0, mock_value, mock_const);
}

int main(int argc, char **str){

    for(int a = 1; a != argc; a++){
        if(strcmp(str[a], "--help")==0){
            printf("GNOLL Dice Notation Parser\n");
            printf("Usage: ./executable [dice notation]\n");
            printf("Executable is non configurable. Use functions directly for advanced features.\n");
            return 0;
        }
        if(strcmp(str[a], "--version")==0){
            printf("GNOLL 4.3.0\n");
            return 0;
        }
    }
    
    // Join arguments if they came in as seperate strings
    char * s = concat_strings(&str[1], (unsigned int)(argc - 1));

    remove("output.dice");
    roll_full_options(
        s,
        "output.dice",
        0,  // Verbose
        0,  // Introspect
        0,  // Mocking
        1,  // Builtins
        0,  // Mocking
        0   // Mocking Seed
    );
    print_gnoll_errors();
    FILE  *f = fopen("output.dice","r");
    int c;
    printf("Result:\n");
    if (f){
        while((c = getc(f)) !=  EOF){
            putchar(c);
        }
        fclose(f);
    }
    // Final Freeing
    free(macros);
}

int yyerror(s)
const char *s;
{
    fprintf(stderr, "%s\n", s);

    if(write_to_file){
        FILE *fp;
        fp = safe_fopen(output_file, "a+");
        fprintf(fp, "%s;", s);
        fclose(fp);
    }
    return(gnoll_errno);

}

int yywrap(){
    return (1);
}


