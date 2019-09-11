// A simple translation from the problem of finding variable dependencies in CNF into GMUS
// Based on parsing utilities of Minisat

// The translation works as follows:
//   - For each original variable x_i, create y_i, a_i, b_i.
//   - Output GCNF
//      GROUP 0:
//       F(x_1, ..., x_n)
//       F(y_1, ..., y_n)
//       a_i -> (x_i = y_i) for each i
//       (x_i = b_i) -> b_i for each i
//       (-b1, ..., -b_n)
//      GROUP i:
//       (a_i)
//   #vars    = 4 * n
//   #clauses = 2 * c + 4 * n + 1 + n
//   #groups  = n
//
//   Note: GMUS information pritned by GMUSers automatically corresponds to the list of independent variables

// CNF parsing code is copied from Minisat.

#include <stdio.h>
#include <stdlib.h>
#include <zlib.h>
#include <iostream>
#include <vector>

using namespace std;

// globals
int vars = 0;
int clauses = 0;

//-------------------------------------------------------------------------------------------------
// A simple buffered character stream class:

static const int buffer_size = 1048576;

class StreamBuffer
{
    gzFile in;
    unsigned char buf[buffer_size];
    int pos;
    int size;

    void assureLookahead()
    {
        if (pos >= size) {
            pos = 0;
            size = gzread(in, buf, sizeof(buf));
        }
    }

   public:
    explicit StreamBuffer(gzFile i) : in(i), pos(0), size(0)
    {
        assureLookahead();
    }

    int operator*() const
    {
        return (pos >= size) ? EOF : buf[pos];
    }
    void operator++()
    {
        pos++;
        assureLookahead();
    }
    int position() const
    {
        return pos;
    }
};

//-------------------------------------------------------------------------------------------------
// End-of-file detection functions for StreamBuffer and char*:

static inline bool isEof(StreamBuffer& in)
{
    return *in == EOF;
}
static inline bool isEof(const char* in)
{
    return *in == '\0';
}

//-------------------------------------------------------------------------------------------------
// Generic parse functions parametrized over the input-stream type.

template <class B>
static void skipWhitespace(B& in)
{
    while ((*in >= 9 && *in <= 13) || *in == 32)
        ++in;
}

template <class B>
static void skipLine(B& in)
{
    for (;;) {
        if (isEof(in))
            return;
        if (*in == '\n') {
            ++in;
            return;
        }
        ++in;
    }
}

template <class B>
static int parseInt(B& in)
{
    int val = 0;
    bool neg = false;
    skipWhitespace(in);
    if (*in == '-')
        neg = true, ++in;
    else if (*in == '+')
        ++in;
    if (*in < '0' || *in > '9')
        fprintf(stderr, "PARSE ERROR! Unexpected char: %c\n", *in), exit(3);
    while (*in >= '0' && *in <= '9')
        val = val * 10 + (*in - '0'), ++in;
    return neg ? -val : val;
}

// String matching: in case of a match the input iterator will be advanced the corresponding
// number of characters.
template <class B>
static bool match(B& in, const char* str)
{
    int i;
    for (i = 0; str[i] != '\0'; i++)
        if (in[i] != str[i])
            return false;

    in += i;

    return true;
}

// String matching: consumes characters eagerly, but does not require random access iterator.
template <class B>
static bool eagerMatch(B& in, const char* str)
{
    for (; *str != '\0'; ++str, ++in)
        if (*str != *in)
            return false;
    return true;
}

template <class B>
static void readClause(B& in, vector<int>& lits)
{
    int parsed_lit;
    lits.clear();
    for (;;) {
        parsed_lit = parseInt(in);
        if (parsed_lit == 0)
            break;
        lits.push_back(parsed_lit);
    }
}

static int y(int x)
{
    return (x > 0) ? x + vars : x - vars;
}
static int a(int x)
{
    return x + 2 * vars;
}
static int b(int x)
{
    return x + 3 * vars;
}

