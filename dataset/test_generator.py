from dataset.opportunity_detector import detect_opportunities


program = """int compute(int x, int y) {
    int a;
    int b;
    int c;

    a = x + 0;
    b = y * 2;
    c = a + (4 + 3);

    return c;
}"""


opportunities = detect_opportunities(program)

print("Detected opportunities:")

for opportunity in sorted(opportunities):
    print("-", opportunity)