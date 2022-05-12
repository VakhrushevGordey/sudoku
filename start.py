class SudokuSolver:
    def solve(self, sudoku):
        sol = [row[:] for row in sudoku]
        if self.gen(sol):
            return sol
        return None

    def get_row(self, ri, table):
        return set(table[ri][:])

    def get_col(self, ci, table):
        return set(table[r][ci] for r in range(9))

    def get_block(self, pos, table):
        ri, ci = pos
        r0 = 3 * (ri // 3)
        c0 = 3 * (ci // 3)
        return set(table[r0 + r][c0 + c] for r in range(3) for c in range(3))

    def get_all(self, pos, table):
        ri, ci = pos
        values = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        values -= self.get_row(ri, table)
        values -= self.get_col(ci, table)
        values -= self.get_block((ri, ci), table)
        return values

    def is_sudoku_correct(self, table):
        for i in range(9):
            if not self.is_line_correct(table[i][:]):
                return False
            if not self.is_line_correct([table[r][i] for r in range(9)]):
                return False
        # для 3х3
        for i in range(3):
            for j in range(3):
                if not self.is_line_correct([table[i * 3 + r][j * 3 + c] for r in range(3) for c in range(3)]):
                    return False
        return True


    def is_line_correct(self, line):
        a = []
        if len(line) != 9:
            return False
        for i in range(9):
            if line[i]:
                if line[i] in a:
                    return False
                else:
                    a.append(line[i])
        return True

    def gen(self, sol):
        mn = None
        while True:
            mn = None
            for ri in range(9):
                for ci in range(9):
                    if sol[ri][ci] != 0:
                        continue
                    values = self.get_all((ri, ci), sol)
                    count = len(values)
                    if count == 0:
                        return False
                    if count == 1:
                        sol[ri][ci] = values.pop()
                    if not mn or \
                            count < len(mn[1]):
                        mn = ((ri, ci), values)
            if not mn:
                return True
            elif 1 < len(mn[1]):
                break
        r, c = mn[0]
        for v in mn[1]:
            sol1 = sol[:]
            sol1[r][c] = v
            if self.gen(sol1):
                for r in range(9):
                    for c in range(9):
                        sol[r][c] = sol1[r][c]
                return True
        return False


def show(table, file=None):
    table = [[e if e else "." for e in row] for row in table]
    i = 0
    f = file
    for row in table:
        i += 1
        print(*row[0:3], sep=' ', end='\t', file=f)
        print(*row[3:6], sep=' ', end='\t', file=f)
        print(*row[6:9], sep=' ', end='\t', file=f)
        print(file=f)
        if i == 3:
            i = 0
            print(file=f)


def show_two(table10, table2, file=None):
    table1 = [[e if e else "." for e in row] for row in table10]
    i = 0
    f = file
    for j in range(9):
        row1 = table1[j]
        row2 = table2[j]
        i += 1
        print(*row1[0:3], sep=' ', end='\t', file=f)
        print(*row1[3:6], sep=' ', end='\t', file=f)
        print(*row1[6:9], sep=' ', end='\t', file=f)

        print("\t", end="\t", file=f)

        print(*row2[0:3], sep=' ', end='\t', file=f)
        print(*row2[3:6], sep=' ', end='\t', file=f)
        print(*row2[6:9], sep=' ', end='\t', file=f)

        print(file=f)
        if i == 3:
            i = 0
            print(file=f)


import datetime
now = datetime.datetime.now().strftime("%m-%d-%H-%M")


sudoku = []
f = open("input.txt", "r")
for i in range(11):
    s = f.readline()
    a = list(map(lambda x: int(x) if x != "." else 0, s.split()))
    if i not in (3, 7):
        sudoku.append(a)
f.close()


f = open("log.txt", "a")
print(f"ЗАПУСК ОТ {now}", file=f)
out = open('output.txt', 'w')
try:
    solver = SudokuSolver()
    print("SOlVE:", file=out)
    sol = solver.solve(sudoku)
    if sol:
        show(sol, file=out)
        show_two(sudoku, sol, file=f)
    else:
        print("НЕ РЕШАЕТСЯ", file=f)
except Exception as e:
    print(f"ОШИБКА: {str(e)}", file=f)
out.close()
f.close()
