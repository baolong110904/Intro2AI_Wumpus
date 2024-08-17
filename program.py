class Program:
    def __init__(self, filename):
        self.map_size = 0
        self.map = []
        self.read_map(filename)
    
    def get_map_size(self):
        return self.map_size
    
    def read_map(self, filename):
        with open(filename, 'r') as file:
            self.map_size = int(file.readline().strip())
            self.map = [line.strip().split('.') for line in file]
            
        self.update_map()
        self.output(filename)

    def update_map(self):
        for i in range(self.map_size):
            for j in range(self.map_size):
                if 'W' in self.map[i][j]:
                    self.add_stench(i, j)
        
        for i in range(self.map_size):
            for j in range(self.map_size):
                if 'P_G' not in self.map[i][j] and ('H_P' not in self.map[i][j]) and 'P' in self.map[i][j]:
                    self.add_breeze(i, j)
                    
        for i in range(self.map_size):
            for j in range(self.map_size):
                if 'P_G' in self.map[i][j]:
                    self.add_whiff(i, j)
        
        for i in range(self.map_size):
            for j in range(self.map_size):
                if 'H_P' in self.map[i][j]:
                    self.add_glow(i, j)
                    
    def get_map(self):
        return self.map_size, self.map
                    
    def add_stench(self, i, j):
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.map_size and 0 <= nj < self.map_size:
                if 'S' not in self.map[ni][nj]:
                    if self.map[ni][nj] == '-':
                        self.map[ni][nj] = 'S'
                    else:
                        self.map[ni][nj] += ',S'

    def add_breeze(self, i, j):
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.map_size and 0 <= nj < self.map_size:
                if 'B' not in self.map[ni][nj]:
                    if self.map[ni][nj] == '-':
                        self.map[ni][nj] = 'B'
                    else:
                        self.map[ni][nj] += ',B'

    def add_whiff(self, i, j):
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.map_size and 0 <= nj < self.map_size:
                if 'W_H' not in self.map[ni][nj]:
                    if self.map[ni][nj] == '-':
                        self.map[ni][nj] = 'W_H'
                    else:
                        self.map[ni][nj] += ',W_H'

    def add_glow(self, i, j):
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.map_size and 0 <= nj < self.map_size:
                if 'G_L' not in self.map[ni][nj]:
                    if self.map[ni][nj] == '-':
                        self.map[ni][nj] = 'G_L'
                    else:
                        self.map[ni][nj] += ',G_L'

    def output(self, filename):
        with open('output_' + filename, 'w') as file:
            for row in self.map:
                file.write('.'.join(row) + '\n')


# Example usage
if __name__ == "__main__":
    program = Program('map1.txt')
