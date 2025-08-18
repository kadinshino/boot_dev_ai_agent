# --- calculator/pkg/calculator.py ---

precedence = {'+': 2, '-': 2, '*': 3, '/': 3}

def evaluate(expression):
    def get_tokens(expr):
        return expr.replace('(', ' ( ').replace(')', ' ) ').split()

    def shunting_yard(tokens):
        output = []
        stack = []
        for token in tokens:
            if token.isdigit():
                output.append(int(token))
            elif token in precedence:
                while stack and stack[-1] in precedence and precedence[token] <= precedence[stack[-1]]:
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
        while stack:
            output.append(stack.pop())
        return output

    def eval_rpn(rpn):
        stack = []
        for token in rpn:
            if isinstance(token, int):
                stack.append(token)
            else:
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    stack.append(a // b)
        return stack[0]

    tokens = get_tokens(expression)
    rpn = shunting_yard(tokens)
    return eval_rpn(rpn)