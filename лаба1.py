import re
import math

class Calculator:
    def __init__(self, text):
        # ЛЕКСЕР: Разбиваем строку на токены
        self.tokens = re.findall(r'\d+\.\d+|\d+|tan|[+\-*/()|]', text)
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, expected=None):
        tok = self.peek()
        if expected is not None and tok != expected:
            raise SyntaxError(f"Ожидалось '{expected}', получено '{tok}'")
        self.pos += 1
        return tok

    def run(self):
        return self.parse_or()

    def parse_or(self):
        left = self.parse_sum()
        while self.peek() == '|':
            self.eat('|')
            right = self.parse_sum()
            left = int(left) | int(right)
        return left

    def parse_sum(self):
        left = self.parse_mul()
        while self.peek() in ('+', '-'):
            op = self.eat()
            right = self.parse_mul()
            left = left + right if op == '+' else left - right
        return left

    def parse_mul(self):
        left = self.parse_unary()
        while self.peek() in ('*', '/'):
            op = self.eat()
            right = self.parse_unary()
            if op == '/':
                if right == 0:
                    raise ZeroDivisionError("Деление на ноль!")
                left = left / right
            else:
                left = left * right
        return left

    def parse_unary(self):
        if self.peek() in ('+', '-'):
            op = self.eat()
            val = self.parse_unary()
            return -val if op == '-' else val
        return self.parse_atom()

    def parse_atom(self):
        tok = self.peek()
        
        if tok == 'tan':
            self.eat('tan')
            self.eat('(')
            val = self.parse_or()
            self.eat(')')
            return math.tan(val)
            
        elif tok == '(':
            self.eat('(')
            val = self.parse_or()
            self.eat(')')
            return val
            
        else:
            if tok is None:
                raise SyntaxError("Неожиданный конец выражения")
            return float(self.eat())


# Главный блок программы
if __name__ == "__main__":
    text = input("Введите пример: ")
    
    try:
        calc = Calculator(text)
        result = calc.run()
        
        # Проверка на лишние знаки в конце
        if calc.peek() is not None:
            print("Введены лишние знаки")
        else:
            # Красивый вывод (убираем .0, если число целое)
            result = round(result, 10)
            if result == int(result):
                result = int(result)
            print("Ответ:", result)
            
    except Exception as e:
        print(f"Ошибка: {e}")
