"""
Laboratory Work 2: Numerical Series Calculation
Calculates series expansion based on given precision and range.
"""

A, B = 0, 1


class NotInScope(Exception):
    pass


class LessThan0(Exception):
    pass


def calculate_series(x, eps):
    """Calculates the series value for given x and epsilon."""
    suma = x / 2  # first term, n = 0
    prevSum = 0
    n = 1
    minus_1_pow = -1  # -1**1
    n_factorial = 1  # 1!
    x_pow = x * x  # x**2
    n_2_plus_2_factorial = 24  # 4!

    while (suma - prevSum > eps) and (prevSum - suma < -eps):
        prevSum = suma
        suma += (minus_1_pow * n_factorial * n_factorial * x_pow) / n_2_plus_2_factorial
        minus_1_pow *= -1
        x_pow *= x
        n += 1
        n_factorial *= n
        n_2_plus_2_factorial *= (2 * n + 1) * (2 * n + 2)

    return suma


def main():
    """Main execution function."""
    try:
        x = float(input('Enter a number from the range [0 ; 1]: '))
        eps = float(input('Enter precision value (> 0): '))

        if x < A or x > B:
            raise NotInScope
        elif eps < 0:
            raise LessThan0
        
        print('Calculating...', end='')
        res = calculate_series(x, eps)
        print(' Done.')
        print(f'For x = {x:.4f}\nFor epsilon = {eps:.5E}\nResult = {res:.10f}')

    except KeyboardInterrupt:
        print('\nProgram aborted by user.')
    except EOFError:
        print('\nError: Input ended unexpectedly.')
    except ValueError:
        print('\nError: Could not convert input to float.')
    except ArithmeticError:
        print('\nError: Arithmetic calculation error.')
    except LessThan0:
        print(f'\nError: Precision ({eps:.5E}) must be greater than 0.')
    except NotInScope:
        print(f'\nError: x ({x:.4f}) is out of range [{A}, {B}].')


if __name__ == '__main__':
    main()
