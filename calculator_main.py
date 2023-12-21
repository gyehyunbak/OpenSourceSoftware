import sys
from PyQt5.QtWidgets import *

class Main(QDialog):
    # 연산식 저장을 위한 전역 변수 선언
    operator = ""
    result = 0.0

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        ### 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        layout_equation_solution = QFormLayout()
        layout_buttons = QGridLayout()

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        self.equation = QLineEdit("") 

        ### layout_equation_solution 레이아웃에 수식, 답 위젯을 추가
        layout_equation_solution.addRow(self.equation)

        ### 사칙연산 버튼 생성
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_division = QPushButton("/")
        button_modulo = QPushButton("%")
        button_inverse = QPushButton("1/x")
        button_square = QPushButton("x²")
        button_square_root = QPushButton("²√x")

        ### 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))
        button_modulo.clicked.connect(lambda state, operation = "%": self.button_operation_clicked(operation))

        ### 단항연산자 시그널 설정
        button_inverse.clicked.connect(self.button_inverse_clicked)
        button_square.clicked.connect(self.button_square_clicked)
        button_square_root.clicked.connect(self.button_square_root_clicked)

        ### =, clear, backspace 버튼 생성
        button_equal = QPushButton("=")
        button_clear = QPushButton("Clear")
        button_backspace = QPushButton("Backspace")

        ### CE, C 버튼 생성
        button_CE = QPushButton("CE")
        button_C = QPushButton("C")

        ### =, clear, backspace, CE, C 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)
        button_CE.clicked.connect(self.button_clear_clicked)
        button_C.clicked.connect(self.button_clear_clicked)

        ### 모든 버튼을 하나의 그리드 레이아웃 layout_buttons에 통합
        ### 연산버튼 추가
        ### 첫째 행
        layout_buttons.addWidget(button_modulo, 0, 0)
        layout_buttons.addWidget(button_CE, 0, 1)
        layout_buttons.addWidget(button_C, 0, 2)
        layout_buttons.addWidget(button_backspace, 0, 3)

        ### 둘째 행
        layout_buttons.addWidget(button_inverse, 1, 0)
        layout_buttons.addWidget(button_square, 1, 1)
        layout_buttons.addWidget(button_square_root, 1, 2)
        layout_buttons.addWidget(button_division)

        ### 셋째 행
        ### 숫자 버튼 추가
        buttons = ['7', '8', '9'],['4', '5', '6'],['1', '2', '3']

        for i in range(3):
            for j in range(3):
                number = buttons[i][j]
                button = QPushButton(str(number))
                button.clicked.connect(lambda state, num = number:
                                        self.number_button_clicked(num))
                
                layout_buttons.addWidget(button, i+2, j)

        ### 0 버튼 추가 및 시그널 설정
        button_zero = QPushButton('0')
        button_zero.clicked.connect(lambda state, num = "0": self.number_button_clicked(num))
        layout_buttons.addWidget(button_zero, 5, 1)

        ### 소숫점 버튼과 00 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout_buttons.addWidget(button_dot, 5, 2)

        button_double_zero = QPushButton("00")
        button_double_zero.clicked.connect(lambda state, num = "00": self.number_button_clicked(num))
        layout_buttons.addWidget(button_double_zero, 5, 0)

        ### 나머지 사칙 연산 버튼 연결
        layout_buttons.addWidget(button_plus, 4, 3)
        layout_buttons.addWidget(button_minus, 3, 3)
        layout_buttons.addWidget(button_product, 2, 3)
        layout_buttons.addWidget(button_equal, 5, 3)

        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution)
        main_layout.addLayout(layout_buttons)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    def number_button_clicked(self, num):
        equation = self.equation.text()
        equation += str(num)
        self.equation.setText(equation)

    def button_operation_clicked(self, operation):
        try:
            if not (self.equation.text()):
                return
            
            if (Main.result == 0.0):
                Main.result = float(self.equation.text())
            else:
                self.update_result()

            Main.operator = operation
            self.equation.setText("")

        except ValueError: # 잘못된 입력에 대한 엑셉션
            self.equation.setText("Error: Invalid input")

    ### 단항연산자 계산 함수
    # 역수
    def button_inverse_clicked(self):
        equation = self.equation.text()
        try:
            result = 1 / float(equation)
            self.equation.setText(str(result))
        except ZeroDivisionError:
            self.equation.setText("Error: Division by zero")
        except ValueError:
            self.equation.setText("Error: Invalid input")

    # 제곱
    def button_square_clicked(self):
        equation = self.equation.text()
        try:
            result = float(equation) ** 2
            self.equation.setText(str(result))
        except ValueError:
            self.equation.setText("Error: Invalid input")
        
    # 제곱근
    def button_square_root_clicked(self):
        equation = self.equation.text()
        try:
            result = float(equation) ** 0.5
            self.equation.setText(str(result))
        except ValueError:
            self.equation.setText("Error: Invalid input")

    def button_equal_clicked(self):
        if not (self.equation.text()): # 두 번째 항이 입력되지 않은 경우 연산하지 않음
            return
        
        self.update_result()

        self.equation.setText(str(Main.result))
        Main.result = 0.0
        #self.equation.setText(Main.global_equation)

    def button_clear_clicked(self):
        self.equation.setText("")
        Main.result = 0.0

    def button_backspace_clicked(self):
        equation = self.equation.text()
        equation = equation[:-1]
        self.equation.setText(equation)

    ### 결과값 전역 변수 업데이트(현재 연산자에 대한 연산 실행)
    def update_result(self):
        if(self.equation.text()):
            second_term = float(self.equation.text())
            if(Main.operator == '+'): # 덧셈
                Main.result += second_term
            elif(Main.operator == '-'): # 뺄셈
                Main.result -= second_term
            elif(Main.operator == '*'): # 곱셈
                Main.result *= second_term
            elif(Main.operator == '/'): # 나눗셈
                Main.result /= second_term
            elif(Main.operator == '%'): # 모듈로
                Main.result %= second_term

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())