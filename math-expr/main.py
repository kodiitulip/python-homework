from __future__ import annotations

from dataclasses import dataclass
from re import findall

@dataclass(order=True)
class ExpressionNode:
    value: str
    left: ExpressionNode | None = None
    right: ExpressionNode | None = None

    def get_children(self) -> tuple[ExpressionNode | None, ExpressionNode | None]:
        return self.left, self.right


class ExpressionTree:
    def __init__(self, expr: str) -> None:
        self.__expr: list[str] = self.__tokenize(expr)
        self.__root: ExpressionNode | None = self.__build_tree(self.__expr)
        
    def evaluate(self) -> float:
        def _eval(node: ExpressionNode | None) -> float:
            if node is None:
                return 0
            left, right = node.get_children()
            if left is None and right is None:
                return float(node.value)
            val_left, val_right = _eval(left), _eval(right)
            match node.value:
                case '+':
                    return val_left + val_right
                case '-':
                    return val_left - val_right
                case '*':
                    return val_left * val_right
                case '/':
                    return val_left / val_right
                case '**':
                    return val_left ** val_right
        return _eval(self.__root)

    @staticmethod
    def __build_tree( postfix: list[str]) -> ExpressionNode:
        stack = []

        for token in postfix:
            if token.isnumeric():
                stack.append(ExpressionNode(token))
            else:
                stack.append(ExpressionNode(value=token, right=stack.pop(), left=stack.pop()))

        return stack.pop()

    def __tokenize(self,expr: str) -> list[str]:
        return self.__infix_to_postfix(findall(r'\d+|[-+*/()]+', expr))
        #return self.__infix_to_postfix([op for op in expr.split() if op.strip()]) # without using regex

    @staticmethod
    def __infix_to_postfix(tokens: list[str]) -> list[str]:
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '**': 3} # value of precedence for each operator
        stack = [] # local stack of operands and operators
        output = [] # local output
        for token in tokens:
            if token.isnumeric():
                output.append(token)
            elif token in precedence:
                while stack and precedence.get(stack[-1], 0) >= precedence.get(token, 0):
                    output.append(stack.pop())
                stack.append(token)
            else:
                output.append('0')
        while stack:
            output.append(stack.pop())
        return output

    def __str__(self):
        return f"ExpressionTree({self.__expr})\n{self.__root}\nEvaluation: {self.evaluate()}"

if __name__ == '__main__':
    exp = "5 + 5 ** 2 + 3"
    tree = ExpressionTree(exp)
    print(tree)