template <class B>
static void parse_convert_DIMACS_main(B& in, FILE* out, bool useInd)
{
    bool printHeader =
        true; // HACK: on some unigen benchmarks the line "p cnf" appears multiple times
    vector<int> lits;

    // some benchmarks include user suggestion for what the independent support should be
    vector<bool> seenInds;

    for (;;) {
        skipWhitespace(in);
        if (*in == EOF)
            break;
        else if (*in == 'p') {
            if (eagerMatch(in, "p cnf")) {
                vars = parseInt(in);
                clauses = parseInt(in);
                if (printHeader) {
                    fprintf(out, "p gcnf %d %d %d\n", 4 * vars,
                            2 * clauses + 5 * vars + 1, vars);
                    printHeader = false;
                    seenInds.resize(vars + 1, false);
                }

            } else {
                printf("PARSE ERROR! Unexpected char: %c\n", *in), exit(3);
            }
        } else if (*in == 'c') {
            if (eagerMatch(in, "c ind")) {
                readClause(in, lits);

                //printf("read: ");
                /*for (unsigned i=0; i<lits.size(); ++i){
                    printf("%d ", lits[i]);
                }*/
                printf("\n");

                for (unsigned i = 0; i < lits.size(); ++i) {
                    if (lits[i] <= 0) {
                        printf("PARSE ERROR! Negative induction group %d\n",
                               lits[i]),
                            exit(3);
                    }
                    if (lits[i] >= seenInds.size())
                        seenInds.resize(lits[i] + 1, false);
                    seenInds[lits[i]] = true;
                }
                skipLine(in);

            } else
                skipLine(in);

        } else if (*in == 'c' || *in == 'p')
            skipLine(in);
        else {
            readClause(in, lits);

            // F(x_1, ..., x_n)
            fprintf(out, "{0} ");
            for (unsigned i = 0; i < lits.size(); ++i)
                fprintf(out, "%d ", lits[i]);
            fprintf(out, "0\n");

            // F(y_1, ..., y_n)
            fprintf(out, "{0} ");
            for (unsigned i = 0; i < lits.size(); ++i)
                fprintf(out, "%d ", y(lits[i]));
            fprintf(out, "0\n");
        }
    }

    bool includeAll = true;
    for (int i = 1; i < seenInds.size(); ++i) {
        if (seenInds[i]) {
            includeAll = false;
            break;
        }
    }

    for (int i = 1; i <= vars; ++i) {
        // a_i -> (x_i = y_i)
        fprintf(out, "{0} %d %d %d 0\n", -a(i), -i, y(i));
        fprintf(out, "{0} %d %d %d 0\n", -a(i), i, -y(i));

        // (x_i = y_i) -> b_i
        fprintf(out, "{0} %d %d %d 0\n", b(i), i, y(i));
        fprintf(out, "{0} %d %d %d 0\n", b(i), -i, -y(i));
    }

    // (-b1, ..., -b_n)
    fprintf(out, "{0} ");
    for (int i = 1; i <= vars; ++i)
        fprintf(out, "%d ", -b(i));
    fprintf(out, "0\n");

    for (int i = 1; i <= vars; ++i) {
        // {i} (a_i)
        if ((!useInd ||
            (useInd && (includeAll || (!includeAll && seenInds[i])))
            )
        ) {
            fprintf(out, "{%d} %d 0\n", i, a(i));
            //printf("%d ",i);
        }
    }
    //printf("\n %d \n",vars);
    exit(0);
}

static void parse_convert_DIMACS(gzFile input_stream, FILE* out, bool useInd)
{
    StreamBuffer in(input_stream);
    parse_convert_DIMACS_main(in, out, useInd);
}

int main(int argc, char** argv)
{
    if (argc < 3 || argc > 5) {
        printf("USAGE: <converter> input file, output file [useInd]\n\n");
        printf(
            "useInd: (optional)  indicates whether to use the independent "
            "support supplied in input cnf file in 'c ind' format (default: "
            "false)\n.[Note:} If useInd is true and no independent support is "
            "given in cnf file, all variables are considered.\n");
        printf(
            "[Note:] If an independent support is supplied both by specifying "
            "n and useInd as true, then the union of the two independent "
            "supports\n is taken as the input independent support. If no "
            "independent support is found in the cnf file with useInd as true "
            "with n specified\n then only first n variables are considered as "
            "independent support\n\n");
        printf("eg: ./togmus input.cnf output.gcnf true 400\n");
        printf(
            "Since useInd is true and n is supplied, the input independent "
            "support is taken to be union of the set of variables\n");
        printf("given in 'c ind' format in input.cnf and variables 1 to 400\n");
        exit(1);
    }

    gzFile in = gzopen(argv[1], "rb");
    if (in == NULL) {
        fprintf(stderr, "Could not open file: %s\n", argv[1]), exit(1);
    }

    FILE* out = fopen(argv[2], "wr");
    if (out == NULL) {
        fprintf(stderr, "Could not open file: %s\n", argv[2]), exit(1);
    }

    bool useInd = false;
    if (argc > 3) {
        std::string indParam = argv[3];
        if (indParam.compare("True") == 0) {
            useInd = true;
        }
    }

    parse_convert_DIMACS(in, out, useInd);

    gzclose(in);
    fclose(out);

    return 0;
}
